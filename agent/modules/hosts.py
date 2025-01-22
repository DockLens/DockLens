import psutil
import socket
import requests
import hashlib
from ..config import API_URL


URL = f"{API_URL}/hosts/cpu"


def get_system_info():
    hostname = socket.gethostname()
    cpu_usage = psutil.cpu_percent()

    # RAM information
    ram_total = psutil.virtual_memory().total
    ram_total_gb = int(ram_total / (1024**2))  # Convert to GB and remove decimal
    ram_usage = psutil.virtual_memory().used
    ram_usage_gb = int(ram_usage / (1024**2))  # Convert to GB and remove decimal

    # Disk information
    disk_total = psutil.disk_usage("/").total
    disk_total_gb = int(disk_total / (1024**3))  # Convert to GB and remove decimal
    disk_usage = psutil.disk_usage("/").used
    disk_usage_gb = int(disk_usage / (1024**3))  # Convert to GB and remove decimal

    host_info = {
        "hostname": hostname,
        "cpu_usage": cpu_usage,
        "ram_total": ram_total_gb,
        "ram_usage": ram_usage_gb,
        "disk_total": disk_total_gb,
        "disk_usage": disk_usage_gb,
    }

    return host_info


def send_data(host_info):
    try:
        response = requests.post(URL, json=host_info)
        response.raise_for_status()
        print(f"Data info system sent for host: {host_info['hostname']}")

    except requests.RequestException as e:
        print(f"Failed to send data for host: {e}")
