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

variable "ssh_public_key_path" {
  description = "Path to your public SSH key"
  type        = string
  default     = "id_rsa.pub"  #Public key
}

variable "ssh_allowed_cidr" {
  description = "CIDR allowed to SSH into the EC2"
  type        = string
  default     = "0.0.0.0/0" # SSH access from anywhere
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro" # Free Tier 
}