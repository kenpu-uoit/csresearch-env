all:
	docker build -t csr/base ./docker

run:
	docker run -it csr/base bash
