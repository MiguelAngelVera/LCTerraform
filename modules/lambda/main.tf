#user info
data "aws_caller_identity" "current" {
  
}


#create api gw
resource "aws_api_gateway_rest_api" "demoapi" {
    name = "api-${var.main-name}"
}


#create resources for api gw
resource "aws_api_gateway_resource" "health" {
    parent_id   = aws_api_gateway_rest_api.demoapi.root_resource_id
    path_part   = "health"
    rest_api_id = aws_api_gateway_rest_api.demoapi.id
}
resource "aws_api_gateway_resource" "login" {
    parent_id   = aws_api_gateway_rest_api.demoapi.root_resource_id
    path_part   = "login"
    rest_api_id = aws_api_gateway_rest_api.demoapi.id
}


#create methods for each resource
resource "aws_api_gateway_method" "health" {
    authorization   = "NONE"
    http_method     = "GET"
    resource_id     = aws_api_gateway_resource.health.id
    rest_api_id     = aws_api_gateway_rest_api.demoapi.id
}
resource "aws_api_gateway_method" "login" {
    authorization   = "NONE"
    http_method     = "POST"
    resource_id     = aws_api_gateway_resource.login.id
    rest_api_id     = aws_api_gateway_rest_api.demoapi.id
}


#integrations
resource "aws_api_gateway_integration" "health" {
    http_method             = aws_api_gateway_method.health.http_method
    resource_id             = aws_api_gateway_resource.health.id
    rest_api_id             = aws_api_gateway_rest_api.demoapi.id
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = aws_lambda_function.health.invoke_arn
}
resource "aws_api_gateway_integration" "login" {
    http_method             = aws_api_gateway_method.login.http_method
    resource_id             = aws_api_gateway_resource.login.id
    rest_api_id             = aws_api_gateway_rest_api.demoapi.id
    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = aws_lambda_function.login.invoke_arn
}


#allow invoke lambdas
resource "aws_lambda_permission" "health" {
    statement_id    = "AllowExecutionFromAPIGateway"
    action          = "lambda:InvokeFunction"
    function_name   = aws_lambda_function.health.function_name
    principal       = "apigateway.amazonaws.com"
    source_arn      = "arn:aws:execute-api:${var.region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.demoapi.id}/*/${aws_api_gateway_method.health.http_method}${aws_api_gateway_resource.health.path}"

}
resource "aws_lambda_permission" "login" {
    statement_id    = "AllowExecutionFromAPIGateway"
    action          = "lambda:InvokeFunction"
    function_name   = aws_lambda_function.login.function_name
    principal       = "apigateway.amazonaws.com"
    source_arn      = "arn:aws:execute-api:${var.region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.demoapi.id}/*/${aws_api_gateway_method.login.http_method}${aws_api_gateway_resource.login.path}"

}
#798699972204


#deploy api
resource "aws_api_gateway_deployment" "demodeploy" {
    rest_api_id = aws_api_gateway_rest_api.demoapi.id
    triggers    = {
        redeployment = sha1(jsonencode([
            aws_api_gateway_method.health.id,
            aws_api_gateway_integration.health.id,
            aws_api_gateway_method.login.id,
            aws_api_gateway_integration.login.id
        ]))
    }
    lifecycle {
      create_before_destroy = true
    }
}

#production stage
resource "aws_api_gateway_stage" "demoprod" {
    deployment_id   = aws_api_gateway_deployment.demodeploy.id
    rest_api_id     = aws_api_gateway_rest_api.demoapi.id
    stage_name      = "prod"
}

#lambda function
resource "aws_lambda_function" "health" {
    function_name   = "health"
    s3_bucket       = var.bucket
    s3_key          = var.object_key
    runtime = "python3.8"
    handler = "app.app"
    source_code_hash = var.hash
    role = var.role
}

#lambda function
resource "aws_lambda_function" "login" {
    function_name   = "login"
    s3_bucket       = var.bucket
    s3_key          = var.object_key
    runtime = "python3.8"
    handler = "app.app"
    source_code_hash = var.hash
    role = var.role
    vpc_config {
        #count               = "${length(var.priv_subnets)}"
        subnet_ids          = var.priv_subnets
        security_group_ids  = [var.sec_groups]
}
}

resource "aws_api_gateway_base_path_mapping" "example" {
  api_id      = aws_api_gateway_rest_api.demoapi.id
  stage_name  = aws_api_gateway_stage.demoprod.stage_name
  domain_name = "app.veram.xyz"
}