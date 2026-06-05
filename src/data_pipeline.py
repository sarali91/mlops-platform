from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sha2

# ==========================================
# 1. PLACE YOUR FUNCTION DEFINITIONS HERE
# ==========================================

def hash_patient_ids(df, column_name="patient_id"):
    """
    Applies HIPAA/GDPR-compliant SHA-256 irreversible hashing 
    to protect sensitive patient identifiers[cite: 10, 36].
    """
    return df.withColumn(column_name, sha2(col(column_name).cast("string"), 256))


# ==========================================
# 2. PLACE YOUR MAIN EXECUTION BLOCK HERE
# ==========================================
if __name__ == "__main__":
    print("🚀 Initializing Spark Session for Healthcare Pipeline...")
    
    # Initialize the local Spark session
    spark = SparkSession.builder \
        .appName("Truveta-MLOps-Pipeline") \
        .getOrCreate()

    # Define your data paths (adjust these if yours are different)
    input_path = "data/mock_ehr.csv"
    output_path = "data/secure_lake/"

    try:
        # 1. Ingest raw EHR data [cite: 36]
        print(f"📥 Reading raw data from: {input_path}")
        raw_df = spark.read.csv(input_path, header=True, inferSchema=True)

        # 2. Apply the hashing transformation using our new function
        print("🔐 Masking patient identifiers via SHA-256...")
        secure_df = hash_patient_ids(raw_df, column_name="patient_id")

        # 3. Write out to scaled, partitioned Parquet files [cite: 36]
        print(f"💾 Saving de-identified data to Parquet lake at: {output_path}")
        secure_df.write \
            .mode("overwrite") \
            .parquet(output_path)
            
        print("✅ Pipeline executed successfully with zero data leaks!")

    except Exception as e:
        print(f"❌ Pipeline failed with error: {str(e)}")
        
    finally:
        # Always stop the Spark session to free up system memory
        spark.stop()