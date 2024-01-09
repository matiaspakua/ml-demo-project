# Python Flask ML Demo Project with CI/CD in AWS EC2

## CI Status (build and test)

[![ci-build-python-app](https://github.com/matiaspakua/ml-demo-project/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/matiaspakua/ml-demo-project/actions/workflows/python-app.yml)

## CD status (docker build and push in DockerHub)

[![cd-build-publish-docker-image](https://github.com/matiaspakua/ml-demo-project/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/matiaspakua/ml-demo-project/actions/workflows/docker-image.yml)

## CD Status (AWS EC2 docker pull and run)

[![run-docker-image](https://github.com/matiaspakua/ml-demo-project/actions/workflows/docker-run.yml/badge.svg?branch=main)](https://github.com/matiaspakua/ml-demo-project/actions/workflows/docker-run.yml)


# Project Overview

This is the demonstration project for the Course - Duke university: **Specialization Building Cloud Computing Solutions at Scale** by Noah Gift.

This project demonstrates how to develop a Flask web application for image classification using the MobileNetV2 pre-trained model from TensorFlow Hub. MobileNetV2 is a lightweight convolutional neural network (CNN) architecture, making it ideal for deploying on mobile devices and web applications.

The project utilizes the TensorFlow Hub library to load the pre-trained MobileNetV2 model and integrate it with the Flask application. Users can upload images to the application, which are then processed by the MobileNetV2 model to predict the class of the image. The predicted class is displayed to the user along with the model's confidence score.

# Project Structure

The project is structured as follows:

1. **github\workflows**: This directory contains the yaml files for CI configuration and CD configuration.
2. **/templates:** This directory contains the static HTML and CSS files for the web application's user interface.
3. **app.py:** This file defines the Flask application and runs the web server.
4. **app_test.py:** this file contains the unit test for each method (using pytest).>
5. **Dockerfile**: file that create the image of the APP to be deployed in a environment where docker is available.
6. **requirements.txt** : file that contains all the dependency needed by the project.
## Project Deployment Workflow

### Step 01
The code for the app is stored in a GitHub repository, which allows for easy version control and collaboration. The app is automatically build and test in a github workflow. 

[Link to YML: python-app.yml](https://github.com/matiaspakua/ml-demo-project/blob/189d424ad72ed630ede8a489aa8804dd2a153403/.github/workflows/python-app.yml)

### Step 02
Then a docker image is create and pushed in DockerHub public repository in another workflow. 

[Link to YML: docker-image.yml](https://github.com/matiaspakua/ml-demo-project/blob/189d424ad72ed630ede8a489aa8804dd2a153403/.github/workflows/docker-image.yml)


### Step 03
A third workflow is executed when the first two are executed successfully and the image is pulled and deployed in a AWS Ubuntu EC2 instance.

[Link to YML: docker-run.yml](https://github.com/matiaspakua/ml-demo-project/blob/189d424ad72ed630ede8a489aa8804dd2a153403/.github/workflows/docker-run.yml)

### Step 04

The last step is wait until the image is pulled and running in the EC2 Ubuntu instance and access the public URL to log into the landing page of the app:

[Landing page on EC2 instance]()

##  Project Setup and Deployment

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

Launch new instance of EC2 with Ubuntu 20.04.

### Install docker in Ubuntu 20.04 instance:

Follow the next instructions:
 - https://linux.how2shout.com/how-to-install-docker-on-aws-ec2-ubuntu-22-04-or-20-04-linux/

### Configure Github Action Runner for Workflow


## Development