DOCKER_IMAGE=docker.ds-wizard.org/template-editor-expander-server

.PHONY: install
install:
	pip install -r requirements.txt
	pip install -e .


.PHONY: docker.build
docker.build:
	docker build -t $(DOCKER_IMAGE) .


.PHONY: docker.push
docker.push:
	docker push $(DOCKER_IMAGE)


.PHONY: docker.all
docker.all:
	make docker.build && make docker.push
