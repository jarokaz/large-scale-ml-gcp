terraform {
  required_version = ">= 0.14"
  required_providers {
    google = "~> 3.5"
  }
}

provider "google" {
    project   = var.project_id 
}

data "google_project" "project" {}

data "google_compute_default_service_account" "default" {}

# Create a VPC for GCE node(s)
module "vpc" {
    source     = "./modules/vpc"
    region     = var.region
    network_name =  "${var.name_prefix}-network"
    subnet_name  =  "${var.name_prefix}-subnet"
}

module "training_node" {
    source          = "./modules/cos-vm"
    name            = "${var.name_prefix}-vm"
    description     = "V100 compute node"
    zone            = var.zone
    network         = module.vpc.network_name
    subnetwork      = module.vpc.subnet_name
    service_account = data.google_compute_default_service_account.default.email
}