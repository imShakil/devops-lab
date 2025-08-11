terraform {
  backend "remote" {
    workspaces {
      name = ""
    }

    organization = "value"
  }

  required_version = "1.12.1"

  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "6.2.0"
    }
  }
  
}