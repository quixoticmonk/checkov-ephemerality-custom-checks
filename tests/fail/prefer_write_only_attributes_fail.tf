# Using resource with write-only attribute available but not using it - this should FAIL CKV2_EPH_WO
resource "aws_ssm_parameter" "example" {
  name  = "/example/parameter"
  type  = "SecureString"
  value = "sensitive-value"  # Should use value_wo instead
}

# Using resource with write-only attribute available but not using it - this should FAIL CKV2_EPH_WO
resource "aws_db_instance" "example" {
  allocated_storage    = 10
  db_name              = "mydb"
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t3.micro"
  username             = "admin"
  password             = "foobarbaz"  # Should use password_wo instead
  parameter_group_name = "default.mysql5.7"
  skip_final_snapshot  = true
}

# Using resource with write-only attribute available but not using it - this should FAIL CKV2_EPH_WO
resource "aws_rds_cluster" "example" {
  cluster_identifier      = "aurora-cluster-demo"
  engine                  = "aurora-mysql"
  engine_version          = "5.7.mysql_aurora.2.04.2"
  availability_zones      = ["us-west-2a", "us-west-2b", "us-west-2c"]
  database_name           = "mydb"
  master_username         = "username"
  master_password         = "mustbeeightcharacters"  # Should use master_password_wo instead
  backup_retention_period = 5
  preferred_backup_window = "07:00-09:00"
  skip_final_snapshot     = true
}
