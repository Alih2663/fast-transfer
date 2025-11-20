resource "aws_s3_bucket" "file_bucket" {
  bucket = var.s3_bucket_name 
}

resource "aws_s3_bucket_public_access_block" "file_bucket" {
  bucket = aws_s3_bucket.file_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true 
}

resource "aws_s3_bucket_versioning" "file_bucket" {
  bucket = aws_s3_bucket.file_bucket.id

  versioning_configuration {
    status = "Disabled"
  }
}

resource "aws_s3_bucket_cors_configuration" "file_bucket" {
  bucket = aws_s3_bucket.file_bucket.id # S3 bucket

  cors_rule {
    allowed_methods = ["PUT", "POST", "GET"] #Allowed methods
    allowed_origins = ["*"]
    allowed_headers = ["*"]
    max_age_seconds = 3600
  }
}
