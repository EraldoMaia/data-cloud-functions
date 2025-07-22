# Todas as variáveis necessárias para o módulo de Cloud Function
# As que nao possuem valor default devem ser passadas no momento da chamada do módulo
# E aquelas que possuem default podem ser sobrescritas se necessário
variable "name" {
    description = "Nome da função do Cloud Function"
    type        = string
}
variable "region" {
    description = "Região onde a função será criada"
    type        = string
    default     = "southamerica-east1"
}
variable "runtime" {
    description = "Runtime da função do Cloud Function"
    type        = string
}
variable "entry_point" {
    description = "Ponto de entrada da função do Cloud Function"
    type        = string
    default     = "main"
}
variable "bucket" {
    description = "Bucket do GCS onde o código da função está armazenado"
    type        = string
    default     = "tf-cloud-functions-bucket"
}
variable "object" {
    description = "Objeto (zip) dentro do bucket do GCS"
    type        = string
}
variable "memory" { 
    description = "Memória alocada para a função do Cloud Function"
    type        = string
    default     = "256M"
}
variable "timeout" { 
    description = "Tempo limite para a execução da função do Cloud Function em segundos"
    type        = number
    default = 90 
}
variable "max_instance_count" { 
    description = "Número máximo de instâncias da função do Cloud Function"
    type        = number
    default = 1 
}
variable "service_account_email" {
    description = "Email da Service Account que a função irá usar"
    type        = string
    default = "cloud-function-sa@data-ops-466417.iam.gserviceaccount.com"
}
