import boto3
from loguru import logger
from botocore.exceptions import ClientError
from fastapi.responses import Response, HTMLResponse, FileResponse, RedirectResponse
from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.staticfiles import StaticFiles
from pathlib import Path    
import mimetypes
import uvicorn
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env") #load env

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)


cursor = conn.cursor(cursor_factory=RealDictCursor)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id SERIAL PRIMARY KEY,
        s3_key TEXT NOT NULL,
        original_filename TEXT NOT NULL,
        share_token TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")
conn.commit()

AWS_BUCKET = os.getenv("AWS_BUCKET") # S3 aws bucket
s3 = boto3.resource(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

s3_client = boto3.client( #Presignel URL client
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)
bucket = s3.Bucket(AWS_BUCKET)


MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE_MB", 5)) * 1024 * 1024  # MB -> byte and file type, max size 
SUPPORTED_FILE_TYPES = ['image/jpeg', 'image/png', 'application/pdf']


def s3_upload(contents: bytes, key: str): # S3 function
    logger.info(f'Uploading {key} to s3')
    bucket.put_object(Key=key, Body=contents)



app = FastAPI()

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"  #Path to frontend
STATIC_DIR = FRONTEND_DIR 


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static") #static file for frontend


@app.get("/frontend", response_class=HTMLResponse) #frontend
async def serve_frontend():
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(index_path)

@app.post("/upload") #upload endpoint
async def upload(file: UploadFile = File(...)):
    ext_map = {
        'image/jpeg': 'jpg',
        'image/png': 'png',
        'application/pdf': 'pdf'
    }

    share_token = uuid4().hex  #unique shareurl

    contents = await file.read() #read file contents
    size = len(contents)
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Max file size is {MAX_FILE_SIZE//1024//1024}MB!")

    file_type, _ = mimetypes.guess_type(file.filename) #file type check
    if file_type not in SUPPORTED_FILE_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_type}")

    ext = ext_map[file_type]      
    key = f"{uuid4()}.{ext}"
    s3_upload(contents=contents, key=key)

    cursor.execute( #store file metadata in db
        "INSERT INTO files (s3_key, original_filename, share_token) VALUES (%s, %s, %s) RETURNING id",
        (key, file.filename, share_token)
    )
    file_id = cursor.fetchone()['id']
    conn.commit()

    share_url = f"/file/{share_token}" #share url path
    return {"file_id": file_id, "filename": file.filename, "share_url": share_url}


@app.get("/download")
async def download(token: str):
    cursor.execute("SELECT s3_key, original_filename FROM files WHERE share_token=%s", (token,))
    file_info = cursor.fetchone()
    
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")


    try: #Presigned URL creation
        presigned_url = s3_client.generate_presigned_url( 
            'get_object',
            Params={
                'Bucket': AWS_BUCKET,
                'Key': file_info['s3_key'],
                'ResponseContentDisposition': f'attachment; filename="{file_info["original_filename"]}"' #download as original filename
            },
            ExpiresIn=3600  #Link expiration time (1 hour)
        )
    except ClientError as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Link olusturulamadi")
    return RedirectResponse(url=presigned_url)

@app.get("/file/{share_token}", response_class=HTMLResponse) #file download page
async def file_page(share_token: str):
    cursor.execute("SELECT s3_key, original_filename FROM files WHERE share_token=%s", (share_token,)) #fetch file metadata
    file_info = cursor.fetchone()
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")

    html = f""" 
    <html>
    <head>
      <title>Download File</title>
      <style>
        body {{
          font-family: Arial;
          text-align: center;
          margin-top: 100px;
        }}
        a {{
          text-decoration: none;
        }}
        button {{
          background-color: #4CAF50;
          color: white;
          padding: 10px 20px;
          border: none;
          border-radius: 8px;
          cursor: pointer;
        }}
      </style>
    </head>
    <body>
      <h2>File Ready 🔽</h2>
      <a href="/download?token={share_token}">
        <button>Download</button>
      </a>
    </body>
    </html>
    """
    return HTMLResponse(content=html) #return html page

if __name__ == "__main__": #run app
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) #dev server
