
resource "google_compute_network" "vpc_network" {
    name                    = var.network_name
    auto_create_subnetworks = "false"
    routing_mode            = "REGIONAL"
}

resource "google_compute_subnetwork" "subnetwork" {
    name                     = var.subnet_name
    region                   = var.region
    network                  = google_compute_network.vpc_network.self_link
    ip_cidr_range            = var.subnet_ip_range
    private_ip_google_access = true
}

resource "google_compute_firewall" "http-ssh" {
  name    = "allow-ssh"
  network = google_compute_network.vpc_network.self_link

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags = ["ssh-traffic"]
}