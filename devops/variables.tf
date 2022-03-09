variable "projet_id"{
  description = "GCP Project ID"
  default = "projet-cloud-instagram"
}

variable "region" {
  description = "GCP Region"
  default = "europe-west1"

}

variable "bucket_name" {
  description = "GCP Bucket Name"
  default = "bucket_deployment"
}

variable "notebook_name" {
  description = "GCP Notebook name"
  default = "notebook-deployment"

}
variable "activate_apis" {
  type = set(string)
  default = [
    "aiplatform.googleapis.com",
    "notebooks.googleapis.com",
    "iamcredentials.googleapis.com",
    "iam.googleapis.com",
    "storage-component.googleapis.com",
    "cloudresourcemanager.googleapis.com"
  ]
}