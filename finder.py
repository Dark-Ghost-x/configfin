import os
import sys
import requests
import time
import urllib3
import concurrent.futures

subs = [
    ("sub1", "https://raw.githubusercontent.com/Ai123999/1Mond/refs/heads/main/1Mond_Notorgamers"),
    ("sub2", "https://raw.githubusercontent.com/Ai123999/2Tues/refs/heads/main/2Tues_Notorgamers"),
    ("sub3", "https://raw.githubusercontent.com/Ai123999/3Wend/refs/heads/main/3Wend_Notorgamers"),
    ("sub5", "https://raw.githubusercontent.com/Ai123999/5Frid/refs/heads/main/5Frid_Notorgamers"),
    ("sub6", "https://raw.githubusercontent.com/Ai123999/6Satu/refs/heads/main/6Satu_Notorgamers"),
    ("sub7", "https://raw.githubusercontent.com/Ai123999/7Sand/refs/heads/main/7Sand_Notorgamers"),
    ("whitelist", "https://raw.githubusercontent.com/Ai123999/WhiteeListSub/refs/heads/main/whitelistkeys"),
    ("whitekey", "https://raw.githubusercontent.com/Ai123999/WhiteKeys/refs/heads/main/WhiteKeys"),
    ("vmess", "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vmess.txt"),
    ("vless", "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt"),
    ("trojan", "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/trojan.txt"),
    ("ss", "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/ss.txt"),
    ("ssr", "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/ssr.txt")
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

def ask_clear_all():
    print(yellow("[*] For updating configs, do you want to delete ALL config files?"))
    print(yellow("    This will DELETE all .txt files and create new ones."))
    while True:
        choice = input("    Delete all config files? (Y/N): ").strip().upper()
        if choice == 'Y':
            return True
        elif choice == 'N':
            return False
        else:
            print(red("    Please enter Y or N."))

def delete_all_txt_files():
    txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
    deleted_count = 0
    for file in txt_files:
        try:
            os.remove(file)
            deleted_count += 1
        except:
            pass
    return deleted_count

def download_single_sub(args):
    name, url = args
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
            response = session.get(url, headers=headers, timeout=15)

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
                        return name, True, len(configs)
                    else:
                        filename = f"{name}.txt"
                        with open(filename, 'w') as f:
                            f.write('')
                        return name, False, 0
                else:
                    filename = f"{name}.txt"
                    with open(filename, 'w') as f:
                        f.write('')
                    return name, False, 0
            elif attempt < 3:
                time.sleep(1)
                continue
            else:
                filename = f"{name}.txt"
                with open(filename, 'w') as f:
                    f.write('')
                return name, False, 0

        except requests.exceptions.Timeout:
            if attempt < 3:
                time.sleep(2)
                continue
            filename = f"{name}.txt"
            with open(filename, 'w') as f:
                f.write('')
            return name, False, 0
        except requests.exceptions.ConnectionError:
            if attempt < 3:
                time.sleep(2)
                continue
            filename = f"{name}.txt"
            with open(filename, 'w') as f:
                f.write('')
            return name, False, 0
        except Exception:
            if attempt < 3:
                time.sleep(2)
                continue
            filename = f"{name}.txt"
            with open(filename, 'w') as f:
                f.write('')
            return name, False, 0

    filename = f"{name}.txt"
    with open(filename, 'w') as f:
        f.write('')
    return name, False, 0

def download_parallel():
    print(yellow("[*] Downloading configs in parallel..."))
    
    download_args = [(name, url) for name, url in subs]
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_name = {executor.submit(download_single_sub, args): args[0] for args in download_args}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_name), 1):
            name = future_to_name[future]
            try:
                result_name, success, count = future.result()
                results[result_name] = (success, count)
                
                if success:
                    if count > 0:
                        print(f"[{i}/{len(subs)}] {name}: {green(f'✓ {count} configs')}")
                    else:
                        print(f"[{i}/{len(subs)}] {name}: {yellow('⚠ Empty')}")
                else:
                    print(f"[{i}/{len(subs)}] {name}: {red('✗ Failed')}")
                    
            except Exception:
                results[name] = (False, 0)
                print(f"[{i}/{len(subs)}] {name}: {red('✗ Error')}")
    
    return results

def retry_failed_parallel(failed_subs):
    if not failed_subs:
        return 0, 0

    print()
    print(yellow("[*] Retrying failed downloads in parallel..."))
    print()

    download_args = [(name, url) for name, url in failed_subs]
    success_count = 0
    fail_count = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_name = {executor.submit(download_single_sub, args): args[0] for args in download_args}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_name), 1):
            name = future_to_name[future]
            try:
                result_name, success, count = future.result()
                
                if success:
                    if count > 0:
                        print(f"[{i}/{len(failed_subs)}] {name}: {green(f'✓ {count} configs')}")
                        success_count += 1
                    else:
                        print(f"[{i}/{len(failed_subs)}] {name}: {red('✗ Still empty')}")
                        fail_count += 1
                else:
                    print(f"[{i}/{len(failed_subs)}] {name}: {red('✗ Failed again')}")
                    fail_count += 1
                    
            except Exception:
                print(f"[{i}/{len(failed_subs)}] {name}: {red('✗ Error')}")
                fail_count += 1
    
    return success_count, fail_count

def main():
    banner()

    if not os.path.exists('configs'):
        os.makedirs('configs')

    os.chdir('configs')

    clear_all = ask_clear_all()
    if not clear_all:
        print()
        print(yellow("[!] Config update cancelled."))
        print(yellow("[!] Program will now exit."))
        print()
        sys.exit(0)

    print()
    print(yellow("[*] Deleting all .txt files..."))
    deleted = delete_all_txt_files()
    print(green(f"✓ Deleted {deleted} .txt files"))
    print()

    print(yellow("[*] Starting parallel download process..."))
    print()

    results = download_parallel()

    success_count = 0
    fail_count = 0
    failed_subs = []

    for name, (success, count) in results.items():
        if success and count > 0:
            success_count += 1
        else:
            fail_count += 1
            for sub_name, sub_url in subs:
                if sub_name == name:
                    failed_subs.append((name, sub_url))
                    break

    retry_success, retry_fail = retry_failed_parallel(failed_subs)
    success_count += retry_success
    fail_count = len(failed_subs) - retry_success

    print()
    print(green("═" * 40))
    if success_count > 0:
        print(green(f"✓ Downloaded: {success_count} files"))
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
