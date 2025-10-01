# Deployment

<p style='text-align:right'>Ken Pu, 2025-09-30</p>

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
- GPUs should be specified using the `device_ids` as an array of strings.

# CSR admin

## Installation

```
cd csr_admin
make install
```

## Tools

```
csr list
```

```
$ csr create <proj>/<host> --image csr/base --ssh 8040 --cpus 16 --ram 8G --data /data --postgres
$ cd /data/<proj>/<host>
```

Edit `users`

```
$ make ...
```