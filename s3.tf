// Build dependency structure
data "external" "build_resources" {
  program = [
    "bash", 
    "./${path.module}/scripts/build_deps.sh",
    "${var.questions_path}",
    "${var.code_path}"
  ]
}

// Check if repo bucket exists,if not create it
data aws_s3_bucket "existing_repo_bucket" {
  bucket = var.code_repo_bucket
}

resource "aws_s3_bucket" "code_repo_bucket" {
  count = length(data.aws_s3_bucket.existing_repo_bucket.id) == 0 ? 1 : 0
}

// Check if repo bucket exists,if not create it
data "aws_s3_bucket" "existing_target_bucket" {
  bucket = var.target_bucket
}

resource "aws_s3_bucket" "target_bucket" {
  count = length(data.aws_s3_bucket.existing_target_bucket) == 0 ? 1 : 0
}

// Upload resorces
resource "aws_s3_object" "entry_point_script" {
  depends_on = [data.external.build_resources]
  bucket = var.code_repo_bucket
  key    = "assets/litedq/entrypoint.py"
  source = "${path.module}/src/entrypoint.py"
  etag   = filemd5("${path.module}/src/entrypoint.py")
}

resource "aws_s3_object" "extra_py_files" {
  depends_on = [data.external.build_resources]
  bucket = var.code_repo_bucket
  key    = "assets/litedq/extra_py_files.zip"
  source = "${path.module}/artifacts/extra_py_files.zip"
  etag   = data.external.build_resources.result.hash
}

resource "aws_s3_object" "extra_packages" {
  depends_on = [data.external.build_resources]
  for_each = fileset("${path.module}/artifacts/extra_packages/", "*")

  bucket = var.code_repo_bucket
  key    = "assets/litedq/packages/${each.value}"
  source = "${path.module}/artifacts/extra_packages/${each.value}"
  etag   = filemd5("${path.module}/artifacts/extra_packages/${each.value}")
}
