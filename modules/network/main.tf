#VPC
resource "aws_vpc" "demo" {
    cidr_block  = "10.0.0.0/16"
    tags        = {
        Name    = "vpc${var.main-name}"
        Terra   = "true"
    }
}


#internet gateway
resource "aws_internet_gateway" "demo" {
    vpc_id      = aws_vpc.demo.id
    tags        = {
        Name    = "gw${var.main-name}"
        Terra   = "true"
    }
}


#public routing table
resource "aws_route_table" "demopub" {
    vpc_id      = aws_vpc.demo.id
    tags        = {
        Name    = "pubRoute${var.main-name}"
        Terra   = "true"
    }
}
resource "aws_route" "demopub" {
    route_table_id          = aws_route_table.demopub.id
    destination_cidr_block  = "0.0.0.0/0"
    gateway_id              = aws_internet_gateway.demo.id
    depends_on              = [aws_internet_gateway.demo]
}


#private routing table
resource "aws_route_table" "demopriv" {
    vpc_id      = aws_vpc.demo.id
    depends_on  = [aws_internet_gateway.demo]
    tags        = {
        Name    = "privRoute${var.main-name}"
        Terra   = "true"
    }
}


#AZ in region
data "aws_availability_zones" "available" {}


#public subnets
resource "aws_subnet" "demopub" {
    vpc_id              = aws_vpc.demo.id
    count               = "${length(data.aws_availability_zones.available.names)}"
    cidr_block          = "10.0.${0+count.index}.0/24"
    availability_zone   = "${data.aws_availability_zones.available.names[count.index]}"
    tags                = {
        Name            = "pub${var.main-name}${data.aws_availability_zones.available.names[count.index]}"
        Terra           = "true"
    }
}
resource "aws_route_table_association" "demopub" {
    count           = "${length(data.aws_availability_zones.available.names)}"
    subnet_id       = "${aws_subnet.demopub[count.index].id}"
    route_table_id  = aws_route_table.demopub.id
}


#private subnets
resource "aws_subnet" "demopriv" {
    vpc_id              = aws_vpc.demo.id
    count               = "${length(data.aws_availability_zones.available.names)}"
    cidr_block          = "10.0.${length(data.aws_availability_zones.available.names)+count.index}.0/24"
    availability_zone   = "${data.aws_availability_zones.available.names[count.index]}"
    tags                = {
        Name            = "priv${var.main-name}${data.aws_availability_zones.available.names[count.index]}"
        Terra           = "true"
    }
}
resource "aws_route_table_association" "demopriv" {
    count           = "${length(data.aws_availability_zones.available.names)}"
    subnet_id       = "${aws_subnet.demopriv[count.index].id}"
    route_table_id  = aws_route_table.demopriv.id
}


resource "aws_security_group" "demodef" {
  name        = "demodef"
  description = "Allow TLS inbound traffic"
  vpc_id      = aws_vpc.demo.id

  ingress {
    description      = "TLS from VPC"
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow_tls"
  }
}