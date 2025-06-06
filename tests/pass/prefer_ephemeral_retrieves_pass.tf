# Using a data source that doesn't have an ephemeral alternative - this should PASS
data "aws_ami" "example" {
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Using another data source that doesn't have an ephemeral alternative - this should PASS
data "aws_availability_zones" "available" {
  state = "available"
}
