# Flask Weather App

version: 1.0.0

## About this Project

> This program retrives the weather based on a Zipcode, City and Country or City, State and Country. Built to run on AWS Apprunner. See image and website below

## Diagram

<img src="diagram.png" alt="drawing" width="500"/>

<br>

website: https://weatherapp.connaker.org/

## Built with
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)
![HTML](https://img.shields.io/badge/HTML-%23E34F26.svg?logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-1572B6?logo=css3&logoColor=fff)
![Flask](https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff)

## Hosted on

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?logo=amazon-web-services&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff)

## Getting Started

> The following are the prequisites to run this program. It is assumed that these are configured prior to running the program.

Locally: <br>

- IDE (such as VsCode)
- Python 3.10 or higher
- Python virtual environment
- Docker
- API from Open Weather (https://openweathermap.org/)

## Installation

1. Clone the repo

   ```sh
   git clone https://github.com/Connaker/pyowm-weatherappck.git
   ```

## Running Locally

> the following are the steps to run the program locally on your machine using Docker.

1. start your virtual environment

   ```sh
   macOS: source .\venv\Scripts\activate <br>
   Windows: .\venv\Scripts\activate
   ```

2. Install requirements.txt

   ```sh
   pip install -r requirements.txt
   ```

3. Docker build

   ```sh
   docker build -t <image_name> .
   ```  

4. Run docker image

   ```sh
   docker run -d --name <app_name> -e API='API KEY' -p 5000:5000 <image_name>
   ```  

5. Open a browser and navigate to the IP address of the Docker container with port 5000.

## Running on AWS

> Alternatively, the program can be run on AWS using App Runner. There are two ways to do this. Using AppRunner yaml file or storing inside an AWS ECR. An example of using Apprunner yaml file can be found under the apprunner folder. It should be noted that the API key is stored in Systems Manager Parameter store. You will need to update the Apprunner file to pick up your key correctly or it will fail to run. If you like to use ECR, you can simply create your ECR and upload the Dockerfile to the ECR. Then in Apprunner, use the ECR option and point to your ECR repository.

## Notes

> The repository also includes a manifest folder for deployment to Kubernetes, Jenkins folder for Jenkins pipeline and Sonar properties to run through a local CI/CD branch that is not covered here. Additionally, the terraform folder contains a straight forward build to deploy Apprunner to AWS. This will require some modification of the backend and variables files to match your account.