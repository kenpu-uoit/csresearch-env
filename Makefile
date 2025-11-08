all:
	docker build -t csr/base ./docker
	docker build -t csr/postgres ./postgres_docker

run:
	docker run -it csr/base bash
