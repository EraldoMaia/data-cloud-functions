
import os
import opendatasets as od
from google.cloud import storage

def main(request):
    dataset_url = "https://www.kaggle.com/datasets/kyanyoga/sample-sales-data"
    download_dir = "/tmp/kaggle-data"
    od.download(dataset_url, data_dir=download_dir)

    # Envia CSV para GCS
    storage_client = storage.Client()
    bucket_name = os.environ["FUNCTION_BUCKET"]
    bucket = storage_client.bucket(bucket_name)

    for root, _, files in os.walk(download_dir):
        for fname in files:
            if fname.endswith(".csv"):
                blob = bucket.blob(f"sample_sales/{fname}")
                blob.upload_from_filename(os.path.join(root, fname))
                print(f"Upload {fname} feito em {bucket_name}/sample_sales/")

    return "Dados do Kaggle enviados ao GCS com sucesso!"
