output "bucket" {
    value = aws_s3_bucket.demobucket.id
}

output "object_key" {
    value = aws_s3_bucket_object.demoobject.key
}

output "file_hash" {
    value = data.archive_file.app.output_base64sha256
}