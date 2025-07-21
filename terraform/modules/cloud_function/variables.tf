
variable "name" {}
variable "region" {}
variable "runtime" {}
variable "entry_point" {}
variable "bucket" {}
variable "object" {}
variable "memory" { default = "256M" }
variable "timeout" { default = 90 }
variable "max_instance_count" { default = 1 }
variable "service_account_email" {default = "cloud-function-sa@data-ops-466417.iam.gserviceaccount.com"}
