# aws-glue-youtube-etl
# 📺 AWS Glue ETL - YouTube Trending Data

Ce projet met en œuvre un pipeline ETL à l'aide de **AWS Glue** pour traiter les données brutes de tendances YouTube et les stocker dans **Amazon S3** en format **Parquet**, partitionné par **région**.

---

## 🔧 Technologies utilisées

- AWS Glue (Spark / PySpark)
- AWS S3
- AWS Glue Catalog
- AWS Athena (optionnel)
- Python

---

## 📂 Structure

- `glue_jobs/etl_youtube_job.py` : le script principal du Glue Job.

---

## 🚀 Pipeline ETL

1. Lecture des données depuis le Glue Data Catalog (`db_youtube_raw.raw_statistics`)
2. Filtrage par région (`ca`, `gb`, `us`)
3. Mapping des colonnes + nettoyage
4. Écriture dans un bucket S3 au format Parquet, partitionné par `region`

---

## ✅ Exécution

Ce script est conçu pour être lancé **via AWS Glue Job** (en Spark/Python).

---

## 📁 Données

Les données brutes YouTube doivent être enregistrées dans le **Data Catalog AWS Glue** avant l’exécution.

---

## 📌 Exemple de chemin de sortie S3

