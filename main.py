import time
import ctypes
import requests
import datetime

from datetime import datetime
from colorama import Fore

ctypes.windll.kernel32.SetConsoleTitleW(f'PAI Price Alert | ')

def alert(old_fdv, new_fdv):
    HOOK = "https://discord.com/api/webhooks/1258469059586949151/lcfeXAepWwBm6NI8JrA74LW0NObah6kA82zpPieUq9UPWRgDuV5vHWZIYMwFNsZU_K1g"
    
    try:
        embed = {
            "title": "🔔",
            "description": "$PAI MCAP Dropped by 100k",
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "footer": {
                "text": "MCAP Monitor"
            },
            "fields": [
                {
                    "name": "> Old MCAP",
                    "value": f"`{old_fdv}`",
                    "inline": False
                },
                {
                    "name": "> New MCAP",
                    "value": f"`{new_fdv}`",
                    "inline": False
                }
            ]
        }
        
        payload = {'embeds': [embed]}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(HOOK, json=payload, headers=headers)
        response.raise_for_status()

        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d | %H:%M:%S")  
        print(f"{Fore.GREEN}[{Fore.RESET}{current_time}{Fore.GREEN}]{Fore.RESET} PINGED ON DISCORD :)")

    except requests.exceptions.RequestException as e:
        print(e)

def checkFDV():
    CA = "ekem8tctl4ezbcjzmhk6roqq6krkwbbdwgr3dxwiwzei"
    URL = f"https://api.dexscreener.com/latest/dex/pairs/solana/{CA}"

    while True:
        sub = 100000
        r = requests.get(URL)
        if r.status_code == 200:
            data = r.json()
            pairs = data.get("pairs")
            fdv = pairs[0].get('fdv')

            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d | %H:%M:%S")
            print(f"{Fore.MAGENTA}[{Fore.RESET}{current_time}{Fore.MAGENTA}]{Fore.RESET} {fdv}")
            ctypes.windll.kernel32.SetConsoleTitleW(f'PAI Price Alert | {fdv}')

            old_fdv = fdv
            new_fdv = pairs[0].get('fdv')
            if fdv < new_fdv - sub:
                print(f"{Fore.GREEN}[{Fore.RESET}{current_time}{Fore.GREEN}]{Fore.RESET} DROPPED BY 100K => {fdv}")
                alert(old_fdv, new_fdv)
                ctypes.windll.kernel32.SetConsoleTitleW(f'PAI Price Alert | {fdv}')
            else:
                print(f"{Fore.GREEN}[{Fore.RESET}{current_time}{Fore.GREEN}]{Fore.RESET} FDV HASN'T DROPPED YET - WAITING...")
                print('')
        time.sleep(3600)

checkFDV()
