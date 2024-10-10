all: run

build:
	docker build -t csr/admin .

run:
	docker run -it --rm \
		-v $(PWD)/admin.py:/admin.py \
		-v /var/run/docker.sock:/var/run/docker.sock csr/admin
