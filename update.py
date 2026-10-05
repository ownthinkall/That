import base64
import urllib.request
import re

# لینک A از Secrets خوانده می‌شود
SOURCE_URL = "https://bujidao.cc/sub?key=wzrXMqjCUiTFYhWC80bLfCSJEVFExXhe"

def fetch_and_convert():
    # ۱. دریافت محتوای لینک A
    req = urllib.request.Request(SOURCE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode('utf-8').strip()

    # ۲. دیکد کردن Base64
    try:
        decoded = base64.b64decode(raw).decode('utf-8')
    except Exception:
        decoded = raw  # شاید از قبل decode شده باشد

    # ۳. پردازش هر خط
    lines = decoded.splitlines()
    new_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # حذف نام قدیمی (بعد از #) و جایگزینی با H
        if '#' in line:
            line = line.split('#')[0] + '#H'
        else:
            line = line + '#H'
        new_lines.append(line)

    # ۴. دوباره Base64 encode
    final_text = '\n'.join(new_lines)
    encoded = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')

    # ۵. ذخیره در فایل خروجی
    with open('sub.txt', 'w') as f:
        f.write(encoded)
    print("Done. Output saved to sub.txt")

if __name__ == '__main__':
    fetch_and_convert()
