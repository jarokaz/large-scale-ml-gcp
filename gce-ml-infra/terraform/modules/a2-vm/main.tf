locals {
    startup_script = "${path.module}/assets/startup-script.sh"
}

data "google_compute_image" "ubuntu" {
    family = "ubuntu-2004-lts"
    project = "ubuntu-os-cloud"
}

data "template_file" "startup_script" {
    template = file(local.startup_script)

    vars = {
        cuda_version = var.cuda_version
    }
}

resource "google_compute_instance" "container_vm" {
    name             = var.name
    machine_type     = var.machine_type
    zone             = var.zone

    tags             = ["ssh-traffic"]

    #guest_accelerator = [ {
    #  count = var.gpu_count
    #  type = var.gpu_type
    #} ]

    network_interface {
        network = var.network
        subnetwork = var.subnetwork
        access_config {}
    }

    boot_disk {
        initialize_params {
          image = data.google_compute_image.ubuntu.self_link
          size  = var.boot_disk_size
        }
    }

    service_account {
        email = var.service_account
        scopes = var.scopes
    }

    scheduling {
        automatic_restart   = true
        on_host_maintenance = "TERMINATE"
    }

    metadata_startup_script = data.template_file.startup_script.rendered
    

}

