module "fnc_get_kaggle_load_gcs" {
  source        = "./modules/cloud_function"
  name          = "fnc-get-kaggle-load-gcs"
  runtime       = "python310"
  object        = "fnc-get-kaggle-load-gcs.zip"
}
