# Using regular resource when ephemeral alternative exists - this should FAIL CKV2_EPH_CREATE
resource "tfe_team_token" "example" {
  team_id = "team-123456789"
}

# Using regular resource when ephemeral alternative exists - this should FAIL CKV2_EPH_CREATE
resource "random_password" "example" {
  length = 16
}

# Using regular resource when ephemeral alternative exists - this should FAIL CKV2_EPH_CREATE
resource "tls_private_key" "example" {
  algorithm = "RSA"
  rsa_bits  = 2048
}
