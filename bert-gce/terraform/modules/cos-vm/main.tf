locals {
    cloud_init = "${path.module}/assets/cloud-config.yaml"
}

data "google_compute_image" "cos" {
    family = "cos-stable"
    project = "cos-cloud"
}

data "template_file" "cloud-init" {
    template = file(local.cloud_init)

    vars = {
        image = var.container_image
    }
}

resource "google_compute_instance" "container_vm" {
    name             = var.name
    machine_type     = var.machine_type
    zone             = var.zone

    tags             = ["ssh-traffic"]

    network_interface {
        network = var.network
        subnetwork = var.subnetwork
        access_config {}
    }

    boot_disk {
        initialize_params {
          image = data.google_compute_image.cos.self_link
          size  = var.boot_disk_size
        }
    }

    service_account {
        email = var.service_account
        scopes = var.scopes
    }

    scheduling {
        automatic_restart   = true
        on_host_maintenance = "MIGRATE"
    }

    #metadata = {
    #    user-data = data.template_file.cloud-init.rendered
    #}

}

