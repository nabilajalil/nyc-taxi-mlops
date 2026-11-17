terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-3"
}

resource "aws_s3_bucket" "mlflow_artifacts" {
  bucket = "nyc-taxi-mlops-artifacts-263185198493-eu-west-3-an"

  lifecycle {
    prevent_destroy = true
  }
}
