# Multi-Tenant Healthcare MLOps Platform 🏥☁️

A cloud-native, multi-tenant data processing and MLOps platform designed to ingest, anonymize, and process Electronic Health Records (EHR) in compliance with GDPR/HIPAA standards. 

## 🚀 Key Features
* **Multi-Tenant Architecture:** Namespace-isolated processing environments provisioned via **Terraform**.
* **GDPR-Compliant Data Pipeline:** Utilizes **PySpark** to ingest mock EHR data, securely hashing PII (Patient Identifiers) to create de-identified research cohorts.
* **MLOps Integration (Coming Soon):** Model tracking and deployment lifecycle managed by **MLflow**.

## 🛠️ Tech Stack
* **Big Data & Processing:** PySpark, Pandas
* **MLOps:** MLflow, Scikit-learn
* **InfraOps (IaC):** Terraform, Kubernetes (Minikube)
* **Language:** Python 3.10, C# (.NET Core - planned)

## 💻 Quick Start
1. **Clone the repository:**
   `git clone https://github.com/sarali91/mlops-platform.git`
2. **Install dependencies:**
   `pip install -r requirements.txt`
3. **Run the Data Pipeline:**
   `python data_pipeline.py`
   *(Check the generated `data/processed_ehr` directory for partitioned Parquet files).*
