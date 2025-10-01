provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "onvolunteers_reports_bucket" {
  name                        = var.gcs_bucket_name
  location                    = var.region
  force_destroy               = false
  uniform_bucket_level_access = true

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_bigquery_dataset" "onvolunteers_reports_dataset" {
  dataset_id                  = var.bq_dataset_id
  project                     = var.project_id
  location                    = var.region
  friendly_name               = "OnVolunteers Reports Data"
  description                 = "BigQuery dataset for OnVolunteers reports ingested from Gmail."
  default_table_expiration_ms = 3600000
  delete_contents_on_destroy  = false
}