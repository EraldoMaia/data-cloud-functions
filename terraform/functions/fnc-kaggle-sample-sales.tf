
module "fnc_kaggle_sample_sales" {
  source             = "../modules/cloud_function"
  name               = "fnc-kaggle-sample-sales"
  region             = var.region
  runtime            = "python310"
  entry_point        = "main"
  bucket             = var.cloud_function_bucket
  object             = "fnc-kaggle-sample-sales.zip"
}
