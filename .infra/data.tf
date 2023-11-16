data "aws_vpc" "default" {
  id = var.vpc_id
}

data "aws_subnet_ids" "default" {
  vpc_id = var.vpc_id
}

data "aws_subnet" "default" {
  for_each = data.aws_subnet_ids.default.ids

  id = each.value
}

locals {
  subnet_cidr_blocks = [for subnet in data.aws_subnet.default : subnet.cidr_block]
}