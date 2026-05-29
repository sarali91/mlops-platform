import os
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

def create_spark_session():
    """Initialize local Spark Session for data processing."""
    return SparkSession.builder \
        .appName("Truveta-EHR-Anonymization-Pipeline") \
        .master("local[*]") \
        .getOrCreate()

def generate_mock_ehr_data(spark):
    """Generate mock Electronic Health Record (EHR) data containing PII."""
    data = [
        ("uw-001", "P1001", "John Doe", "123-45-6789", 45, "Type 2 Diabetes", "Metformin"),
        ("uw-001", "P1002", "Jane Smith", "987-65-4321", 62, "Hypertension", "Lisinopril"),
        ("sw-002", "P2001", "Alice Johnson", "555-66-7777", 28, "Asthma", "Albuterol"),
        ("sw-002", "P2002", "Bob Brown", "111-22-3333", 50, "Type 2 Diabetes", "Insulin")
    ]
    
    schema = StructType([
        StructField("tenant_id", StringType(), True),
        StructField("patient_id", StringType(), True),
        StructField("patient_name", StringType(), True),    # PII (Needs anonymization)
        StructField("ssn", StringType(), True),             # PII (Needs anonymization)
        StructField("age", IntegerType(), True),
        StructField("diagnosis", StringType(), True),
        StructField("medication", StringType(), True)
    ])
    
    return spark.createDataFrame(data, schema)

def process_and_anonymize(df):
    """
    Implement GDPR/HIPAA compliant anonymization logic:
    1. Drop direct identifiers (Name, SSN).
    2. Apply SHA-256 irreversible hashing to Patient ID.
    """
    print("Executing Anonymization (GDPR/HIPAA Compliance)...")
    anonymized_df = df.drop("patient_name", "ssn") \
                      .withColumn("hashed_patient_id", F.sha2(F.col("patient_id"), 256)) \
                      .drop("patient_id")
    return anonymized_df

if __name__ == "__main__":
    spark = create_spark_session()
    
    # 1. Ingest raw data
    raw_df = generate_mock_ehr_data(spark)
    print("--- Raw EHR Data (Contains PII) ---")
    raw_df.show()
    
    # 2. Process and anonymize
    clean_df = process_and_anonymize(raw_df)
    print("--- De-identified Research Data (Safe for ML Training) ---")
    clean_df.show(truncate=False)
    
    # 3. Write to local Parquet files partitioned by tenant (Simulating Data Lake)
    output_path = "./data/processed_ehr"
    print(f"Writing data to partitioned Data Lake: {output_path}")
    
    clean_df.write \
            .mode("overwrite") \
            .partitionBy("tenant_id") \
            .parquet(output_path)
    
    print("Data Pipeline Completed Successfully!")
    spark.stop()
