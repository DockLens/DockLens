import docker
import requests
import socket
from ..config import API_URL

URL = f"{API_URL}/containers/status"


# Fungsi untuk mengambil informasi kontainer dari Docker
def get_containers_info():
    client = docker.from_env()
    containers = client.containers.list(all=True)
    container_info = []
    for container in containers:
        info = {
            "hostname": socket.gethostname(),
            "container_id": container.id,
            "name": container.name,
            "status": container.status,
        }
        container_info.append(info)
    return container_info


# Fungsi untuk mengirim data ke API
def send_data(containers):
    for container in containers:
        try:
            response = requests.post(URL, json=container)
            response.raise_for_status()
            print(
                f"Data sent for container {container['name']} hostname {container['hostname']}"
            )
        except requests.RequestException as e:
            print(
                f"Failed to send data for container {container['name']} - hostname : {container['hostname']} : {e}"
            )
