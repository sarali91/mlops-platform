terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

# Automatically use local Kubeconfig context
provider "kubernetes" {
  config_path = "~/.kube/config" 
}

# ---------------------------------------------------------
# Tenant A: UW Medicine
# ---------------------------------------------------------
resource "kubernetes_namespace" "tenant_uw" {
  metadata {
    name = "tenant-uw-medicine"
    labels = {
      "tenant-id"   = "uw-001"
      "environment" = "production"
    }
  }
}

# Apply strict resource quotas for Tenant A
resource "kubernetes_resource_quota" "tenant_uw_quota" {
  metadata {
    name      = "uw-resource-quota"
    namespace = kubernetes_namespace.tenant_uw.metadata[0].name
  }
  spec {
    hard = {
      "requests.cpu"    = "2"
      "requests.memory" = "4Gi"
      "limits.cpu"      = "4"
      "limits.memory"   = "8Gi"
      "pods"            = "10"
    }
  }
}

# ---------------------------------------------------------
# Tenant B: Swedish Medical
# ---------------------------------------------------------
resource "kubernetes_namespace" "tenant_swedish" {
  metadata {
    name = "tenant-swedish-medical"
    labels = {
      "tenant-id"   = "sw-002"
      "environment" = "production"
    }
  }
}
