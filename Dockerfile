FROM apache/airflow:2.10.2

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
USER airflow

RUN pip install --no-cache-dir \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.2/constraints-3.12.txt" \
    dbt-postgres==1.8.0 dbt-core==1.8.0 great-expectations==0.18.19 pandas sqlalchemy