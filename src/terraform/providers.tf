# Create a new instance of the latest Ubuntu 14.04 on an
# t2.micro node with an AWS Tag naming it "Yelp_scraper"
provider "aws" {
  region = "us-east-1"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "web" {
  ami           = "${data.aws_ami.ubuntu.id}"
  instance_type = "t2.medium"
  vpc_security_group_ids = ['vpc-6baf940d']
  key_name = 'postgres_prep'
  subnet_id = 'subnet-35a16a7d'
  security_groups = ['launch-wizard-6']
  tags {
    Name = "Yelp_scraper"
  }
}
