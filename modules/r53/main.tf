resource "aws_route53_record" "example" {
  name    = "app.veram.xyz"
  type    = "A"
  zone_id = "Z05097189KLSYOKJ54C8"

  alias {
    evaluate_target_health = true
    name                   = "d-5wdb5t39gc.execute-api.us-east-2.amazonaws.com"
    zone_id                = "ZOJJZC49E0EPZ"
  }
}