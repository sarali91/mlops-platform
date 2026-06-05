import mlflow
import random


def train_mock_model():
    # Set the MLflow experiment name
    mlflow.set_experiment("Healthcare_Risk_Prediction")

    with mlflow.start_run():
        print("🧠 Training ML model on securely de-identified patient cohorts...")

        # Log hyperparameters
        mlflow.log_param("algorithm", "RandomForestClassifier")
        mlflow.log_param("max_depth", 12)
        mlflow.log_param("n_estimators", 100)

        # Mock model evaluation metrics
        mock_accuracy = random.uniform(0.90, 0.96)
        mock_auc = random.uniform(0.88, 0.94)

        # Log metrics to MLflow
        mlflow.log_metric("accuracy", mock_accuracy)
        mlflow.log_metric("auc_roc", mock_auc)

        print(
            f"✅ Model training completed. Tracked in MLflow (Accuracy: {mock_accuracy:.2f})"
        )


if __name__ == "__main__":
    train_mock_model()
