module "fnc_get_kaggle_load_gcs" {
  source        = "./modules/cloud_function"
  name          = "fnc-get-kaggle-load-gcs"
  runtime       = "python310"
  object        = "fnc-get-kaggle-load-gcs.zip"
}

module "fnc_get_gcs_load_gbq" {
  source        = "./modules/cloud_function"
  name          = "fnc-get-gcs-load-gbq"
  runtime       = "python310"
  object        = "fnc-get-gcs-load-gbq.zip"
}