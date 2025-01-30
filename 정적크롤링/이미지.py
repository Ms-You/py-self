import requests as req

url = "https://api.imgur.com/3/upload?client_id=546c25a59c58ad7"

# f = open("./크롤링/image.jpg", "rb") # read binary
# img = f.read()
# f.close()

with open("./크롤링/image.jpg", "rb") as f:
    img = f.read()

res = req.post(url, files={
    "image": img,
    "type": "file",
    "name": "./크롤링/image.jpg"
})

# print(res.status_code)
# print(res.text)

link = res.json()["data"]["link"]
print(link)
