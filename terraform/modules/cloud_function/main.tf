
resource "google_cloudfunctions2_function" "function" {
  name     = var.name
  location = var.region

  build_config {
    runtime     = var.runtime
    entry_point = var.entry_point
    source {
      storage_source {
        bucket = var.bucket
        object = var.object
      }
    }
  }

  service_config {
    max_instance_count    = var.max_instance_count
    available_memory      = var.memory
    timeout_seconds       = var.timeout
    service_account_email = var.service_account_email
  }
}
