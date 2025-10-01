import docker
from tabulate import tabulate

def command():
    client = docker.from_env()
    containers = client.containers.list()
    table_data = []
    headers = ["Container Name", "Container ID", "GPUs", "CPU Limit", "Memory Limit (MB)", "Ports"]

    for container in containers:
        container_name = container.name
        container_id = container.id[:12]  # First 12 characters for brevity
        attrs = container.attrs
        gpu_devices = []

        # Check HostConfig for DeviceRequests (used with --gpus option)
        host_config = attrs.get('HostConfig', {})
        device_requests = host_config.get('DeviceRequests', []) or []
        for request in device_requests:
            capabilities = request.get('Capabilities', [])
            # Capabilities is a list of lists
            if any('gpu' in cap for cap in capabilities):
                device_ids = request.get('DeviceIDs')
                if device_ids:
                    gpu_devices.extend(device_ids)
                else:
                    count = request.get('Count', 0)
                    if count == -1:
                        gpu_devices.append('all')
                    else:
                        gpu_devices.extend(str(i) for i in range(count))

        # Check Config Env for NVIDIA_VISIBLE_DEVICES (legacy method)
        config = attrs.get('Config', {})
        env_vars = config.get('Env', [])
        for env_var in env_vars:
            if env_var.startswith('NVIDIA_VISIBLE_DEVICES='):
                devices = env_var.split('=', 1)[1].split(',')
                gpu_devices.extend(devices)

        # Check HostConfig for Devices (manual device mapping)
        devices = host_config.get('Devices', []) or []
        for device in devices:
            host_path = device.get('PathOnHost')
            if host_path and '/dev/nvidia' in host_path:
                gpu_devices.append(host_path)

        # Remove duplicates and format the GPU devices
        gpu_devices = list(set(gpu_devices))
        if gpu_devices:
            gpu_info = ', '.join(gpu_devices)
        else:
            gpu_info = "None"

        # Get CPU and Memory limits
        cpu_quota = host_config.get('CpuQuota', None)
        cpu_period = host_config.get('CpuPeriod', None)
        cpu_limit = None
        if cpu_quota and cpu_period and cpu_period > 0:
            cpu_limit = cpu_quota / cpu_period
        elif host_config.get('NanoCpus'):
            cpu_limit = host_config.get('NanoCpus') / 1e9  # Convert from nanocpus to cpus

        cpu_shares = host_config.get('CpuShares', None)  # Relative weight (not a hard limit)

        memory_limit = host_config.get('Memory', None)  # In bytes
        if memory_limit and memory_limit > 0:
            memory_limit_mb = memory_limit / (1024 * 1024)  # Convert to MB
            mem_info = f"{memory_limit_mb:.2f}"
        else:
            mem_info = "None"

        # Prepare CPU info
        if cpu_limit:
            cpu_info = f"{cpu_limit} CPUs"
        elif cpu_shares:
            cpu_info = f"Shares: {cpu_shares}"
        else:
            cpu_info = "None"

        # Get exposed ports
        network_settings = attrs.get('NetworkSettings', {})
        ports_info = network_settings.get('Ports', {})
        ports = []

        for container_port, host_bindings in ports_info.items():
            if host_bindings:
                for binding in host_bindings:
                    host_ip = binding.get('HostIp', '')
                    host_port = binding.get('HostPort', '')
                    if host_ip:
                        port_mapping = f"{host_ip}:{host_port}->{container_port}"
                    else:
                        port_mapping = f"{host_port}->{container_port}"
                    ports.append(port_mapping)
            else:
                # Port is exposed but not published
                ports.append(f"{container_port} (exposed)")

        if ports:
            ports_info_str = ', '.join(ports)
        else:
            ports_info_str = "None"

        table_data.append([container_name, container_id, gpu_info, cpu_info, mem_info, ports_info_str])
    print(tabulate(table_data, headers=headers, tablefmt="grid"))