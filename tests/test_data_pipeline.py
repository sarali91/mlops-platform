import pytest
from hashlib import sha256
from pyspark.sql import SparkSession
from src.data_pipeline import hash_patient_ids

@pytest.fixture(scope="session")
def spark_session():
    """Fixture to initialize a local Spark Session for testing."""
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("mlops-unit-tests") \
        .getOrCreate()
    yield spark
    spark.stop()

def test_hash_patient_ids_transforms_correctly(spark_session):
    # 1. Arrange: Create a minimal mock DataFrame with a raw patient ID 
    raw_data = [("PT-12345", "John Doe"), ("PT-67890", "Jane Smith")]
    schema = ["patient_id", "name"]
    input_df = spark_session.createDataFrame(raw_data, schema)

    # Calculate what the expected SHA-256 hash output should be manually 
    expected_hash_1 = sha256("PT-12345".encode()).hexdigest()

    # 2. Act: Run your pipeline's hashing function 
    processed_df = hash_patient_ids(input_df, column_name="patient_id")
    result_rows = processed_df.collect()

    # 3. Assert: Verify the data was masked correctly and schemas match
    assert "patient_id" in processed_df.columns
    
    # Check that the first row's patient_id matches our expected secure hash 
    assert result_rows[0]["patient_id"] == expected_hash_1
    
    # Ensure the raw patient identifier is completely gone 
    assert result_rows[0]["patient_id"] != "PT-12345"