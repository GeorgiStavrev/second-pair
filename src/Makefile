.EXPORT_ALL_VARIABLES:

# Local Development
install:
	pip install -r requirements.txt
install-dev:
	pip install -r dev-requirements.txt
lint:
	flake8 .
format:
	black .
run:
	ENV=local python app.py

# Google Cloud Run deployment
deploy:
	source set_env.sh && ./build_and_deploy.sh

# AWS ECR/ECS Deployment
deploy-aws-test:
	BUILD_ENV=test ./scripts/deploy.sh
deploy-aws-prod:
	BUILD_ENV=prod ./scripts/deploy.sh

remove-ecr-images-test:
	BUILD_ENV=test ./scripts/remove_images_from_ecr.sh

remove-ecr-images-prod:
	BUILD_ENV=prod ./scripts/remove_images_from_ecr.sh

# TESTS
test-dev:
	pytest -sv ./tests -k "dev"

test-prod:
	pytest -sv ./tests -k "prod"

test:
	pytest -sv ./test