locals {
  registry_id  = replace(data.aws_ecr_authorization_token.token.proxy_endpoint, "/^https?:///", "")
  dash_context = "${path.module}/docker"
  
  # Compute compound hash for each file in docker
  dash_hash    = sha1(join("", [for f in fileset(local.dash_context, "**") : filesha1("${local.dash_context}/${f}")]))
}

# Create ECR repo for dashboard image
resource "aws_ecr_repository" "dash" {
  name                 = "litedq/dash"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

// Build docker image and tag to latest
resource "docker_image" "dash_image" {
  name = "${local.registry_id}/${aws_ecr_repository.dash.name}:latest"
  build {
    context  = local.dash_context
    no_cache = true
  }

  triggers = {
    redeployment = local.dash_hash
  }
}

// Push to ECR
resource "docker_registry_image" "image_handler" {
  name = docker_image.dash_image.name

  triggers = {
    redeployment = local.dash_hash
  }
}
