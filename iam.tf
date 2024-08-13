data "aws_iam_policy_document" "glue_policy_document" {
    statement {
      actions = [ "sts:AssumeRole" ]
      principals {
        identifiers = [ "glue.amazonaws.com" ]
        type = "Service"
      }
    }
}

data "aws_iam_policy_document" "s3_policy_document" {
  statement {
    effect = "Allow"
    actions = [ "s3:*" ]
    resources = [ "*" ]
  }
}

resource "aws_iam_role" "glue_service_role" {
  name = "aws-glue-${var.job_name}-service-role"
  assume_role_policy = data.aws_iam_policy_document.glue_policy_document.json
}

// Attach service role policy
resource "aws_iam_role_policy_attachment" "glue_attachment" {
  role = aws_iam_role.glue_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"

}

resource "aws_iam_role_policy" "s3_attachment" {
  name = "s3-glue-all-access"
  policy = data.aws_iam_policy_document.s3_policy_document.json
  role = aws_iam_role.glue_service_role.id
}