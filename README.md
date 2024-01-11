# Python Flask ML Demo Project with CI/CD in AWS EC2

| 1. CI Status <br>(build and test) | 2. CD status <br>(docker build and push in DockerHub) | 3. CD Status <br>(AWS EC2 docker pull and run) |
| ---- | ---- | ---- |
| [![ci-build-python-app](https://github.com/matiaspakua/ml-demo-project/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/matiaspakua/ml-demo-project/actions/workflows/python-app.yml) | [![cd-build-publish-docker-image](https://github.com/matiaspakua/ml-demo-project/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/matiaspakua/ml-demo-project/actions/workflows/docker-image.yml) | [![run-docker-image](https://github.com/matiaspakua/ml-demo-project/actions/workflows/docker-run.yml/badge.svg?branch=main)](https://github.com/matiaspakua/ml-demo-project/actions/workflows/docker-run.yml) |
# Project Overview

This is the demonstration project for the Course - Duke university: **Specialization Building Cloud Computing Solutions at Scale** by Noah Gift.

This project demonstrates how to develop a Flask web application for image classification using the MobileNetV2 pre-trained model from TensorFlow Hub. MobileNetV2 is a lightweight convolutional neural network (CNN) architecture, making it ideal for deploying on mobile devices and web applications.

[Pre-Trained Model webpage](https://pytorch.org/hub/pytorch_vision_mobilenet_v2/)

The project utilizes the TensorFlow Hub library to load the pre-trained MobileNetV2 model and integrate it with the Flask application. Users can upload images to the application, which are then processed by the MobileNetV2 model to predict the class of the image. The predicted class is displayed to the user along with the model's confidence score.

[TensoyFlow Project](https://www.tensorflow.org/)

[Hub of pre-trained models](https://www.kaggle.com/models?tfhub-redirect=true)
# Project Structure

The project is structured as follows:

1. **github\workflows**: This directory contains the yaml files for CI configuration and CD configuration.
2. **/templates:** This directory contains the static HTML and CSS files for the web application's user interface.
3. **app.py:** This file defines the Flask application and runs the web server.
4. **app_test.py:** this file contains the unit test for each method (using pytest).>
5. **Dockerfile**: file that create the image of the APP to be deployed in a environment where docker is available.
6. **requirements.txt** : file that contains all the dependency needed by the project.
## Project Deployment Workflow

The following diagram describe the high level architecture of the Application and the CI/CD process:

![](https://github.com/matiaspakua/ml-demo-project/blob/595a2ebac6d0ec0e2d49d64d78ba06951692cab6/images/ML-Demo-project.png)
### Step 01
The code for the app is stored in a GitHub repository, which allows for easy version control and collaboration. The app is automatically build and test in a github workflow. 

[Link to YML: python-app.yml](https://github.com/matiaspakua/ml-demo-project/blob/189d424ad72ed630ede8a489aa8804dd2a153403/.github/workflows/python-app.yml)

### Step 02
Then a docker image is create and pushed in DockerHub public repository in another workflow. 

[Link to YML: docker-image.yml](https://github.com/matiaspakua/ml-demo-project/blob/189d424ad72ed630ede8a489aa8804dd2a153403/.github/workflows/docker-image.yml)

### Step 03
A third workflow is executed when the first two are executed successfully and the image is pulled and deployed in a AWS Ubuntu EC2 instance.

[Link to YML: docker-run.yml](https://github.com/matiaspakua/ml-demo-project/blob/189d424ad72ed630ede8a489aa8804dd2a153403/.github/workflows/docker-run.yml)

![](https://github.com/matiaspakua/ml-demo-project/blob/595a2ebac6d0ec0e2d49d64d78ba06951692cab6/images/docker_hub_image_push.png)

### Step 04

Validate that the workflows works properly:

![](https://github.com/matiaspakua/ml-demo-project/blob/9b3386851c91e22ca4bbfdb473904c94de1dbc81/images/repository_workflows.png)

### Step 05

The last step is wait until the image is pulled and running in the EC2 Ubuntu instance and access the public URL to log into the landing page of the app:

[Landing page on EC2 instance](http://ec2-54-227-35-67.compute-1.amazonaws.com:8080/)

![](https://github.com/matiaspakua/ml-demo-project/blob/9b3386851c91e22ca4bbfdb473904c94de1dbc81/images/ml_demo_landing_page.png)

## Project Setup and Deployment

## Setup

1. Install Python v3.11 (does not work with python 3.12)
2. Install Docker
3. Install Git and create a github account. Configure credential and SSH connection.
4. Execute first time in the console:

```bash
 matias@ml-demo-project$ pip install -r requirements.txt 
```

5. validate that all the dependencies listed in the "requirements.txt" are properly installed.

### Setup AWS EC2 instance

Launch new instance of EC2 with Ubuntu 20.04, using all the default parameters of the Free-Tier.

![](https://github.com/matiaspakua/ml-demo-project/blob/9b3386851c91e22ca4bbfdb473904c94de1dbc81/images/aws_ec2_ubuntu_instance.png)
![]()

Ensure that you enable all the traffic (in and out) for testing purposes:

![](https://github.com/matiaspakua/ml-demo-project/blob/9b3386851c91e22ca4bbfdb473904c94de1dbc81/images/aws_ec2_instance_creation.png)

### Install docker in Ubuntu 20.04 instance:

Follow the next instructions to install docker on the Ubuntu instance.
 - https://linux.how2shout.com/how-to-install-docker-on-aws-ec2-ubuntu-22-04-or-20-04-linux/

After the installation, verify that docker is properly configured and running:

![](https://github.com/matiaspakua/ml-demo-project/blob/9b3386851c91e22ca4bbfdb473904c94de1dbc81/images/aws_ec2_instance_docker_installed.png)
### Configure GitHub Action Runner for Workflow

After the EC2 instance is properly up and running with docker, is needed to configure the workflows and runners in github to communicate to EC2 to pull and run the builded image of the application from a public repository, in this case: DockerHub.

To do this, follow the instructions on the github actions section:

![](https://github.com/matiaspakua/ml-demo-project/blob/9b3386851c91e22ca4bbfdb473904c94de1dbc81/images/github_runner_installation.png)

After installed the runner daemon in the EC2 Ubuntu instance, validate that is properly installed and running in background:

![](https://github.com/matiaspakua/ml-demo-project/blob/9b3386851c91e22ca4bbfdb473904c94de1dbc81/images/github_runner_folder_installation.png)

Verify is running:

![](https://github.com/matiaspakua/ml-demo-project/blob/9b3386851c91e22ca4bbfdb473904c94de1dbc81/images/github_runner_running.png)

## Development

The development flow need to follow the best practices:

1. Clean code
2. Modularity
3. Cohesion
4. Testing
5. Commit (small) to a version control.
6. Verify CI
7. Verify CD
8. Integration / acceptance testing
9. Documentation.

## Unit Testing with Pytest

The project comes with a very basic unit test in the file: "app_test.py".

To execute the tests and view the report, prompt the following:

```bash
$ pytest.exe -vv --html=report.html app_test.py
```

This command will execute and generate a HTML report as follow:

![[pytest_console_execution.png]]

The report can be opened with any browser:

![[pytest_report.png]]

And even, the test execution and result can be monitored in the GitHub Action Pipeline:

![[pytest_ci_build_execution.png]]

## Acceptance Testing

For the validation of the current application exits a series of images in the folder: **/images/test/** that can be used to "acceptance testing" as follow:

| Test Case | Test input Images | Expected Restult |
| ---- | ---- | ---- |
| 01 | image.jpg | solar_dish<br><br>0.7601 |
| 02 | image1.jpg | boathouse<br><br>0.2617 |
| 03 | image2.jpg | tabby<br><br>0.2365 |
| 04 | image3.jpg | sports_car<br><br>0.5183 |
| 05 | image4.jpg | dining_table<br><br>0.3249 |


Each result gives 3 matches from the highest to the lowest probability of similarity, like the following example:

![](https://github.com/matiaspakua/ml-demo-project/blob/9b3386851c91e22ca4bbfdb473904c94de1dbc81/images/images_probability_result.png)