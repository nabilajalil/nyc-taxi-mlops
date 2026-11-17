resource "aws_instance" "taxi_server" {
  ami           = "ami-0c2d516f60d275525"
  instance_type = "t3.small"

  key_name = "nyc-taxi-ec2-key"

  subnet_id = "subnet-0ca5a30f0e2052a55"

  vpc_security_group_ids = [
    "sg-044ecb96e3c7031bf"
  ]

  tags = {
    Name = "nyc-taxi-mlops-server"
  }

  lifecycle {
    prevent_destroy = true
  }
}
