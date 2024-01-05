setup:
    @echo "Creating a Python virtual environment..."
	python -m venv ~/.flask-ml-demo

    @echo "WINDOWS Activating the virtual environment..."	
	source ~/.flask-ml-demo/Scripts/activate
	
	@echo "LINUX Activating the virtual environment..."
	source flask-ml-demo/bin/activate

install:
	@echo "Install process: upgrade and install requirements..."
	pip install --upgrade pip &&\
	pip install -r requirements.txt

test:
	@echo "Unit Test execution..."
	python -m pytest -vv app_test.py

format:
	@echo "Files formar according to black library conventions..."
	black *.py

lint:
	@echo "Files linting..."
	pylint --disable=R,C,W1203,W0702 *.py

docker-build:
	docker build -t ml-demo-project .

docker-run:
	docker run -p 8080:8080 ml-demo-project-app

docker-debug:
	docker run -d -p 8080:8080 --name ml-demo-project-container ml-demo-project-app
	docker exec -it ml-demo-project-container bash

docker-clean:	
	if [ -n "$$(docker images -aq)" ]; then \
		docker rmi -f $$(docker images -aq); \
	fi

all: install format lint test
