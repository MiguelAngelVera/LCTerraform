#role for lambda
resource "aws_iam_role" "roledemo" {
    name                = "lambdarol" 
    assume_role_policy    = jsonencode({
        Version     = "2012-10-17"
        Statement   = [{
            Action    = "sts:AssumeRole"
            Effect    = "Allow"
            Sid       = ""
            Principal = {
                Service = "lambda.amazonaws.com"
            }
        }
        ]
    })
}

#add required managed policy to lambda role
resource "aws_iam_role_policy_attachment" "policydemo" {
    role        = aws_iam_role.roledemo.name
    policy_arn  = "arn:aws:iam::aws:policy/AWSLambdaExecute"
}

resource "aws_iam_role_policy_attachment" "policydemo2" {
    role        = aws_iam_role.roledemo.name
    policy_arn  = "arn:aws:iam::aws:policy/service-role/AWSLambdaENIManagementAccess"
}