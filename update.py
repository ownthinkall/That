import base64
import urllib.request
import os
import re

SOURCE_URL = os.environ.get('SOURCE_URL')

# نقشه پیشوند -> (نام کشور, پرچم)
COUNTRY_MAP = {
    'uk': ('England', '🏴󠁧󠁢󠁥󠁮󠁧󠁿'),
    'ca': ('Canada', '🇨🇦'),
    'fr': ('France', '🇫🇷'),
    'tk': ('Tokyo', '🇯🇵'),
    'us': ('USA', '🇺🇸'),
    'de': ('Germany', '🇩🇪'),
    'nl': ('Netherlands', '🇳🇱'),
    'jp': ('Japan', '🇯🇵'),
    'ir': ('Iran', '🇮🇷'),
    'ru': ('Russia', '🇷🇺'),
    'in': ('India', '🇮🇳'),
    'sg': ('Singapore', '🇸🇬'),
    'ae': ('UAE', '🇦🇪'),
}

def make_name(host):
    m = re.match(r'([a-zA-Z]+)[-_]?([xX]?\d+)?', host)
    if not m:
        return 'H'

    prefix = m.group(1).lower()
    number = m.group(2) if m.group(2) else ''

    if number.lower().startswith('x'):
        number = number[1:]

    if prefix in COUNTRY_MAP:
        country, flag = COUNTRY_MAP[prefix]
        return f"{country} {number} {flag}".strip()
    else:
        return f"{prefix.upper()} {number}".strip()


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

        m = re.search(r'@([^:/?#]+)', line)
        host = m.group(1) if m else ''

        new_name = make_name(host)

        if '#' in line:
            line = line.split('#')[0] + '#' + new_name
        else:
            line = line + '#' + new_name

        new_lines.append(line)

    final_text = '\n'.join(new_lines)
    encoded = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')

    with open('sub.txt', 'w') as f:
        f.write(encoded)
    print("Done. Output saved to sub.txt")


if __name__ == '__main__':
    fetch_and_convert()
