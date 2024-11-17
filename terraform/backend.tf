terraform {
  #backend "local" {}
  backend "s3" {
    bucket = "connaker-terraform-statefiles"
    key    = "apprunner/weatherapp.tfstate"
    region = "us-east-1"
  }
}