import secrets
import json

# 400~499 플래그 생성
flags = {
    code: f"CTF{{{code}_{secrets.token_hex(8)}}}" 
    for code in range(400, 500)
}

# JSON으로 저장
with open('flags.json', 'w', encoding='utf-8') as f:
    json.dump(flags, f, ensure_ascii=False, indent=2)

print("flags.json 파일을 생성했습니다.")
