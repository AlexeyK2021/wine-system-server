from config import API_PORT
import requests

API_URL = f"http://127.0.0.1:{API_PORT}/api/"

if __name__ == '__main__':
    result = requests.get(API_URL + f"process/start/tank=1&login=admin")
    print(result)
