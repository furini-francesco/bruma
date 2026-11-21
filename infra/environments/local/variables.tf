variable "environment_name" {
  description = "Name of the local environment"
  type        = string
  default     = "local"
}

variable "app_name" {
  description = "Name of the application managed in this environment"
  type        = string
  default     = "demo-api"
}
