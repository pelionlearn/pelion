from time import sleep
import requests

response = requests.post(
    "http://localhost:5000/coref/submit",
    json={"text": "Steve is very cool. He is very strong."},
)
response = response.json()
print(response)

task_id = response["task_id"]

while True:
    response = requests.get(f"http://localhost:5000/coref/status/{task_id}")
    print(response.content)
    # response = response.json()
    # print(response)
    sleep(3)
