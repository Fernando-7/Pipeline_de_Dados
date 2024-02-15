# Use uma imagem oficial do Airflow como base
FROM apache/airflow:2.8.1-python3.11

# Copie o arquivo requirements.txt para o sistema de arquivos da imagem Docker
COPY requirement.txt /requirement.txt

RUN apt-get update

RUN pip install --user upgrade pip
# Instale as dependências listadas no arquivo requirements.txt
RUN pip install --no-cache-dir --user -r /requirement.txt
