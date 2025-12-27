This website allows users to upload files and instantly generate a unique shareable URL.  
You can send this link to anyone so they can download the file directly.

Infrastructure is fully managed using **Terraform**, which automatically provisions **Amazon S3**, **Amazon RDS**, **IAM roles**, and all required cloud resources.
The application logic runs on a dedicated **AWS EC2 instance** and configuration and application deployment are **fully automated using Ansible**.
**GitHub Actions** handles the **deployment process**, automatically updating the live server whenever new code is pushed, **eliminating the need for manual changes**

The project supports JPEG, PNG, and PDF files.  
Before uploading, it validates the file type and file size to ensure it meets the allowed criteria.

Downloads utilize **AWS S3 Presigned URLs** for secure, direct file access.

File metadata such as filename and file type is stored in an **Amazon RDS PostgreSQL database**.

This project includes **full Docker support** for both the backend API and the PostgreSQL database.
Therefore this setup provides a fast, reliable, and scalable file sharing solution..
