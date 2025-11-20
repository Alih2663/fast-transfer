variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "s3_bucket_name" {
  default = "fast-transfer-bucket-v2"  # Bucket name (- Change as needed - )
}

variable "db_identifier" {
  type        = string
  description = "RDS instance identifier"
}

variable "db_name" {
  type        = string
  description = "Database name"
}

variable "db_user" {
  type        = string
  description = "Postgres username"
}

variable "db_password" {
  type        = string
  description = "Postgres password"
  sensitive   = true
}
