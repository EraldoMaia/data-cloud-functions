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

variable "cloud_function_bucket" {
  type        = string
  default     = "tf-cloud-functions-bucket"
  description = "Nome do bucket onde serao armazenadas as funcoes."
}
