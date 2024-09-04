terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "5.65.0"
    }
  }
}
// Data
// Used to retrieve ECR credential for pushing images
data "aws_ecr_authorization_token" "token" {}


// Configuire AWS provider
provider "aws" {
  region = "eu-west-1"
}

// Configure Docker provider
provider "docker" {
  registry_auth {
    address  = data.aws_ecr_authorization_token.token.proxy_endpoint
    username = data.aws_ecr_authorization_token.token.user_name
    password = data.aws_ecr_authorization_token.token.password
  }
}
