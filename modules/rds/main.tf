data "aws_db_snapshot" "demosnap" {
    most_recent = true
    db_instance_identifier = "database-1"
}


# Create new staging DB
resource "aws_db_instance" "demodb" {
  instance_class       = "db.t2.micro"
  identifier           = "database-1"
  username             = "admin"
  password             = "N0semeolvida987"
  db_subnet_group_name = aws_db_subnet_group.demogroup.name
  snapshot_identifier  = "${data.aws_db_snapshot.demosnap.id}"
  vpc_security_group_ids = [var.sec_groups]
  skip_final_snapshot = true
}


resource "aws_db_subnet_group" "demogroup" {
  name       = "secdemo"
  subnet_ids = var.priv_subnets

  tags = {
    Name = "My DB subnet group"
  }
}