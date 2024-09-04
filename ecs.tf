// Create ECS cluster
resource "aws_ecs_cluster" "cluster" {
  name = "litedq-dash-cluster"
}


// Link capacity providers (use fargate)
resource "aws_ecs_cluster_capacity_providers" "cap_providers" {
  cluster_name       = aws_ecs_cluster.cluster.name
  capacity_providers = ["FARGATE"]
}

// Create task definition
resource "aws_ecs_task_definition" "litedq_task" {
  family                   = "litedq-dash-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.dash_cpu
  memory                   = var.dash_memory
  execution_role_arn       = aws_iam_role.ecs_exec_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  container_definitions = jsonencode([
    {
      name  = "litedq-dash"
      image = docker_registry_image.image_handler.name
      cpu   = 0
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/litedq-dash"
          awslogs-region        = "eu-west-1"
          awslogs-stream-prefix = "ecs"
        }
      }
      portMappings = [{
        containerPort = var.dash_port
        hostPort      = var.dash_port
      }]
    }
  ])
}

// Create ECS service
resource "aws_ecs_service" "litedq_dash_service" {
  name                 = "litedq-dash-service"
  cluster              = aws_ecs_cluster.cluster.id
  task_definition      = aws_ecs_task_definition.litedq_task.arn
  desired_count        = var.dash_service_count
  launch_type          = "FARGATE"
  force_new_deployment = true

  triggers = {
    redeployment = local.dash_hash
  }

  network_configuration {
    security_groups  = [aws_security_group.ecs.id]
    subnets          = aws_subnet.private_subnets.*.id
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.group.id
    container_name   = "litedq-dash"
    container_port   = var.dash_port
  }

  depends_on = [ docker_registry_image.image_handler ]
}
