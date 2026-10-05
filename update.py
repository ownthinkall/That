import base64
import urllib.request
import os

SOURCE_URL = os.environ.get('SOURCE_URL')

def fetch_and_convert():
    req = urllib.request.Request(SOURCE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode('utf-8').strip()

    try:
        decoded = base64.b64decode(raw).decode('utf-8')
    except Exception:
        decoded = raw

    lines = decoded.splitlines()
    new_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if '#' in line:
            line = line.split('#')[0] + '#H'
        else:
            line = line + '#H'
        new_lines.append(line)

    final_text = '\n'.join(new_lines)
    encoded = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')

    with open('sub.txt', 'w') as f:
        f.write(encoded)
    print("Done. Output saved to sub.txt")

if __name__ == '__main__':
    fetch_and_convert()
