locals {
  packages_list = formatlist("s3://${var.code_repo_bucket}/%s", [for k, x in aws_s3_object.extra_packages : x.key])
}

resource "aws_glue_job" "data_logger_glue" {
  name              = var.job_name
  role_arn          = aws_iam_role.glue_service_role.arn
  glue_version      = var.glue_version
  number_of_workers = var.worker_number
  worker_type       = var.worker_type
  max_retries       = var.max_retries
  timeout           = var.timeout

  command {
    name            = "glueetl"
    script_location = "s3://${var.code_repo_bucket}/${aws_s3_object.entry_point_script.key}"
  }

  default_arguments = {
    "--additional-python-modules" = join(",", local.packages_list)
    "--extra-py-files"            = "s3://${var.code_repo_bucket}/${aws_s3_object.extra_py_files.key}"
    "--target_table"              = var.target_table
    "--target_database"           = var.target_database
    "--target_bucket"             = var.target_bucket
    "--write_mode"                = var.write_mode
    "--dry_run"                   = var.dry_run
    "--enable-glue-datacatalog"   = ""
    "--conf"                      = "spark.sql.legacy.allowNonEmptyLocationInCTAS=true"
  }
}

resource "aws_glue_trigger" "data_logger_trigger" {
  count = var.job_schedule == null ? 0 : 1 
  name = "${var.job_name}-trigger-schedule"
  schedule = var.job_schedule
  type = "SCHEDULED"

  actions {
    job_name = aws_glue_job.data_logger_glue.name
  }
}
