# ADR 0001: Use SHA-256 for EHR De-identification

**Date:** 2026-06-05
**Status:** Accepted

## Context
Our Multi-Tenant Healthcare MLOps Platform must ingest raw Electronic Health Records (EHR) and strip all Personally Identifiable Information (PII) before the data lands in the secure Parquet data lake for machine learning training. To maintain referential integrity (e.g., tracking a single patient across multiple encounters without knowing who they are), we need a deterministic hashing mechanism for the `patient_id` field.

We must comply with HIPAA Safe Harbor standards, which require that the de-identification method cannot be reasonably reversed.

## Considered Alternatives
1. **MD5 Hashing:** Faster compute, but cryptographically broken and vulnerable to collision attacks. Does not meet modern compliance standards.
2. **AES-256 Encryption:** Allows for two-way decryption. While secure, it introduces the overhead of key rotation and management (KMS), and decryption is not required for downstream ML model training.
3. **SHA-256 Hashing:** A one-way cryptographic hash function. It provides strong resistance against pre-image and collision attacks, requires no key management, and perfectly preserves referential integrity.

## Decision
We will use **SHA-256** to irreversibly mask `patient_id` and `encounter_id` identifiers within the PySpark ingestion pipeline. 

## Consequences
* **Positive:** Achieves HIPAA compliance without introducing the operational overhead of managing encryption keys. Data scientists can join tables on the hashed IDs perfectly.
* **Negative:** Slightly higher CPU overhead during the PySpark transformation phase compared to non-cryptographic hashes like MurmurHash (though acceptable given the security mandate).
* **Negative:** Susceptible to dictionary attacks if the raw `patient_id` format is highly predictable. In the future, if ID entropy is low, we may need to introduce a "salt" (HMAC-SHA256) loaded via secure environment variables.