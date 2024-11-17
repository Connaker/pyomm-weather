variable access_role_arn {
    default = "arn:aws:iam::432367782265:role/service-role/AppRunnerECRAccessRole"
}
variable api{
    default = "arn:aws:ssm:us-east-2:432367782265:parameter/openweatherapi"
}
variable image_identifier {
    default = "432367782265.dkr.ecr.us-east-2.amazonaws.com/flask-weatherapp:latest"
}
variable "instance_role_arn" {
    default = "arn:aws:iam::432367782265:role/apprunnerinstancerole" 
}