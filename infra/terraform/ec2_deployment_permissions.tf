data "aws_iam_role" "taxi_ec2" {
  name = "NYCTaxiEC2S3ReadOnlyRole"
}

resource "aws_iam_role_policy_attachment" "ec2_ssm" {
  role       = data.aws_iam_role.taxi_ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy_attachment" "ec2_ecr_readonly" {
  role       = data.aws_iam_role.taxi_ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}
