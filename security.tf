# Allow any connection to the ALB from outside using port 80
# Allow any outbound connection on all ports
resource "aws_security_group" "load_balancer" {
  name = "litedq-loadbalancer-security-group"
  vpc_id = aws_vpc.web_vpc.id

  ingress {
    protocol = "tcp"
    from_port = 80
    to_port = 80
    cidr_blocks = [ "0.0.0.0/0" ]
  }

  egress {
    protocol = "-1"
    from_port = 0
    to_port = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Allow only inbound connection comming from the load balancer
resource "aws_security_group" "ecs" {
  name = "litedq-ecs-security-group"
  vpc_id = aws_vpc.web_vpc.id

  ingress {
    protocol = "tcp"
    from_port = 80
    to_port = 80
    security_groups = [ aws_security_group.load_balancer.id ]
  }

  egress {
    protocol = "-1"
    from_port = 0
    to_port = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}