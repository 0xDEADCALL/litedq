resource "aws_cloudwatch_log_group" "litedq_log_group" {
  name = "/ecs/litedq-dash"
  retention_in_days = 5

  tags = {
    Name = "litedq-dash-log-group"
  }
}

resource "aws_cloudwatch_log_stream" "litedq_log_stream" {
  name = "litedq-dash-log-stream"
  log_group_name = aws_cloudwatch_log_group.litedq_log_group.name
}