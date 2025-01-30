import re

s = 'hello, world'
print(re.match(r'hello, world', s)) # 일치하지 않은 경우 None
print(re.match(r'hello.', s)) # . : 아무거나
print(re.match(r'hello9*', s)) # * : 바로 앞에 있는 문자가 0개 이상 있을 수 있다.
print(re.match(r'hello+', s)) # + : 바로 앞에 있는 문자가 1개 이상 있을 수 있다.
print(re.match(r'hello, (python)?', s)) # ? : 바로 앞에 있는 문자가 없을 수 있다.

s = '이 영화는 A등급 입니다.'
print(re.match(r'이 영화는 [ABCD]등급 입니다', s))
print(re.findall(r'이 (..)는 (.)등급 입니다', s))