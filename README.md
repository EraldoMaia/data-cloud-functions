# data-cloud-functions

Repositorio para armazenar os artefatos de criacao de funcoes do cloud run.

Passo a passo, para criar uma nova function:

1. Crie a funcao na pasta functions;
2. Crie a referencia ao modulo na main do terraform principal, com a referencia da nova function
3. Substitua a _FUNCTION_NAME com o nome da funcao nova no arquivo cloudbuild.yaml.
