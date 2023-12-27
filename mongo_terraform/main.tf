terraform {
  required_providers {
    mongodbatlas = {
      source = "mongodb/mongodbatlas",
      version = "1.8.0"
    }
  }
}

provider "mongodbatlas" {
  public_key = var.public_key
  private_key = var.private_key

}

resource "mongodbatlas_project" "spotify_project" {
  name = "spotify_project"
  org_id = var.org_id
  is_collect_database_specifics_statistics_enabled = true
  is_data_explorer_enabled = true
  is_performance_advisor_enabled = true
  is_realtime_performance_panel_enabled = true
  is_schema_advisor_enabled = true
}

resource "mongodbatlas_cluster" "spotify" {
  name = var.cluster_name
  project_id = mongodbatlas_project.spotify_project.id
  backing_provider_name = "GCP"
  provider_name = "TENANT"
  provider_instance_size_name = var.cluster_size
  provider_region_name = var.region
}

resource "mongodbatlas_database_user" "mongo_user" {
  project_id = mongodbatlas_project.spotify_project.id
  auth_database_name = "admin"
  username = var.username
  password = var.password
  roles {
    role_name     = "readWriteAnyDatabase"
    database_name = "admin"
  }
}

resource "mongodbatlas_project_ip_access_list" "network" {
  project_id = mongodbatlas_project.spotify_project.id
  cidr_block = "0.0.0.0/0"
  comment  = "Access from anywhere"
}

output "srv_address" {
  value = mongodbatlas_cluster.spotify.connection_strings[0].standard_srv
}

output "user" {
  value = var.username
}

output "password" {
  value = var.password
}
