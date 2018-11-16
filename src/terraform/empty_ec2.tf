provider "aws" {
  access_key = ""
  secret_key = ""
  region     = "us-east-1"
}

resource "aws_instance" "example" {
  ami                     = "ami-2757f631"
  instance_type           = "t2.micro"
  vpc_security_group_ids  = [""]
  key_name                = "postgres_prep"
  subnet_id               = "subnet-35a16a7d"
  tags {
     Name = "Yelp_scraper"
  }
}
