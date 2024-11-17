resource "aws_apprunner_service" "weatherapp" {
  service_name = "weatherapp-prod"
  instance_configuration {
    instance_role_arn = var.instance_role_arn
  }
  source_configuration {
    authentication_configuration {
      access_role_arn = var.access_role_arn
    }
    image_repository {
      image_configuration {
        port = "5000"
        runtime_environment_secrets = {
          "API" = var.api
        }
      }
      image_identifier      = var.image_identifier
      image_repository_type = "ECR"
    }
    auto_deployments_enabled = false
  }

  tags = {
    Name = "flask-weatherapp"
  }
}