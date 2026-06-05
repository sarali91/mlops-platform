from pyspark.sql.types import StructType, StructField, StringType


def get_ehr_schema():
    """Defines the strict structural contract for incoming EHR data."""
    return StructType(
        [
            StructField("patient_id", StringType(), False),  # False = Cannot be Null
            StructField("encounter_id", StringType(), True),
            StructField("facility_id", StringType(), True),
            StructField("medical_notes", StringType(), True),
        ]
    )
