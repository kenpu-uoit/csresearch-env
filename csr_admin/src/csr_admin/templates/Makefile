PROJECT = "{{ project }}_{{ hostname }}"

start:
	docker compose -p $(PROJECT) up -d

stop:
	docker compose -p $(PROJECT) down

reboot:
	docker compose -p $(PROJECT) down
	docker compose -p $(PROJECT) up -d

check:
	docker compose -p $(PROJECT) exec -it research nvidia-smi
