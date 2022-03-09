terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.5.0"
    }
  }
}

provider "google" {
  credentials = file("projet-cloud-instagram-4ceaf2261b59.json")
  project = var.projet_id
  region  = var.region
  zone    = "europe-west1b"
}