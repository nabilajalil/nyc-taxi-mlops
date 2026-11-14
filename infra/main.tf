terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}
provider "aws" { region = var.aws_region }
variable "aws_region" { type = string; default = "eu-west-1" }
variable "ami_id" { type = string; description = "Ubuntu AMI ID for your region" }
variable "ssh_public_key" { type = string; description = "SSH public key text" }
variable "allowed_ssh_cidr" { type = string; description = "Your public IP/32" }
resource "aws_key_pair" "taxi" { key_name = "taxi-mlops-key"; public_key = var.ssh_public_key }
resource "aws_security_group" "taxi" {
  name_prefix = "taxi-mlops-"
  ingress { from_port = 22; to_port = 22; protocol = "tcp"; cidr_blocks = [var.allowed_ssh_cidr] }
  ingress { from_port = 8000; to_port = 8000; protocol = "tcp"; cidr_blocks = ["0.0.0.0/0"] }
  egress { from_port = 0; to_port = 0; protocol = "-1"; cidr_blocks = ["0.0.0.0/0"] }
}
resource "aws_instance" "taxi" {
  ami = var.ami_id
  instance_type = "t3.small"
  key_name = aws_key_pair.taxi.key_name
  vpc_security_group_ids = [aws_security_group.taxi.id]
  root_block_device { volume_size = 20 }
  tags = { Name = "nyc-taxi-mlops" }
}
output "public_ip" { value = aws_instance.taxi.public_ip }
