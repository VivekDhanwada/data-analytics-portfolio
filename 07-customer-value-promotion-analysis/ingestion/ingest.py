import os
import logging
import pandas as pd
from datetime import datetime
from google.cloud import bigquery

# Configuration
PROJECT_ID = "dunnhumby-retail-analytics"
DATASET = "raw"
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

# Logging setup
log_filename = f"ingestion_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
log_path = os.path.join(os.path.dirname(__file__), "..", "docs", log_filename)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Expected schema for each table
TABLES = {
    "campaign_desc": {
        "file": "campaign_desc.csv",
        "expected_columns": ["DESCRIPTION", "CAMPAIGN", "START_DAY", "END_DAY"],
        "primary_key": ["CAMPAIGN"]
    },
    "campaign_table": {
        "file": "campaign_table.csv",
        "expected_columns": ["DESCRIPTION", "household_key", "CAMPAIGN"],
        "primary_key": ["household_key", "CAMPAIGN"]
    },
    "causal_data": {
        "file": "causal_data.csv",
        "expected_columns": ["PRODUCT_ID", "STORE_ID", "WEEK_NO", "display", "mailer"],
        "primary_key": ["PRODUCT_ID", "STORE_ID", "WEEK_NO"]
    },
    "coupon_redempt": {
        "file": "coupon_redempt.csv",
        "expected_columns": ["household_key", "DAY", "COUPON_UPC", "CAMPAIGN"],
        "primary_key": ["household_key", "DAY", "COUPON_UPC"]
    },
    "coupon": {
        "file": "coupon.csv",
        "expected_columns": ["COUPON_UPC", "PRODUCT_ID", "CAMPAIGN"],
        "primary_key": ["COUPON_UPC", "PRODUCT_ID"]
    },
    "hh_demographic": {
        "file": "hh_demographic.csv",
        "expected_columns": ["AGE_DESC", "MARITAL_STATUS_CODE", "INCOME_DESC", 
                            "HOMEOWNER_DESC", "HH_COMP_DESC", "HOUSEHOLD_SIZE_DESC", 
                            "KID_CATEGORY_DESC", "household_key"],
        "primary_key": ["household_key"]
    },
    "product": {
        "file": "product.csv",
        "expected_columns": ["PRODUCT_ID", "MANUFACTURER", "DEPARTMENT", "BRAND", 
                            "COMMODITY_DESC", "SUB_COMMODITY_DESC", "CURR_SIZE_OF_PRODUCT"],
        "primary_key": ["PRODUCT_ID"]
    },
    "transaction_data": {
        "file": "transaction_data.csv",
        "expected_columns": ["household_key", "BASKET_ID", "DAY", "PRODUCT_ID", 
                            "QUANTITY", "SALES_VALUE", "STORE_ID", "RETAIL_DISC", 
                            "TRANS_TIME", "WEEK_NO", "COUPON_DISC", "COUPON_MATCH_DISC"],
        "primary_key": ["household_key", "BASKET_ID", "PRODUCT_ID"]
    }
}

def check_file_exists(filepath, table_name):
    if not os.path.exists(filepath):
        logger.error(f"MISSING FILE: {table_name} — {filepath}")
        return False
    logger.info(f"File found: {table_name}")
    return True


def validate_columns(df, expected_columns, table_name):
    actual_columns = list(df.columns)
    missing = [col for col in expected_columns if col not in actual_columns]
    extra = [col for col in actual_columns if col not in expected_columns]
    
    if missing:
        logger.error(f"MISSING COLUMNS in {table_name}: {missing}")
    if extra:
        logger.warning(f"EXTRA COLUMNS in {table_name}: {extra}")
    if not missing:
        logger.info(f"Schema valid: {table_name}")
    return len(missing) == 0


def check_nulls(df, table_name):
    null_counts = df.isnull().sum()
    null_counts = null_counts[null_counts > 0]
    if null_counts.empty:
        logger.info(f"No nulls found: {table_name}")
    else:
        for col, count in null_counts.items():
            logger.warning(f"NULLS in {table_name}.{col}: {count} rows")


def check_duplicates(df, primary_key, table_name):
    duplicate_count = df.duplicated(subset=primary_key).sum()
    if duplicate_count > 0:
        logger.warning(f"DUPLICATES in {table_name}: {duplicate_count} rows on key {primary_key}")
    else:
        logger.info(f"No duplicates found: {table_name}")


def standardise_columns(df):
    df.columns = [col.strip().lower() for col in df.columns]
    return df

def load_to_bigquery(df, table_name, client):
    table_id = f"{PROJECT_ID}.{DATASET}.{table_name}"
    
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    
    try:
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()
        logger.info(f"Loaded {len(df):,} rows into {table_id}")
    except Exception as e:
        logger.error(f"FAILED to load {table_name}: {e}")

def main():
    logger.info("Starting ingestion pipeline")
    client = bigquery.Client(project=PROJECT_ID)
    
    success_count = 0
    fail_count = 0
    
    for table_name, config in TABLES.items():
        logger.info(f"--- Processing: {table_name} ---")
        
        filepath = os.path.join(DATA_PATH, config["file"])
        
        # Check file exists
        if not check_file_exists(filepath, table_name):
            fail_count += 1
            continue
        
        # Load CSV
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df):,} rows from {config['file']}")
        
        # Validate schema
        if not validate_columns(df, config["expected_columns"], table_name):
            fail_count += 1
            continue
        
        # Check nulls
        check_nulls(df, table_name)
        
        # Check duplicates
        check_duplicates(df, config["primary_key"], table_name)
        
        # Standardise column names
        df = standardise_columns(df)
        
        # Load to BigQuery
        load_to_bigquery(df, table_name, client)
        success_count += 1
    
    logger.info(f"Pipeline complete. Success: {success_count} | Failed: {fail_count}")


if __name__ == "__main__":
    main()