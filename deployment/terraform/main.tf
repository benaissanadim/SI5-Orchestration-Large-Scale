terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.3.0"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

resource "kubernetes_namespace" "polymetrie-increment-teamg" {
  metadata {
    name = "terraform"
  }
}

resource "helm_release" "postgresql" {
  name      = "my-postgresql"
  namespace = kubernetes_namespace.polymetrie-increment-teamg.metadata[0].name
  repository = "https://charts.bitnami.com/bitnami"
  chart     = "postgresql"
  version   = "13.2.24"
  values    = [file("../charts/values/postgres/values-postgres.yaml")]
}

resource "kubernetes_deployment" "polymetrie-increment-teamg" {
  depends_on = [helm_release.postgresql]

  metadata {
    name      = "polymetrie-increment"
    namespace = kubernetes_namespace.polymetrie-increment-teamg.metadata[0].name
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "polymetrie-increment"
      }
    }
    template {
      metadata {
        labels = {
          app = "polymetrie-increment"
        }
      }
      spec {
        container {
          name  = "polymetrie-increment"
          image = "hamza125/polymetrie-increment:latest"
          port {
            container_port = 5000
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "polymetrie-increment-teamg" {

  metadata {
    name      = "polymetrie-increment-service"
    namespace = kubernetes_namespace.polymetrie-increment-teamg.metadata[0].name
  }

  spec {
    selector = {
      app = "polymetrie-increment"
    }
    port {
      protocol    = "TCP"
      port        = 5000
      target_port = 5000
    }
  }
}

