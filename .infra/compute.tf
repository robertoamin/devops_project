resource "aws_ecr_repository" "ecr" {
  name                 = "${var.app_name}-ecr"
  image_tag_mutability = "MUTABLE"
  tags                 = var.tags
}


resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/${var.app_name}-service"
  retention_in_days = 5
}


resource "aws_security_group" "app_alb" {
  name        = "${var.app_name}-alb-sg"
  description = var.app_name
  vpc_id      = var.vpc_id

  ingress {
    description      = "ALB HTTP"
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    description      = "ALB HTTPS"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = var.tags
}

resource "aws_security_group" "app_service" {
  name        = "${var.app_name}-service-sg"
  description = var.app_name
  vpc_id      = var.vpc_id

  ingress {
    description      = "ALB HTTP"
    from_port        = var.container_port
    to_port          = var.container_port
    protocol         = "tcp"
    cidr_blocks      = local.subnet_cidr_blocks
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = var.tags
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecs-ecsTaskExecutionRole-${var.app_name}"
  tags = var.tags

  assume_role_policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
    "Effect": "Allow",
    "Principal": {
      "Service": "ecs-tasks.amazonaws.com"
    },
    "Action": "sts:AssumeRole"
  }
 ]
}
EOF
}


resource "aws_iam_role_policy" "ecs_cluster_ecstaskpolicy" {
  name   = "ecs-ecsTaskExecutionRole-ECSTaskPolicy-${var.app_name}"
  role   = aws_iam_role.ecs_task_execution_role.id
  policy = var.ecs_role_policy
}

resource "aws_iam_role_policy_attachment" "ecs-task-execution-role-policy-attachment" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_task_definition" "app" {
  family                   = "${var.app_name}-task"
  cpu                      = var.fargate_service_cpu
  memory                   = var.fargate_service_memory
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  tags                     = var.tags
  container_definitions    = <<EOF
  [
    {
      "name": "blacklist",
      "image": "273162695576.dkr.ecr.us-east-1.amazonaws.com/blacklist-ecr:develop-2023-11-19.19.05.38.a3b260fa",
      "networkMode": "awsvpc",
      "essential": true,
      "portMappings": [
        {
          "containerPort": ${var.container_port},
          "hostPort": ${var.container_port}
        }
      ],
      "environment": [
        {
          "name": "FLASK_DEBUG",
          "value": "1"
        },
        {
          "name": "APP_SETTINGS",
          "value": "blacklist.config.DevelopmentConfig"
        },
        {
          "name": "FLASK_APP",
          "value": "blacklist.app:create_app"
        },
        {
          "name": "JWT_SECRET_KEY",
          "value": "blacklist.app:create_app"
        },
        {
          "name": "POSTGRES_HOST",
          "value": "app.c6hjnftyyenf.us-east-1.rds.amazonaws.com"
        },
        {
          "name": "POSTGRES_PORT",
          "value": "5432"
        },
        {
          "name": "POSTGRES_DB",
          "value": "app"
        },
        {
          "name": "POSTGRES_USER",
          "value": "app"
        },
        {
          "name": "POSTGRES_PASSWORD",
          "value": "123asd456"
        }
      ],
      "healthCheck": {
        "command": [
          "CMD-SHELL",
          "curl -f http://localhost:5000/health || exit 1"
        ],
        "interval": 5,
        "timeout": 2,
        "retries": 3
      }
    }
  ]
  EOF
}

resource "aws_ecs_service" "app" {
  name            = "${var.app_name}-service"
  cluster         = var.fargate_cluster_name
  task_definition = aws_ecs_task_definition.app.arn
  desired_count          = var.fargate_service_min_capacity
  enable_execute_command = true
  platform_version       = "LATEST"

  network_configuration {
    subnets          = concat(var.subnets, var.private_subnets)
    security_groups  = concat([aws_security_group.app_service.id], var.fargate_service_security_groups)
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.app.arn
    container_name   = "blacklist"
    container_port   = var.container_port
  }

  deployment_controller {
    type = "CODE_DEPLOY"
  }

  capacity_provider_strategy {
    capacity_provider = "FARGATE_SPOT"
    weight            = 2
  }

  tags = var.tags

  lifecycle {
    ignore_changes = [
      task_definition,
      desired_count,
      capacity_provider_strategy,
      launch_type,
      load_balancer,
      platform_version,
      network_configuration
    ]
  }
}