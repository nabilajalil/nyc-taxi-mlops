data "aws_iam_policy_document" "github_ssm_deploy" {
  statement {
    sid    = "SendCommandsToTaxiInstance"
    effect = "Allow"

    actions = [
      "ssm:SendCommand"
    ]

    resources = [
      aws_instance.taxi_server.arn,
      "arn:aws:ssm:eu-west-3::document/AWS-RunShellScript"
    ]
  }

  statement {
    sid    = "ReadDeploymentCommandResults"
    effect = "Allow"

    actions = [
      "ssm:GetCommandInvocation",
      "ssm:ListCommandInvocations"
    ]

    resources = ["*"]
  }

  statement {
    sid    = "DescribeTaxiInstance"
    effect = "Allow"

    actions = [
      "ec2:DescribeInstances",
      "ssm:DescribeInstanceInformation"
    ]

    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "github_ssm_deploy" {
  name   = "nyc-taxi-ssm-deploy"
  role   = aws_iam_role.github_deploy.id
  policy = data.aws_iam_policy_document.github_ssm_deploy.json
}
