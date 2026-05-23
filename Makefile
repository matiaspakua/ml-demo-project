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
	python -m pytest -vv --html=report.html tests/

format:
	@echo "Files formar according to black library conventions..."
	black src/ tests/

lint:
	@echo "Files linting..."
	pylint --disable=R,C,W1203,W0702 src/ tests/

docker-build:
	@echo "Docker build image..."
	docker build -t ml-demo-project .

docker-run:
	@echo "Docker run image at port 8111..."
	docker run -p 8111:8111 ml-demo-project

docker-debug:
	@echo "Docker run and open IT console for degug..."
	docker run -d -p 8111:8111 --name ml-demo-project-container ml-demo-project
	docker exec -it ml-demo-project-container bash

docker-clean:
	@echo "Docker image clean..."
	if [ -n "$$(docker images -aq)" ]; then \
		docker rmi -f $$(docker images -aq); \
	fi

all: install format lint test
