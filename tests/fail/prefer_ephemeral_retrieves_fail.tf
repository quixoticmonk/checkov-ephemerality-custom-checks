# Using data source when ephemeral alternative exists - this should FAIL CKV2_EPH_RET
data "aws_secretsmanager_random_password" "example" {
  exclude_lowercase = false
  exclude_numbers   = true
  exclude_punctuation = true
  exclude_uppercase = false
  include_space     = false
  length            = 16
}

# Using data source when ephemeral alternative exists - this should FAIL CKV2_EPH_RET
data "tfe_team_token" "example" {
  team_id = "team-123456789"
}
