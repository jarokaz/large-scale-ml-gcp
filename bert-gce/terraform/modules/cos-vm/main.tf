data "google_compute_image" "cos" {
    family = "cos-stable"
    project = "cos-cloud"
}

resource "google_compute_instance" "container_vm" {
    name             = var.name
    machine_type     = var.machine_type
    zone             = var.zone

    tags             = ["http-traffic", "ssh-traffic"]

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

}

