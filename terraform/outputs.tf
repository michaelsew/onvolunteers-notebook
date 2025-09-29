output "gcs_bucket_self_link" {
  description = "The self_link of the created GCS bucket."
  value       = google_storage_bucket.onvolunteers_reports_bucket.self_link
}

output "gcs_bucket_name" {
  description = "The name of the created GCS bucket."
  value       = google_storage_bucket.onvolunteers_reports_bucket.name
}

output "bq_dataset_id" {
  description = "The ID of the created BigQuery dataset."
  value       = google_bigquery_dataset.onvolunteers_reports_dataset.dataset_id
}