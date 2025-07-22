module "fnc_kaggle_sample_sales" {
  source        = "./modules/cloud_function"
  name          = "fnc-kaggle-sample-sales"
  runtime       = "python310"
  object        = "fnc-kaggle-sample-sales.zip"
}
