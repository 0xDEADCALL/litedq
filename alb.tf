resource "aws_alb" "alb" {
  name            = "litedq-load-balancer"
  subnets         = aws_subnet.public_subnets.*.id
  security_groups = [aws_security_group.load_balancer.id]
}

resource "aws_alb_target_group" "group" {
  name        = "litedq-target-group"
  port        = var.dash_port
  protocol    = "HTTP"
  vpc_id      = aws_vpc.web_vpc.id
  target_type = "ip"
}

resource "aws_alb_listener" "frontend" {
  load_balancer_arn = aws_alb.alb.arn
  port              = var.dash_port
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_alb_target_group.group.arn
    type             = "forward"
  }
}
