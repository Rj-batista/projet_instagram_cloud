resource "google_project_service" "project_apis" {
  for_each = var.activate_apis
  project  = var.projet_id
  service  = each.value
}

resource "google_service_account" "terraform" {
  account_id = "id-account"
  project = var.projet_id
}

resource "google_storage_bucket" project_bucket{
  name     = var.bucket_name
  location = var.region
  force_destroy = true
  storage_class = "REGIONAL"
  uniform_bucket_level_access = true


}

resource "google_notebooks_instance" "project_notebook" {
  name = var.notebook_name
  location = "europe-west1-b"
  machine_type = "n1-standard-1"
  post_startup_script = "pip install transformers"
  container_image {
    repository = "gcr.io/deeplearning-platform-release/tf-cpu.2-3"
  }

}