import os
from kagglehub      import dataset_download
from google.cloud   import storage
from google.cloud   import secretmanager
from json           import loads
from re             import sub
from glob           import glob

def get_secret(secret_url):
    """
    Funcao para acessar o Secret Manager e obter as credenciais do Kaggle.
    """
    client      = secretmanager.SecretManagerServiceClient()
    response    = client.access_secret_version(name=secret_url)
    
    clean_response = sub(r'[\n\r\t]', '', response.payload.data.decode('UTF-8')) # Remove caracteres de controle (\n, \r, \t)
    return loads(clean_response)  # Converte o JSON em um dicionário Python

def upload_to_gcs(bucket_name, source_file_path, destination_blob_name, project_id, folder_name):
    """
    Envia um arquivo local para o GCS dentro de uma pasta opcional.
    
    :param bucket_name: Nome do bucket
    :param source_file_path: Caminho local do arquivo
    :param destination_blob_name: Nome do arquivo no bucket
    :param project_id: ID do projeto GCP
    :param folder_name: Nome da pasta no bucket (opcional)
    """
    storage_client  = storage.Client(project=project_id) if project_id else storage.Client()
    bucket          = storage_client.bucket(bucket_name)
    
    # Se a pasta for especificada, prefixa o nome do arquivo com ela
    blob_name   = f"{folder_name}/{destination_blob_name}" if folder_name else destination_blob_name
    blob        = bucket.blob(blob_name)
    
    blob.upload_from_filename(source_file_path)
    print(f"Arquivo {source_file_path} carregado em: gs://{bucket_name}/{blob_name}")
    return f"gs://{bucket_name}/{blob_name}"


def main(request):

    # Descomentar em ambiente de desenvolvimento local
    # request_json = request

    # Descomentar as linhas abaixo se estiver rodando em um ambiente de produção, como o Cloud Functions
    content_type = request.headers.get('content-type', '')
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
    else:
        return "Invalid content type", 400

    # Obtendo os parâmetros da requisição, que devem ser passados via URL
    project_id      = request_json.get("project_id")
    bucket_name     = request_json.get("bucket_name")   
    secret_url      = request_json.get("secret_url")    
    file_prefix     = request_json.get("file_prefix")

    # Armazenando os valores das secrets do Kaggle em variáveis de ambiente
    secret_data = get_secret(secret_url)

    # Atribui os valores das secrets do Kaggle às variáveis locais 
    os.environ["KAGGLE_USERNAME"]   = secret_data["username"]
    os.environ["KAGGLE_KEY"]        = secret_data["key"]

    # 1. Baixar dataset localmente
    dataset_path = dataset_download("kyanyoga/sample-sales-data")
    print(f"Dataset baixado em: {dataset_path}")

    # 2. Localizar o arquivo CSV no diretório baixado
    csv_files = glob(os.path.join(dataset_path, "*.csv"))
    if not csv_files:
        raise FileNotFoundError("Nenhum arquivo CSV encontrado no dataset baixado!")
    
    local_csv = csv_files[0]  # assume que há apenas um CSV
    print(f"Encontrado CSV: {local_csv}")

    # 3. Enviar para o GCS
    upload_to_gcs(bucket_name=bucket_name,source_file_path= local_csv, destination_blob_name= f"{file_prefix}.csv", project_id=project_id, folder_name=file_prefix)


    return f"gs://{bucket_name}/{file_prefix}.csv"
