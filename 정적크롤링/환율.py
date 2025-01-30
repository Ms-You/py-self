import requests as req
import re

url = "https://finance.naver.com/marketindex/?tabSel=exchange#tab_section"
res = req.get(url)
html = res.text

r = re.compile(r"h_lst.*?blind\">(.*?)</span>.*?value\">(.*?)</", re.DOTALL)
captures = r.findall(html)

print("========")
print("환율 계산기")
print("========")

for c in captures:
    print(c[0], ": ", c[1])

print()
usd = float(captures[0][1].replace(",", ""))
won = int(input("달러로 바꾸길 원하는 금액(원)을 입력해주세요: "))
dollar = int(won/usd)
print(f"{dollar} 달러 환전되었습니다.")
