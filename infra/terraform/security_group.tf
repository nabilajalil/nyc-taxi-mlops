resource "aws_security_group" "taxi_server" {
  name        = "launch-wizard-1"
  description = "launch-wizard-1 created 2026-11-15T10:18:18.930Z"
  vpc_id      = "vpc-0ab064b61dfc619b0"

  ingress {
    description = ""
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["88.183.108.221/32"]
    ipv6_cidr_blocks = [
      "2a01:e0a:ddb:3740:d5ab:2399:69aa:a68a/128"
    ]
  }

  egress {
    description = ""
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    prevent_destroy = true
  }
}
