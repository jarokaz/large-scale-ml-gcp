terraform {
  required_version = ">= 0.14"
  required_providers {
    google = "~> 3.5"
  }

  backend "gcs" {
    bucket  = "jk-terraform-state"
    prefix  = "bert-gce-lab"
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
    #source          = "./modules/dl-vm"
    source          = "./modules/a2-vm"
    name            = "${var.name_prefix}-vm"
    zone            = var.zone
    network         = module.vpc.network_name
    subnetwork      = module.vpc.subnet_name
    machine_type    = var.machine_type
    service_account = data.google_compute_default_service_account.default.email
    container_image = var.container_image
}


resource "google_storage_bucket" "artifact_repo" {
  name          = "${var.name_prefix}-bucket"
  location      = var.region
  storage_class = "REGIONAL"
  force_destroy = false
}