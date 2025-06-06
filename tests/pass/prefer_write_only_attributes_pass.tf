# Using write-only attribute
resource "aws_ssm_parameter" "example" {
  name     = "/example/parameter"
  type     = "SecureString"
  value_wo = "sensitive-value"
}

# Using write-only attribute for RDS
resource "aws_db_instance" "example" {
  allocated_storage    = 10
  db_name              = "mydb"
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t3.micro"
  username             = "admin"
  password_wo          = "foobarbaz"
  parameter_group_name = "default.mysql5.7"
  skip_final_snapshot  = true
}
