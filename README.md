# Python Flask ML Demo Project wi CI/CD

[![Python application](https://github.com/matiaspakua/ml-demo-project/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/matiaspakua/ml-demo-project/actions/workflows/python-app.yml)

This is the demonstration project for the Course - Duke university: **Specialization Building Cloud Computing Solutions at Scale** by Noah Gift.

# Project Overview

This project demonstrates how to develop a Flask web application for image classification using the MobileNetV2 pre-trained model from TensorFlow Hub. MobileNetV2 is a lightweight convolutional neural network (CNN) architecture, making it ideal for deploying on mobile devices and web applications.

The project utilizes the TensorFlow Hub library to load the pre-trained MobileNetV2 model and integrate it with the Flask application. Users can upload images to the application, which are then processed by the MobileNetV2 model to predict the class of the image. The predicted class is displayed to the user along with the model's confidence score.

# Project Structure

The project is structured as follows:

1. **.github:** This directory contains the yaml files for CI configuration and CD configuration.
    
2. **app_test.py:** this file contains the unit test for each method (using pytest).
    
3. **templates:** This directory contains the static HTML and CSS files for the web application's user interface.
    
4. **app.py:** This file defines the Flask application and runs the web server.
# Project Setup and Deployment
