variable "name" {
    description = "The name of the GCE node"
    type        = string
}

variable "zone" {
    description = "The instance's zone"
    type        = string
}

variable "service_account" {
    description = "The service account for the node"
}

variable "network" {
    description = "The name of the node's network "
}

variable "subnetwork" {
    description = "The name of the node's subnetwork"
}


variable "machine_type" {
    description = "The node's machine type"
    default     = "n1-standard-4"
}

variable "boot_disk_size" {
    description = "The size of the boot disk"
    default     = 100
}

variable "container_image" {
    description = "The URI of the container image"
    type        = string
}

variable "scopes" {
  description = "Instance scopes."
  type        = list(string)
  default = [
    "https://www.googleapis.com/auth/devstorage.read_only",
    "https://www.googleapis.com/auth/logging.write",
    "https://www.googleapis.com/auth/monitoring.write",
    "https://www.googleapis.com/auth/pubsub",
    "https://www.googleapis.com/auth/service.management.readonly",
    "https://www.googleapis.com/auth/servicecontrol",
    "https://www.googleapis.com/auth/trace.append",
  ]
}