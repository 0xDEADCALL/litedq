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

variable "job_schedule" {
  type = string
  nullable = true
  default = null
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

// VPC Variables
variable "vpc_name" {
  type = string
}
variable "vpc_cidr" {
  default = "10.0.0.0/26"
}

variable "public_subnets_cidrs" {
  type = list(string)
  default = [ "10.0.0.0/28", "10.0.0.16/28"]
}

variable "private_subnets_cidrs" {  
  type = list(string)
  default = [ "10.0.0.32/28", "10.0.0.48/28" ]
}

variable "azs" {
  type = list(string)
  default = [ "eu-west-1a", "eu-west-1b"]
}

// Variables for litedq-dash
variable "dash_port" {
  type = number
  default = 80
}

variable "dash_cpu" {
  type = number
  default = 256
}

variable "dash_memory" {
  type = number
  default = 512
}

variable "dash_service_count" {
  type = number
  default = 1
}
