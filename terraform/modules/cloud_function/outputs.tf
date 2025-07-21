output "function_name" {
  value = google_cloudfunctions2_function.function.name
}

output "function_url" {
  value = google_cloudfunctions2_function.function.service_config[0].uri
}

output "service_account_email" {
  value = google_cloudfunctions2_function.function.service_config[0].service_account_email
}
