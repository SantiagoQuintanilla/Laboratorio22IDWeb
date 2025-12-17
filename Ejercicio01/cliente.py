import requests

r = requests.get("https://httpbin.org/get")

data = r.json()

print("IP:")
print(data["origin"])

print("\nHEADERS:")
print(data["headers"])

print("\nARGS:")
print(data["args"])