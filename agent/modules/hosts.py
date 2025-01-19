import psutil
import socket
import requests
import hashlib
from ..config import API_URL

hostname_id = socket.gethostname()

URL = f"{API_URL}/hosts/cpu"


# Fungsi untuk mengambil informasi kontainer dari Docker
def get_cpu_percentage():
    cpu_percentage = psutil.cpu_percent()
    hsn = hostname_id

    cpu_info = {"hostname": hsn, "percentage": cpu_percentage}

    return cpu_info


# Fungsi untuk mengirim data ke API
def send_data(cpu_info):
    try:
        response = requests.post(URL, json=cpu_info)
        response.raise_for_status()
        print(f"Data sent for CPU: {cpu_info['percentage']}")

    except requests.RequestException as e:
        print(f"Failed to send data for CPU: {e}")
