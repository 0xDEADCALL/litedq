// Assume policies
data "aws_iam_policy_document" "glue_assume_policy_document" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["glue.amazonaws.com"]
      type        = "Service"
    }
  }
}

data "aws_iam_policy_document" "ecs_assume_policy_document" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["ecs-tasks.amazonaws.com"]
      type        = "Service"
    }
  }
}

// Allow all S3 actions on the target bucket only
data "aws_iam_policy_document" "s3_all_glue" {
  statement {
    effect    = "Allow"
    actions   = ["s3:*"]
    resources = ["arn:aws:s3:::${var.target_bucket}/*"]
  }
}

data "aws_iam_policy_document" "s3_read_ecs" {
  statement {
    effect    = "Allow"
    actions   = [
      "s3:Get*",
      "s3:List*",
      "s3:Describe*",
      "s3-object-lambda:Get*",
      "s3-object-lambda:List*"
    
    ]
    resources = ["arn:aws:s3:::${var.target_bucket}/*"]
  }
}

resource "aws_iam_role" "glue_service_role" {
  name               = "aws-glue-${var.job_name}-service-role"
  assume_role_policy = data.aws_iam_policy_document.glue_assume_policy_document.json
}

resource "aws_iam_role" "ecs_task_role" {
  name               = "litedq-dash-ecs-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume_policy_document.json
}

resource "aws_iam_role" "ecs_exec_role" {
  name               = "litedq-dash-ecs-exec-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume_policy_document.json
}

// Attach service role policy
resource "aws_iam_role_policy_attachment" "glue_attachment" {
  role       = aws_iam_role.glue_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

// Attach read ALL to Glue role
resource "aws_iam_role_policy_attachment" "attach_s3_read_all_to_glue" {
  role       = aws_iam_role.glue_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

// Attach ALL actions to target bucket
resource "aws_iam_role_policy" "attach_s3_to_glue" {
  name   = "s3-all-logger-bucket"
  policy = data.aws_iam_policy_document.s3_all_glue.json
  role   = aws_iam_role.glue_service_role.id
}



resource "aws_iam_role_policy_attachment" "ecs_athena_task_attachment" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonAthenaFullAccess"
}

resource "aws_iam_role_policy" "s3_attachment" {
  name   = "s3-read-logger-bucket"
  policy = data.aws_iam_policy_document.s3_read_ecs.json
  role   = aws_iam_role.ecs_task_role.name
}

resource "aws_iam_role_policy_attachment" "ecs_exec_attachment" {
  role       = aws_iam_role.ecs_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
