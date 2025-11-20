resource "aws_db_instance" "postgres" {
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "15"
  instance_class         = "db.t3.micro" #Free tier eligible
  identifier             = var.db_identifier
  db_name                = var.db_name
  username               = var.db_user
  password               = var.db_password
  parameter_group_name   = "default.postgres15" 

  skip_final_snapshot    = true
  publicly_accessible    = true

  vpc_security_group_ids = [aws_security_group.db_sg.id] # Allow access from backend
}

resource "aws_security_group" "db_sg" {
  name        = "${var.db_identifier}-sg"
  description = "Allow backend to connect to Postgres"

  ingress {
    description = "Postgres access"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]   #Allow from anywhere
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
