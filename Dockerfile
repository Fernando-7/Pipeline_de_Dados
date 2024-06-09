# Use uma imagem oficial do Airflow como base
FROM apache/airflow:2.8.1-python3.11

# Copie o arquivo requirements.txt para o sistema de arquivos da imagem Docker
COPY requirement.txt /requirement.txt

#USER root
#RUN apt-get clean && \ apt-get update && \
#    apt-get upgrade -y && \
#     apt-get clean;
     
USER airflow
# Instale as dependências listadas no arquivo requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /requirement.txt
