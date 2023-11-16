resource "aws_security_group" "rds_security_group" {
  name   = "${var.app_name}-rds-sg"
  vpc_id = var.vpc_id

  ingress {
    description = "Access to RDS Port"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_subnet_group" "default" {
  name       = lower("${var.app_name}-${var.environment}")
  subnet_ids = var.private_subnets
}

module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "5.6.0"

  identifier = lower("${var.app_name}-rds-${var.environment}")

  create_db_option_group    = false
  create_db_parameter_group = false

  engine               = "postgres"
  engine_version       = "13"
  family               = "postgres13" # DB parameter group
  major_engine_version = "13"         # DB option group
  instance_class       = var.rds_instance_class

  allocated_storage      = var.rds_storage
  username               = var.rds_username
  password               = var.rds_password
  create_random_password = false
  port                   = 5432

  db_subnet_group_name    = aws_db_subnet_group.default.name
  vpc_security_group_ids = [join("", aws_security_group.rds_security_group.*.id)]

  maintenance_window = "Sun:00:00-Sun:03:00"
  backup_window      = "03:00-06:00"

  backup_retention_period = 7

  publicly_accessible = var.rds_publicly_accessible
}