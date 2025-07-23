import kagglehub
import os
from google.cloud import storage
from google.cloud import secretmanager

def get_secret(secret_url):
    """
    Funcao para acessar o Secret Manager e obter as credenciais do Kaggle.
    """
    client      = secretmanager.SecretManagerServiceClient()
    response    = client.access_secret_version(name=secret_url)
    return response.payload.data.decode('UTF-8')

def get_bucket(bucket_name,project_id):
    """
    Funcao para acessar o bucket do Google Cloud Storage.
    """
    storage_client = storage.Client()
    bucket         = storage_client.bucket(bucket_name,project_id)
    return bucket

def main(request):

    # Obtendo os parâmetros da requisição, que devem ser passados via URL
    project_id      = request.args.get("project_id")
    file_prefix     = request.args.get("file_prefix")
    name_csv        = request.args.get("name_csv")
    bucket_name     = request.args.get("bucket_name")   # bucket_name = ""
    secret_url      = request.args.get("secret_url")    # Caminho da secret no Secret Manager

    # Armazenando os valores das secrets do Kaggle em variáveis de ambiente
    header_params = get_secret(secret_url)
    # Atribui os valores das secrets do Kaggle às variáveis locais 
    os.environ["KAGGLE_USERNAME"]   = header_params["username"]
    os.environ["KAGGLE_KEY"]        = header_params["key"]

    # Obtem o bucket do GCS
    bucket_path = get_bucket(bucket_name,project_id)

    # Baixa o dataset do Kaggle e envia para o bucket do GCS
    dataset_path = kagglehub.dataset_download("kyanyoga/sample-sales-data",bucket_path=bucket_path, file_prefix=file_prefix, name_csv=name_csv)
    print("Dataset baixado em:", dataset_path)
    
    return 'Successfully downloaded dataset from Kaggle and uploaded to GCS bucket.'
