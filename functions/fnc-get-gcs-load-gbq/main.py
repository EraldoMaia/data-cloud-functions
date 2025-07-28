from csv            import DictReader
from datetime       import datetime
from google.cloud   import storage
from google.cloud   import bigquery
from time           import sleep


def read_csv_from_gcs(bucket_name: str, file_path: str, project_id: str):
    """
    Lê um arquivo CSV do GCS e retorna o cabeçalho e os dados 
    como lista de dicionários (todos os valores como STRING).
    """

    storage_client  = storage.Client(project=project_id)
    bucket          = storage_client.bucket(bucket_name)
    blob            = bucket.blob(f"{file_path}/{file_path}.csv")

    try:
        data = blob.download_as_text(encoding="utf-8").splitlines()

    except UnicodeDecodeError:
        print("UTF-8 falhou, tentando latin1...")
        data = blob.download_as_text(encoding="latin1").splitlines()

    csv_reader       = DictReader(data)

    # Converte cabeçalhos para lower case
    fieldnames_lower = [f.lower() for f in csv_reader.fieldnames]

    rows = []
    for row in csv_reader:
        rows.append({k: str(v) for k, v in row.items()})  # Força tudo como string

    return fieldnames_lower, rows

def create_table_if_not_exists(project_id: str, dataset_id: str, table_id: str, schema_fields: list):
    """
    Cria a tabela no BigQuery caso ela não exista.
    Todos os campos serão STRING, adicionando dt_insercao_registro como DATETIME.
    A tabela será particionada por dt_insercao_registro (DAY).
    """

    client    = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)

    try:
        client.get_table(table_ref)
        print(f"Tabela {dataset_id}.{table_id} já existe.")

    except Exception:
        print(f"Criando tabela {dataset_id}.{table_id}...")
        schema = [bigquery.SchemaField(name, "STRING") for name in schema_fields]
        schema.append(bigquery.SchemaField("dt_insercao_registro", "DATETIME"))

        table                   = bigquery.Table(table_ref, schema=schema)

        # Cria a tabela particionada por dt_insercao_registro
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="dt_insercao_registro"
        )

        table                   = client.create_table(table)
        sleep(60)  # Espera 1 min para garantir que a tabela foi criada

        print(f"Tabela {dataset_id}.{table_id} criada com sucesso e particionada por dt_insercao_registro.")

def validate_schema(csv_header: list, project_id: str, dataset_id: str, table_id: str) -> bool:
    """
    Valida se o cabeçalho do CSV corresponde ao esquema da tabela BigQuery (exceto dt_insercao_registro).
    """
    client          = bigquery.Client(project=project_id)
    table_ref       = client.dataset(dataset_id).table(table_id)
    table           = client.get_table(table_ref)

    expected_schema = [field.name for field in table.schema if field.name != "dt_insercao_registro"]
    return set(csv_header) == set(expected_schema)

def truncate_table_if_exists(project_id: str, dataset_id: str, table_id: str):
    """
    Aplica TRUNCATE TABLE no BigQuery caso a tabela já exista.
    """
    client      = bigquery.Client(project=project_id)
    table_ref   = f"{project_id}.{dataset_id}.{table_id}"

    try:
        client.get_table(f"{dataset_id}.{table_id}")
        print(f"Aplicando TRUNCATE TABLE em {table_ref}...")

        query = f"TRUNCATE TABLE `{table_ref}`"
        client.query(query).result()
        print(f"Tabela {table_ref} truncada com sucesso.")
        
    except Exception:
        print(f"Tabela {table_ref} não existe. Nenhum truncate aplicado.")

