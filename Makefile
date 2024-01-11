setup:
	@echo "Creating a Python virtual environment..."
	python -m venv ~/.flask-ml-demo

	@echo "WINDOWS Activating the virtual environment..."	
	source ~/.flask-ml-demo/Scripts/activate
	
	@echo "LINUX Activating the virtual environment..."
	@source flask-ml-demo/bin/activate

install:
	@echo "Install process: upgrade and install requirements..."
	pip install --upgrade pip &&\
	pip install -r requirements.txt

test:
	@echo "Unit Test execution..."
	python -m pytest -vv --html=report.html app_test.py

format:
	@echo "Files formar according to black library conventions..."
	black *.py

lint:
	@echo "Files linting..."
	pylint --disable=R,C,W1203,W0702 *.py

docker-build:
	@echo "Docker build image..."
	docker build -t ml-demo-project .

docker-run:
	@echo "Docker run image at port 8080..."
	docker run -p 8080:8080 ml-demo-project-app

docker-debug:
	@echo "Docker run and open IT console for degug..."
	docker run -d -p 8080:8080 --name ml-demo-project-container ml-demo-project-app
	docker exec -it ml-demo-project-container bash

docker-clean:
	@echo "Docker image clean..."
	if [ -n "$$(docker images -aq)" ]; then \
		docker rmi -f $$(docker images -aq); \
	fi

all: install format lint test
