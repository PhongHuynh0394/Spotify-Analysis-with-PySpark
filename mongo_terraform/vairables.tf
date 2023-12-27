variable "public_key" {
  type = string
  default = "add-your-key" # add your
}

variable "private_key" {
  type = string
  default = "add-your-key" #add your
}

variable "org_id" {
  type = string
  description = "Organiztion ID"
  default = "add-your-id" # add your
}

variable "username" {
  type = string
  description = "username for cluster"
  default = "root" # you can modify this if needed
}

variable "password" {
  type = string
  description = "pass for cluster"
  default = "123" # You can modify this if needed
}
variable "cluster_name" {
  type = string
  description = "Cluster name"
  default = "spotify-cluster" # you can modify this if needed
}

variable "cluster_size" {
  type = string
  description = "Cluster size name"
  default = "M0" 
}

variable "region" {
  type = string
  description = "Region name"
  default = "WESTERN_EUROPE" 
}

