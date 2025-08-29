# Using a resource that doesn't have an ephemeral alternative - this should PASS
resource "aws_s3_bucket" "example" {
  bucket = "my-example-bucket"
  
  tags = {
    Name        = "My Example Bucket"
    Environment = "Dev"
  }
}

# Using another resource that doesn't have an ephemeral alternative - this should PASS
resource "aws_vpc" "example" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "Example VPC"
  }
}

# password = 1234