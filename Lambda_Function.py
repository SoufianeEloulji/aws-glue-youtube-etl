import awswrangler as wr
import pandas as pd
import urllib.parse
import os
import traceback

# Récupération des variables d'environnement
os_input_s3_cleansed_layer = os.environ['s3_cleansed_layer']
os_input_glue_catalog_db_name = os.environ['glue_catalog_db_name']
os_input_glue_catalog_table_name = os.environ['glue_catalog_table_name']
os_input_write_data_operation = os.environ['write_data_operation']

def lambda_handler(event, context):
    print("Événement reçu :", event)
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print(f"Nom du bucket : {bucket}")
    print(f"Clé de l'objet : {key}")
    
    try:
        # Lecture du fichier JSON depuis S3
        file_path = f's3://{bucket}/{key}'
        print(f"Lecture du fichier : {file_path}")
        df_raw = wr.s3.read_json(file_path)
        print("Lecture JSON réussie.")

        # Vérification que la clé 'items' existe
        if 'items' not in df_raw:
            raise ValueError("Le champ 'items' est manquant dans le JSON.")

        # Normalisation des données imbriquées
        df_step_1 = pd.json_normalize(df_raw['items'])
        print("Normalisation réussie. Aperçu des données :")
        print(df_step_1.head())

        # Écriture au format Parquet dans S3 + catalogage Glue
        print(f"Écriture dans : {os_input_s3_cleansed_layer}")
        wr_response = wr.s3.to_parquet(
            df=df_step_1,
            path=os_input_s3_cleansed_layer,
            dataset=True,
            database=os_input_glue_catalog_db_name,
            table=os_input_glue_catalog_table_name,
            mode=os_input_write_data_operation
        )
        print("Écriture réussie dans S3 + Glue catalogué.")
        print("Réponse awswrangler :", wr_response)

        return {
            'statusCode': 200,
            'body': f'Succès : fichier {key} traité et écrit dans {os_input_s3_cleansed_layer}'
        }

    except Exception as e:
        print("Une erreur est survenue :")
        print(traceback.format_exc())
        print(f"Erreur lors du traitement de l'objet {key} dans le bucket {bucket}.")
        raise e
