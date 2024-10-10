# Deployment

<p style='text-align:right'>Ken Pu, 2024-10-09</p>

## Runtime

The runtime environment is expected to be `csr/base` or an image built from it.
It should be run in a NVIDIA enabled host OS.

The base image only exports the SSH port at 22.  Therefore, the runtime deployment should only map a single host port to container:22.

## Persistent storage

- Home directory should be a host directory mounted to `/home` inside the container.
- User definition file should be mounted to `/etc/users` inside the container.
- Any additional persistent data repository (shared across all users) should be mounted to well specified path inside the container.

## Resource limitation

- CPU, memory quota should be specified.
- GPUs should be specified.

## Sample `docker-compose.yaml`

```yaml
services:
  research-env-1:
    image: csr/base
    hostname: research-env-1
    ports:
      - "8022:22"
    volumes:
      - ./data/home:/home
      - ./data/users:/etc/users
    runtime: nvidia
    deploy:
      resources:
        limits:
          cpus: 8
          memory: 32G
        reservations:
          devices:
            - driver: nvidia
              count: 2
              capabilities: [gpu]
    environment:
      - NVIDIA_VISIBLE_DEVICES=0,2
```

## Maintenance

### Start

```sh
docker compose up -d
```

### Restart

```
docker compose down
docker compose up -d
```

### Dynamically adding new user

- Update `./data/users` with the new user.  (Old users cannot be deleted.)
- Login to the container (either through ssh or `docker exec`)
- run `/bin/createusers`