def insert_into_bigquery(project_id: str, dataset_id: str, table_id: str, rows: list, mode: str = "streaming"):
    """
    Insere os dados no BigQuery, adicionando o campo dt_insercao_registro.
    Suporta streaming (padrão) ou batch.
    """
    client      = bigquery.Client(project=project_id)
    table_ref   = client.dataset(dataset_id).table(table_id)

    for row in rows:
        row["dt_insercao_registro"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if mode == "batch":
        print(f"Inserindo {len(rows)} registros em batch...")
        job = client.load_table_from_json(rows, table_ref)
        job.result()
        print(f"Inseridos {len(rows)} registros em batch no {dataset_id}.{table_id}")
        
    else:
        print(f"Inserindo {len(rows)} registros via streaming...")
        errors = client.insert_rows_json(table_ref, rows)
        if errors:
            raise RuntimeError(f"Erros ao inserir no BigQuery: {errors}")
        else:
            print(f"Inseridos {len(rows)} registros em streaming no {dataset_id}.{table_id}")

def log_exec_success(project_id, dataset, table_name, qtd_linhas):
    """
    Registra uma carga bem-sucedida na tabela de log.
    """
    client      = bigquery.Client(project=project_id)
    table_ref   = client.dataset("data_quality").table("tb_log_exec")

    rows = [{
        "projeto": project_id,
        "dataset": dataset,
        "table_name": table_name,
        "qtd_linhas": qtd_linhas,
        "dt_insercao_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }]

    errors = client.insert_rows_json(table_ref, rows)
    if errors:
        print(f"[ERRO] Falha ao logar sucesso: {errors}")

def log_exec_error(project_id, dataset, table_name, error_message):
    """
    Registra uma falha na carga na tabela de erro.
    """
    client      = bigquery.Client(project=project_id)
    table_ref   = client.dataset("data_quality").table("tb_log_error")

    rows = [{
        "projeto": project_id,
        "dataset": dataset,
        "table_name": table_name,
        "error_mensage": error_message,
        "dt_insercao_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }]

    errors = client.insert_rows_json(table_ref, rows)
    if errors:
        print(f"[ERRO] Falha ao logar erro: {errors}")


def main(request):

    # Descomentar em ambiente de desenvolvimento local
    # request_json = request

    # Descomentar as linhas abaixo se estiver rodando em um ambiente de produção, como o Cloud Functions
    content_type = request.headers.get('content-type', '')
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
    else:
        return "Invalid content type", 400

    project_id          = request_json.get("project_id")
    bq_raw_project_id   = request_json.get("bq_raw_project_id", project_id)
    dataset_id          = request_json.get("dataset_id")
    bucket_name         = request_json.get("bucket_name")
    gcs_file_path       = request_json.get("file_prefix")
    table_id            = request_json.get("file_prefix")
    mode                = request_json.get("mode", "batch")  # default: bath

    try:
        # 1. Lê o CSV do GCS
        csv_header, rows = read_csv_from_gcs(bucket_name, gcs_file_path, project_id)

        # 2. Cria tabela se não existir
        create_table_if_not_exists(bq_raw_project_id, dataset_id, table_id, csv_header)

        # 3. Valida esquema
        if not validate_schema(csv_header, bq_raw_project_id, dataset_id, table_id):
            raise ValueError(f"Esquema do CSV não corresponde ao da tabela {dataset_id}.{table_id}!")

        # 4. Trunca a tabela se existir
        truncate_table_if_exists(bq_raw_project_id, dataset_id, table_id)

        # 5. Insere os dados
        insert_into_bigquery(bq_raw_project_id, dataset_id, table_id, rows, mode=mode)
        
        # 6. Insere os dados de execução no log de sucesso
        log_exec_success(project_id, dataset_id, table_id, len(rows))

        return f"{len(rows)} registros inseridos em {dataset_id}.{table_id} via {mode}"
    
    except Exception as e:
        error_msg = str(e)
        print(f"[ERRO] {error_msg}")

        # 7. Insere os dados de execução no log de erro
        log_exec_error(project_id, dataset_id, table_id, error_msg)

        return f"Erro ao carregar os dados: {error_msg}", 500
