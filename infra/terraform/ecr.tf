resource "aws_ecr_repository" "taxi_api" {
  name                 = "nyc-taxi-mlops"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Project   = "nyc-taxi-mlops"
    ManagedBy = "Terraform"
  }
}

resource "aws_ecr_lifecycle_policy" "taxi_api" {
  repository = aws_ecr_repository.taxi_api.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep only the 5 most recent images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 5
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}
