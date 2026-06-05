from pyspark.sql import SparkSession

def get_spark_session(app_name="Truveta-MLOps-Pipeline"):
    """Initializes and returns a localized Spark Session."""
    return SparkSession.builder \
        .appName(app_name) \
        .getOrCreate()