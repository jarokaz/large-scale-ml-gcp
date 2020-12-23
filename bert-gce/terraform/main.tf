terraform {
  required_version = ">= 0.14"
  required_providers {
    google = "~> 3.5"
  }
}

provider "google" {
    project   = var.project_id 
}

data "google_project" "project" {
}

# Create a VPC for GCE node(s)
module "gce_vpc" {
    source     = "./modules/vpc"
    region     = var.region
    network_name =  "${var.name_prefix}-network"
    subnet_name  =  "${var.name_prefix}-subnet"
}