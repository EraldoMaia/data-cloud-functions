module "fnc_kaggle_sample_sales" {
  source        = "../../modules/cloud_function" # caminho do módulo Terraform
  name          = "fnc-kaggle-sample-sales"   # nome da função no GCP
  runtime       = "python311"                 # runtime suportado no GCP
  entry_point   = "main"                       # nome da função dentro do main.py
  bucket_source = var.bucket_source            # bucket onde o zip da função será armazenado
  source_path   = "../../functions/fnc-kaggle-sample-sales" # código da função
  service_account_email = var.service_account_email        # se o módulo suportar SA
}
