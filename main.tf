terraform {
    required_providers {
      aws = {
          source = "hashicorp/aws"
          version = "~> 3.0"
      }
    }
}

provider "aws" {
    profile = "default"
    region = var.region
}

module "vpc" {
    source = "./modules/network"
    main-name = var.main-name
}


module "s3" {
    source = "./modules/S3"
    main-name = var.main-name
}

module "roles" {
    source = "./modules/roles"
    
}


module "lambda" {
    source          = "./modules/lambda"
    main-name       = var.main-name
    bucket          = module.s3.bucket
    object_key      = module.s3.object_key
    hash            = module.s3.file_hash
    role            = module.roles.lambda_rol
    region          = var.region
    priv_subnets    = module.vpc.priv_subnets
    sec_groups      = module.vpc.sec_groups
}


module "r53" {
    source = "./modules/r53"
}

module "rds" {
    source          = "./modules/rds"
    priv_subnets    = module.vpc.priv_subnets
    sec_groups      = module.vpc.sec_groups
}
# module "vpc" {
#   source = "terraform-aws-modules/vpc/aws"

#   name = "my-vpc"
#   cidr = "10.0.0.0/16"

#   azs             = ["us-east-2a", "us-east-2b", "us-east-2c"]
#   private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
#   public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

#   #enable_nat_gateway = true
#   #enable_vpn_gateway = true

#   tags = {
#     Terraform = "true"
#     Environment = "dev"
#   }
# }