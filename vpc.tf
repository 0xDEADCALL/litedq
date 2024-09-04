resource "aws_vpc" "web_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = var.vpc_name
  }
}

// We'll need a public subnet because the load balancer sits in it 
// and needs to be reachable from outside
resource "aws_subnet" "public_subnets" {
  count                   = length(var.public_subnets_cidrs)
  vpc_id                  = aws_vpc.web_vpc.id
  cidr_block              = element(var.public_subnets_cidrs, count.index)
  map_public_ip_on_launch = true
  availability_zone       = element(var.azs, count.index)

  tags = {
    Name = "${var.vpc_name}-public-subnet-${count.index}"
  }
}

resource "aws_subnet" "private_subnets" {
  count                   = length(var.private_subnets_cidrs)
  vpc_id                  = aws_vpc.web_vpc.id
  cidr_block              = element(var.private_subnets_cidrs, count.index)
  map_public_ip_on_launch = false
  availability_zone       = element(var.azs, count.index)

  tags = {
    Name = "${var.vpc_name}-private-subnet-${count.index}"
  }
}

// Gateways
// We need an internet gateway for the public subnets to access the internet
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.web_vpc.id

  tags = {
    Name = "${var.vpc_name}-igw"
  }
}

// We need a NAT gateway to allow outbound connections for private subnets
resource "aws_eip" "nat_eip" {
  depends_on = [aws_internet_gateway.igw]
}

resource "aws_nat_gateway" "ngw" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = element(aws_subnet.public_subnets.*.id, 0)
  depends_on    = [aws_internet_gateway.igw]

  tags = {
    Name = "${var.vpc_name}-nat"
  }
}

// Routing tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.web_vpc.id

  tags = {
    Name = "${var.vpc_name}-public-route-table"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.web_vpc.id

  tags = {
    Name = "${var.vpc_name}-private-route-table"
  }
}

// Routes
resource "aws_route" "route_public_igw" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_route" "route_private_nat" {
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.ngw.id
}

// Routes associations
// Link public subnets to internet
resource "aws_route_table_association" "public" {
  for_each       = { for k, v in aws_subnet.public_subnets : k => v }
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}

// Link outbound connections of private subnets to internet
resource "aws_route_table_association" "private" {
  for_each       = { for k, v in aws_subnet.private_subnets : k => v }
  subnet_id      = each.value.id
  route_table_id = aws_route_table.private.id
}

// Create S3 endpoint to avoid it getting through the 
// IGW
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.web_vpc.id
  service_name      = "com.amazonaws.eu-west-1.s3"
  route_table_ids   = [aws_route_table.private.id]
  vpc_endpoint_type = "Gateway"
  policy            = <<POLICY
    {
    "Version": "2008-10-17",
    "Statement": [
        {
        "Action": "*",
        "Effect": "Allow",
        "Resource": "*",
        "Principal": "*"
        }
    ]
    }
    POLICY

  tags = {
    Name = "${var.vpc_name}-s3-endpoint"
  }
}


