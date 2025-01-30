# HTTP 통신을 위한 파이썬 패키지
import requests

res = requests.get("https://google.com/")
print(res.status_code)
print(res.headers['content-type'])
print(res.cookies)

# 보낸 요청에 대해
print(res.request.method)
print(res.request.headers)