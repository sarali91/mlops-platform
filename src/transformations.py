from pyspark.sql.functions import col, sha2

def hash_patient_ids(df, column_name="patient_id"):
    """Applies HIPAA/GDPR-compliant SHA-256 irreversible hashing."""
    return df.withColumn(column_name, sha2(col(column_name).cast("string"), 256))