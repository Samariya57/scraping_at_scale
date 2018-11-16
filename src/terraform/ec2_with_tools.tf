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
  connection {
  # The default username for our AMI
  user = "ubuntu"
  agent = "false"
  private_key = "${file(var.private_key_path)}"

  # The connection will use the local SSH agent for authentication.
  }
  provisioner "remote-exec" {
  inline = [
    "sudo apt-get install python-setuptools",
    "sudo apt-get install python-pip",
    "sudo pip install --upgrade pip",
    "sudo pip install PyHamcrest",
    "sudo pip install argparse",
    "sudo pip install BeautifulSoup4",
    "sudo pip install psycopg2",
    "sudo apt install git-all",
    "git clone https://github.com/Samariya57/yelp_updates.git",
    "cd yelp_updates",
    "git checkout develop",
    "python src/scraper/yelp_one_page_restaurant_reader.py"
    ]
  }
}
