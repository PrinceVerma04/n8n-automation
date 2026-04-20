# import requests


# user_message = "Can you tell me about black holes in 3-4 lines"

# request_message = {"message": user_message}

# url = "http://localhost:5678/webhook-test/6a793279-70ee-4c4b-a044-e1f53553ff02"

# response = requests.post(url, json=request_message)

# print(response.status_code)

# print(response.json()[0]["output"])

import requests


user_message = "add another file with name Prince_no_more and add this in file Despacito Quiero respirar tu cuello despacito Deja que te diga cosas al oído…"

request_message = {"message": user_message}

url = "http://localhost:5678/webhook/6a793279-70ee-4c4b-a044-e1f53553ff02"

response = requests.post(url, json=request_message)

print("Status Code:", response.status_code)
print("Response Text:", response.text)
print("Response Headers:", response.headers)

if response.text:
    try:
        print("Response JSON:", response.json())
    except Exception as e:
        print("Error parsing JSON:", e)
else:
    print("Response body is empty")