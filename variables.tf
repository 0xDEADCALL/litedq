// Glue Variables
variable "job_name" {
  type = string
}

variable "glue_version" {
  type    = string
  default = "4.0"
}

variable "worker_type" {
  type    = string
  default = "Standard"
}

variable "worker_number" {
  type    = number
  default = 1
}

variable "max_retries" {
  type    = string
  default = "0"
}

variable "timeout" {
  type    = number
  default = 2880
}

// S3 Variables
variable "code_repo_bucket" {
  type = string
}

 // Database Variables
variable "target_bucket" {
  type = string
}

variable "target_database" {
  type = string
}

variable "target_table" {
  type = string
}

variable "write_mode" {
  type = string
  default = "overwrite"
}

variable "dry_run" {
  type = bool
  default = false
}

// Trigger Variables
variable "trigger_schedule" {
  type     = string
  nullable = true
  default  = null
}

// DQ Variables
variable "code_path" {
  type = string
}
variable "questions_path" {
  type = string
}
