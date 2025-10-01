variable "project_id" {
  description = "The GCP project ID."
  type        = string
}

variable "region" {
  description = "The GCP region for resources."
  type        = string
  default     = "us-central1" # Example default region
}

variable "gcs_bucket_name" {
  description = "The name of the GCS bucket for storing Parquet files. Must be globally unique."
  type        = string
}

variable "bq_dataset_id" {
  description = "The ID of the BigQuery dataset."
  type        = string
}