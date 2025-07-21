# Bucket para armazenar o tfstate (precisa existir antes do primeiro init remoto)
resource "google_storage_bucket" "tfstate_bucket" {
  name          = var.tfstate_bucket
  location      = var.region
  force_destroy = false

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 365
    }
  }
}

module "fnc_kaggle_sample_sales" {
  source = "./functions/fnc-kaggle-sample-sales.tf"
}
