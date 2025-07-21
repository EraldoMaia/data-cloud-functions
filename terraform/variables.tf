variable "region" {
  type        = string
  default     = "southamerica-east1"
  description = "Regiao onde os recursos serao criados."
}

variable "project_id" {
  type        = string
  default     = "data-ops-466417"
  description = "Id do projeto onde os recursos serao criados."
}

variable "bucket_source" {
  type        = string
  default     = "tf-cloud-functions-bucket"
  description = "Nome do bucket onde serao armazenadas as funcoes."
}

variable "tf_state_gcf_bucket" {
  description = "Bucket GCS para armazenar o tfstate e os logs do Cloud Build."
  type        = string
  default     = "cloudbuild-logs-cloud-function-466417"
}

variable "service_account_email" {
  description = "Service Account que a função irá usar"
  type        = string
  default     = "cloud-function-sa@data-ops-466417.iam.gserviceaccount.com"
}