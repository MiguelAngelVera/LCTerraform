data "archive_file" "app" {
    type        = "zip"
    source_dir  = "${path.module}/../../app"
    output_path = "${path.module}/../../code-api.zip"
}

resource "aws_s3_bucket" "demobucket" {
    bucket          = "bucket-vera-demo"
    acl             = "private"
    versioning {
      enabled       = true
    }
    server_side_encryption_configuration {
        rule {
            apply_server_side_encryption_by_default {
                sse_algorithm   = "AES256"
            }
        }
    }
    tags = {
        Name        = "bucket${var.main-name}"
        Terra       = "true"
    }
}


resource "aws_s3_bucket_object" "demoobject" {
    bucket  = aws_s3_bucket.demobucket.id
    key     = "app-demo.zip"
    source  = data.archive_file.app.output_path
}