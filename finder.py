import os
import sys
import requests
import time
import urllib3

subs = [
    ("sub1", "https://raw.githubusercontent.com/Ai123999/1Mond/refs/heads/main/1Mond_Notorgamers"),
    ("sub2", "https://raw.githubusercontent.com/Ai123999/2Tues/refs/heads/main/2Tues_Notorgamers"),
    ("sub3", "https://raw.githubusercontent.com/Ai123999/3Wend/refs/heads/main/3Wend_Notorgamers"),
    ("sub5", "https://raw.githubusercontent.com/Ai123999/5Frid/refs/heads/main/5Frid_Notorgamers"),
    ("sub6", "https://raw.githubusercontent.com/Ai123999/6Satu/refs/heads/main/6Satu_Notorgamers"),
    ("sub7", "https://raw.githubusercontent.com/Ai123999/7Sand/refs/heads/main/7Sand_Notorgamers"),
    ("whitelist", "https://raw.githubusercontent.com/Ai123999/WhiteeListSub/refs/heads/main/whitelistkeys"),
    ("whitekey", "https://raw.githubusercontent.com/Ai123999/WhiteKeys/refs/heads/main/WhiteKeys")
]

def clear():
    os.system('clear')

def red(text):
    return f"\033[91m{text}\033[0m"

def green(text):
    return f"\033[92m{text}\033[0m"

def yellow(text):
    return f"\033[93m{text}\033[0m"

def banner():
    clear()
    print(red("╔══════════════════════════════════════╗"))
    print(red("║                                      ║"))
    print(red("║           Created By Red             ║"))
    print(red("║    Telegram: t.me/Red_Rooted_ghost   ║"))
    print(red("║                                      ║"))
    print(red("╚══════════════════════════════════════╝"))
    print()

def ask_overwrite(filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        print(yellow(f"  File {filename} already has configs."))
        while True:
            choice = input("  Do you want to overwrite it? (Y/N): ").strip().upper()
            if choice == 'Y':
                return True
            elif choice == 'N':
                return False
            else:
                print(red("  Please enter Y or N."))
    return True

def create_files():
    for name, _ in subs:
        filename = f"{name}.txt"
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write("")

def download_sub(name, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    for attempt in range(1, 4):
        try:
            session = requests.Session()
            session.verify = False
            response = session.get(url, headers=headers, timeout=30)

            if response.status_code == 200:
                content = response.text
                if content:
                    lines = content.split('\n')
                    configs = []
                    for line in lines:
                        line = line.strip()
                        if line:
                            configs.append(line)

                    if configs:
                        filename = f"{name}.txt"
                        with open(filename, 'w') as f:
                            f.write('\n'.join(configs))
                        return True, len(configs)
                    else:
                        return False, 0
                else:
                    return False, 0
            elif attempt < 3:
                wait_time = attempt * 3
                time.sleep(wait_time)
                continue
            else:
                return False, 0

        except requests.exceptions.Timeout:
            if attempt < 3:
                time.sleep(10)
                continue
            return False, 0
        except requests.exceptions.ConnectionError:
            if attempt < 3:
                time.sleep(5)
                continue
            return False, 0
        except Exception:
            if attempt < 3:
                time.sleep(5)
                continue
            return False, 0

    return False, 0

def retry_failed():
    failed = []
    for name, url in subs:
        filename = f"{name}.txt"
        if os.path.exists(filename) and os.path.getsize(filename) == 0:
            failed.append((name, url))

    if not failed:
        return 0, 0

    print()
    print(yellow("[*] Retrying failed downloads..."))
    print()

    success_count = 0
    fail_count = 0

    for i, (name, url) in enumerate(failed, 1):
        print(f"[{i}/{len(failed)}] Retrying {name}...", end=' ', flush=True)

        success, count = download_sub(name, url)

        if success:
            if count > 0:
                print(green(f"✓ {count} configs"))
                success_count += 1
            else:
                print(red("✗ Still empty"))
                fail_count += 1
        else:
            print(red("✗ Connection failed"))
            fail_count += 1

        time.sleep(2)

    return success_count, fail_count

def main():
    banner()

    if not os.path.exists('configs'):
        os.makedirs('configs')

    os.chdir('configs')

    print(yellow("[*] Checking existing files..."))
    create_files()
    print(green("✓ All files checked successfully"))
    print()

    total_subs = len(subs)
    success_count = 0
    fail_count = 0
    skip_count = 0

    print(yellow("[*] Starting update process..."))
    print()

    for i, (name, url) in enumerate(subs, 1):
        filename = f"{name}.txt"
        print(f"[{i}/{total_subs}] Checking {name}...")

        if not ask_overwrite(filename):
            print(yellow(f"  Skipping {name}"))
            skip_count += 1
            print()
            continue

        print(f"  Downloading {name}...", end=' ', flush=True)
        success, count = download_sub(name, url)

        if success:
            if count > 0:
                print(green(f"✓ {count} configs"))
                success_count += 1
            else:
                print(yellow("⚠ No configs found"))
                fail_count += 1
        else:
            print(red("✗ Connection failed"))
            fail_count += 1

        print()
        time.sleep(1)

    retry_success, retry_fail = retry_failed()
    success_count += retry_success
    fail_count += retry_fail

    print()
    print(green("═" * 40))
    if success_count > 0:
        print(green(f"✓ Updated: {success_count} files"))
    if skip_count > 0:
        print(yellow(f"⚠ Skipped: {skip_count} files"))
    if fail_count > 0:
        print(red(f"✗ Failed: {fail_count} files"))
    print(green("═" * 40))
    print()
    print(yellow("All configs saved in: configs/ folder"))
    print()

    print(yellow("[*] Files in configs folder:"))
    files = [f for f in os.listdir('.') if f.endswith('.txt')]
    files.sort()

    for file in files:
        size = os.path.getsize(file)
        if size > 0:
            print(green(f"  {file} ({size} bytes)"))
        else:
            print(red(f"  {file} (empty)"))

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        test = requests.get("https://raw.githubusercontent.com", timeout=5, verify=False)
    except:
        print(red("⚠ No internet connection or GitHub is blocked"))
        print(red("  Please check your connection and try again"))
        sys.exit(1)

    main()
