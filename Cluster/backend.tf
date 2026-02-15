terraform {
  backend "s3" {
    bucket         = "nti-terraform-statees"
    key            = "eks/nonprod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "nti-terraform-locks"
    encrypt        = true
  }
}
