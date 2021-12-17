output "priv_subnets" {
    value = "${aws_subnet.demopriv[*].id}"
}

output "sec_groups" {
    value = "${aws_security_group.demodef.id}"
}