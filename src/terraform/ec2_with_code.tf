provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region     = "${var.region}"
}

resource "aws_instance" "scraper" {
  ami                    = "ami-2757f631"
  instance_type          = "t2.micro"
  vpc_security_group_ids = ["${var.security_group}"]
  key_name               = "postgres_prep"
  subnet_id              = "${var.subnet}"

  tags {
    Name = "yelp_scraper"
  }

  connection {
  	user = "ubuntu"
  	agent = "false"
  	private_key = "${file("~/.ssh/postgres_prep.pem")}"
  	# The connection will use the local SSH agent for authentication.
  }

  provisioner "file" {
    source      = "~/.bash_profile"
    destination = "~/.env"
  }

  provisioner "remote-exec" {
     inline = [
      	"sleep 30",
      	"sudo apt-get update -y",
      	"sudo apt-get install python2 -y",
      	"sudo apt-get install python-setuptools -y",
      	"sudo apt-get install python-pip -y",
      	"sudo pip install --upgrade pip",
      	"sudo pip install PyHamcrest",
      	"sudo pip install argparse",
      	"sudo pip install BeautifulSoup4",
      	"sudo pip install psycopg2",
      	"sudo pip install requests",
      	"sudo apt-get install python-lxml -y",
      	"git clone https://github.com/Samariya57/scraping_at_scale.git",
      	"cd scraping_at_scale",
      	". ~/.env",
      	"python src/scraper/yelp_one_page_restaurant_reader.py"
     ]
  }
}

output "ip" {
  value = "${aws_instance.scraper.public_ip}"
}
