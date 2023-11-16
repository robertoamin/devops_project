variable "app_name" {
  type        = string
  description = "The name of the application."
  default = "blacklist"
}

variable "vpc_id" {
  type        = string
  description = "The ID of the VPC where the resources will be created."
}

variable "private_subnets" {
  default     = []
  type        = list(string)
  description = "A list of private subnets where the resources will be created."
}

variable "fargate_service_cpu" {
  type        = number
  default     = 1024
  description = "The number of CPU units for the Fargate service."
}

variable "health_check_endpoint" {
  default = "/health"
  type = string
}

variable "fargate_service_min_capacity" {
  type        = number
  default     = 1
  description = "The minimum number of tasks to run for the Fargate service."
}

variable "rds_username" {
  type        = string
  default     = "postgres"
  description = "The username for the RDS instance."
}

variable "rds_password" {
  type        = string
  description = "The password for the RDS instance."
  sensitive   = true
}

variable "rds_publicly_accessible" {
  type        = bool
  default     = false
  description = "Whether the RDS instance should be publicly accessible."
}

variable "fargate_service_max_capacity" {
  type        = number
  default     = 4
  description = "The maximum number of tasks to run for the Fargate service."
}

variable "subnets" {
  type        = list(string)
  description = "A list of subnets where the resources will be created."
}

variable "fargate_service_memory" {
  type        = number
  default     = 2048
  description = "The amount of memory for the Fargate service."
}

variable "fargate_scale_when_memory_utilization" {
  type        = number
  default     = 80
  description = "The memory utilization threshold at which to scale up the Fargate service."
}

variable "fargate_scale_when_cpu_utilization" {
  type        = number
  default     = 60
  description = "The CPU utilization threshold at which to scale up the Fargate service."
}

variable "tags" {
  default     = {}
  description = "A map of tags for the resources."
}

variable "fargate_cluster_name" {
  type        = string
  default     = "blacklist-fargate-cluster"
  description = "The name of the Fargate cluster."
}

variable "rds_instance_class" {
  type        = string
  default     = "db.t3.micro"
  description = "The instance class for the RDS instance."
}

variable "rds_storage" {
  type    = number
  default = 20
}

variable "alb_internal" {
  type        = bool
  default     = false
  description = "Whether the ALB is internal."
}

variable "container_port" {
  type        = number
  description = "The port number for the container."
  default = 5000
}

variable "ecs_role_policy" {
  type        = string
  default     = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "logs:CreateLogStream",
        "logs:CreateLogGroup",
        "logs:PutLogEvents",
        "s3:*",
        "ssmmessages:CreateControlChannel",
        "ssmmessages:CreateDataChannel",
        "ssmmessages:OpenControlChannel",
        "ssmmessages:OpenDataChannel"
        ],
      "Resource": "*"
    }
  ]
}
  EOF
  description = "The IAM policy for the ECS role."
}

variable "fargate_service_security_groups" {
  type        = list(string)
  default     = []
  description = "A list of security groups for the Fargate service."
}

variable "deregistration_delay" {
  description = "The amount of time for the load balancer to wait before deregistering a target (in seconds)"
  type        = number
  default     = 30
}

variable "environment" {
  type = string
  default = "dev"
}

variable "aws_region" {
  type      = string
  default = "us-east-1"
}

variable "aws_access_key" {
  type      = string
  sensitive = true
}

variable "aws_secret_key" {
  type      = string
  sensitive = true
}