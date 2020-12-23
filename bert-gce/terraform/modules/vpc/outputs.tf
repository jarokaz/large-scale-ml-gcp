output "subnet_name" {
    value = google_compute_subnetwork.subnetwork.name
}

output "network_name" {
    value = google_compute_network.vpc_network.name
}
