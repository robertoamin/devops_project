resource "aws_lb" "app" {
  name               = "${var.app_name}-alb"
  internal           = var.alb_internal
  security_groups    = [aws_security_group.app_alb.id]
  load_balancer_type = "application"

  subnets = var.subnets

  enable_deletion_protection = false
  tags = merge(var.tags, {
    ecs_service = var.app_name
  })
}

resource "aws_alb_target_group" "app" {
  name                 = "${var.app_name}-target-group"
  port                 = var.container_port
  protocol             = "HTTP"
  target_type          = "ip"
  vpc_id               = var.vpc_id
  deregistration_delay = var.deregistration_delay

  health_check {
    path                = var.health_check_endpoint
    protocol            = "HTTP"
    interval            = 30
    timeout             = 20
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }

  tags = var.tags
}

resource "aws_lb_target_group" "app_two" {
  name        = "${var.app_name}-target2-group"
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path                = var.health_check_endpoint
    protocol            = "HTTP"
    interval            = 30
    timeout             = 20
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }
}

resource "aws_alb_listener" "http_local" {
  load_balancer_arn = aws_lb.app.id
  port              = 80
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_alb_target_group.app.id
    type             = "forward"
  }

  lifecycle {
    ignore_changes = [default_action]
  }
}