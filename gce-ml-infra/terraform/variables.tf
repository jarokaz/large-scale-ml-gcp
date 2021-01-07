variable "project_id" {
    description = "The GCP project ID"
    type        = string
}

variable "region" {
    description = "The region for the environment's components"
    type        = string
}

variable "zone" {
    description = "The zone for the GCE node"
    type        = string
}

variable "name_prefix" {
    description = "The name prefix to add to the resource names"
    type        = string
}

variable "container_image" {
    description = "The URI of the container image"
    type        = string
}

variable "machine_type" {
    description = "The node's machine type"
    type        = string
}