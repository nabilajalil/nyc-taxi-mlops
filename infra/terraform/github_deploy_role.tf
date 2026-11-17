data "aws_iam_policy_document" "github_deploy_trust" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRoleWithWebIdentity"
    ]

    principals {
      type = "Federated"

      identifiers = [
        aws_iam_openid_connect_provider.github.arn
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"

      values = [
        "sts.amazonaws.com"
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"

      values = [
        "repo:nabilajalil@186692670/nyc-taxi-mlops@1458411181:ref:refs/heads/main"
      ]
    }
  }
}

resource "aws_iam_role" "github_deploy" {
  name               = "nyc-taxi-github-deploy"
  assume_role_policy = data.aws_iam_policy_document.github_deploy_trust.json

  tags = {
    Project   = "nyc-taxi-mlops"
    ManagedBy = "Terraform"
  }
}
