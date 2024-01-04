# ml-demo-project

This is the demostration project for the Specialization Building Cloud Computing Solutions at Scale by Noah Gift.

# Description

## Deploy a simple Flask app into AWS.

1. Python Flask app that can load the model and make predictions on images.  reference: https://dev.to/dishant2001/deploy-your-deep-learning-model-with-flask-on-aws-ec2-instance-5h34

## Configure a model to generate preditions 

2. use a model TensorFlow Hub image classifier model: https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/classification/5

3. Dockerfile to containerize Flask app and the model.  reference: https://github.com/epigramai/tf-serving-flask-app/blob/master/Dockerfile

https://www.coursera.org/learn/cloud-virtualization-containers-api-duke/lecture/ASOnh/push-to-project-to-aws-ecr-registry

4. Push Docker image to a registry  Amazon Elastic Container Registry (Amazon ECR).
5. Deploy Docker image to AWS using Amazon Elastic Container Service (Amazon ECS) or Amazon Elastic Kubernetes Service (Amazon EKS).  reference: https://aws.amazon.com/blogs/opensource/deploying-python-flask-microservices-to-aws-using-open-source-tools/
6. simple web-based interface that can send images to your Flask API and display the predictions. reference: https://github.com/epigramai/tf-serving-flask-app/blob/master/templates/index.html
