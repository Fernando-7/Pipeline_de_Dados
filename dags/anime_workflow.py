from airflow import DAG
from datetime import datetime
import pandas as pd
from airflow.operators.python import PythonOperator
import ast
import re
from google.oauth2 import service_account

def brute_base():
    df = pd.read_csv("/opt/airflow/data/animeInfoCombination.csv")
    df['key'] = range(1, len(df) + 1)
    df.to_csv('/opt/airflow/data/animeInfoCombinationFinal.csv', index=False) 

def producers_dataset():
    credentials_path = '/opt/airflow/data/tcc-uspesalq-6d0d06026a16.json'
    credential = service_account.Credentials.from_service_account_file(credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"])
    df = pd.read_csv("/opt/airflow/data/animeInfoCombinationFinal.csv")
    print("Dataframe:", type(df))
    print("Credential:", type(credential))
    # Criando um dataset de produtoras
    # transformando listas de string em listas normais
    df['producers'] = df['producers'].apply(lambda x: ast.literal_eval(str(x)) if pd.notna(str(x)) else str(x))
    # Quebrando a lista e unidades em todo o dataframe
    producers = df[['key','producers']].explode('producers')
    # Removendo valores nulos
    producers = producers.dropna(subset=['producers'])
    # persistindo os dados de produtoras
    producers.to_gbq(credentials=credential,destination_table='tccuspesalq.producer',if_exists='replace',project_id='tcc-uspesalq')

def genres_dataset():
    credentials_path = '/opt/airflow/data/tcc-uspesalq-6d0d06026a16.json'
    credential = service_account.Credentials.from_service_account_file(credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"])
    df = pd.read_csv("/opt/airflow/data/animeInfoCombinationFinal.csv")
    # Criando um dataset de generos
    # transformando listas de string em listas normais
    df['genres'] = df['genres'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)
    # Quebrando a lista e unidades em todo o dataframe
    genres = df[['key','genres']].explode('genres')
    # Removendo valores nulos
    genres = genres.dropna(subset=['genres'])
    # Remover repetições de genero, o genero padrão tem como nome por exemplo DramaDrama, agora só Drama
    genres['genres'] = genres['genres'].apply(lambda x: re.sub(r'(\w+)\1', r'\1', x))
    # persistindo os dados de gêneros de animes no bigquery
    genres.to_gbq(credentials=credential,destination_table='tccuspesalq.genres',if_exists='replace',project_id='tcc-uspesalq')

def voice_dataset():
  credentials_path = '/opt/airflow/data/tcc-uspesalq-6d0d06026a16.json'
  credential = service_account.Credentials.from_service_account_file(credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"])
  df = pd.read_csv("/opt/airflow/data/animeInfoCombinationFinal.csv")
  # Criando um dataset de vozes dos atores
  # transformando listas de string em listas normais
  df['voiceActorNameandLanguage'] = df['voiceActorNameandLanguage'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)
  # Quebrando a lista e unidades em todo o dataframe
  voiceActor = df[['key','voiceActorNameandLanguage']].explode('voiceActorNameandLanguage')
  # Removendo valores nulos
  voiceActor = voiceActor.dropna(subset=['voiceActorNameandLanguage'])
  # Resetando index estático
  voiceActor.reset_index(inplace=True)
  voiceActor['ActorName'] = voiceActor['voiceActorNameandLanguage'].apply(lambda x: x[0])
  voiceActor['Language'] = voiceActor['voiceActorNameandLanguage'].apply(lambda x: x[1])
  # Removendo index estático
  voiceActor = voiceActor.drop(['index','voiceActorNameandLanguage'], axis=1)
  # persistindo os dados de gêneros de atores no bigquery

  voiceActor.to_gbq(credentials=credential,destination_table='tccuspesalq.voice_actors',if_exists='replace',project_id='tcc-uspesalq')

def licenses():
    credentials_path = '/opt/airflow/data/tcc-uspesalq-6d0d06026a16.json'
    credential = service_account.Credentials.from_service_account_file(credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"])
    df = pd.read_csv("/opt/airflow/data/animeInfoCombinationFinal.csv")
    # Criando um dataset de licenciadores
    # transformando listas de string em listas normais
    df['licenses'] = df['licenses'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)
    # Quebrando a lista e unidades em todo o dataframe
    licenses = df[['key','licenses']].explode('licenses')
    # Removendo valores nulos
    licenses = licenses.dropna(subset=['licenses'])
    # persistindo os dados de licenciadores no bigquery
    licenses.to_gbq(credentials=credential,destination_table='tccuspesalq.licenses',if_exists='replace',project_id='tcc-uspesalq')

def principal():
    credentials_path = '/opt/airflow/data/tcc-uspesalq-6d0d06026a16.json'
    credential = service_account.Credentials.from_service_account_file(credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"])
    df = pd.read_csv("/opt/airflow/data/animeInfoCombinationFinal.csv")
    principal = df.drop(['producers','genres','staffNameandOccupation','voiceActorNameandLanguage','licenses'], axis=1)
    # persistindo os dados principais no bigquery
    principal.to_gbq(credentials=credential,destination_table='tccuspesalq.principal',if_exists='replace',project_id='tcc-uspesalq')

with DAG('Anime_Workflow', start_date = datetime(2024,5,23),
         schedule_interval = '30 * * * *', catchup = False) as dag:

  taskBruteBase = PythonOperator(
    task_id = 'task_brute_base',
    python_callable = brute_base
  )

  taskProducersDataset = PythonOperator(
    task_id = 'task_producers_dataset',
    python_callable = producers_dataset
  )
  
  taskGenresDataset = PythonOperator(
    task_id = 'task_genres_dataset',
    python_callable = genres_dataset
  )

  taskVoiceDataset = PythonOperator(
    task_id = 'task_voice_dataset',
    python_callable = voice_dataset
  )

  taskLicenses = PythonOperator(
    task_id = 'task_licenses',
    python_callable = licenses
  )

taskPrincipal = PythonOperator(
    task_id = 'task_principal',
    python_callable = principal
  )

# Definindo a sequência das tarefas
taskBruteBase >> taskProducersDataset >> taskGenresDataset >> taskVoiceDataset >> taskLicenses >> taskPrincipal 