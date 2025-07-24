# data-cloud-functions

Repositorio para armazenar os artefatos de criacao de funcoes do cloud run.

Passo a passo, para criar uma nova function:

1. Crie a funcao na pasta functions;
2. Crie a referencia ao modulo na main do terraform principal, com a referencia da nova function
3. Substitua a _FUNCTION_NAME com o nome da funcao nova no arquivo cloudbuild.yaml.


Para poder usar a intragracao entre os projetos é necessario fornecer os acessos ao GCF a conta de servico dentro do projeto especifico.

1. Camada raw:
   ```
   gcloud config set project raw

   gcloud projects add-iam-policy-binding raw \
     --member="serviceAccount:cloudfunction-sa@data-ops-466417.iam.gserviceaccount.com" \
     --role="roles/bigquery.jobUser"

   gcloud projects add-iam-policy-binding raw \
     --member="serviceAccount:cloudfunction-sa@data-ops-466417.iam.gserviceaccount.com" \
     --role="roles/bigquery.dataEditor"
   ```

Para bronze e silver repete o mesmo processo mudando o projeto.
