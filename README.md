This website allows users to upload files and instantly generate a unique shareable URL.  
You can send this link to anyone so they can download the file directly.

The application supports JPEG, PNG, and PDF files.  
Before uploading, it validates the file type and file size to ensure it meets the allowed criteria.

Uploaded files are stored securely in Amazon S3.  
File metadata such as filename and file type is stored in an Amazon RDS PostgreSQL database.

This project includes full Docker support for both the backend API and the PostgreSQL database.

Therefore this setup provides a fast, reliable, and scalable file sharing solution.

