data "aws_iam_policy_document" "github_ecr_push" {
  statement {
    sid    = "GetECRAuthorizationToken"
    effect = "Allow"

    actions = [
      "ecr:GetAuthorizationToken"
    ]

    resources = ["*"]
  }

  statement {
    sid    = "PushImagesToTaxiRepository"
    effect = "Allow"

    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:CompleteLayerUpload",
      "ecr:InitiateLayerUpload",
      "ecr:PutImage",
      "ecr:UploadLayerPart",
      "ecr:BatchGetImage"
    ]

    resources = [
      aws_ecr_repository.taxi_api.arn
    ]
  }
}

resource "aws_iam_role_policy" "github_ecr_push" {
  name   = "nyc-taxi-ecr-push"
  role   = aws_iam_role.github_deploy.id
  policy = data.aws_iam_policy_document.github_ecr_push.json
}
