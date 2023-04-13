# https://gist.github.com/GaryOderNichts/3f137c031c3617e513a67fff5780b76e
# https://gist.github.com/NWPlayer123/7e6233aee364796c55d85f143bba4bd1

# Import required libraries
import os, json
import ftputil
from struct import *

# Declare FTP variables
address = input("Enter the Wii U's IP address. Do not include the port.\n -> ")

# Declare other variables
titleurl = "/storage_mlc/usr/save/system/pdm/[userid]/"
titleurlnu = "/storage_mlc/usr/save/system/pdm/"

def file_check():

    if "saves" not in os.listdir():
        os.mkdir("saves")

    if "PlayStats.json" not in os.listdir():
        with open("PlayStats.json", 'w') as f:
            json.dump({"entry_count": 0, "entries": []}, f, indent=4)

def transfer_saves():

    with ftputil.FTPHost(address, "anonymous", "anonymous") as ftp_host:
        print("\nConnected to Wii U!\n")

        ftp_host.chdir(titleurlnu)
        names = ftp_host.listdir(ftp_host.curdir)
        print("There are the following users on the Wii U:")

        for name in names:
            if name == "version": continue
            print(f" -> {name}")

        userid = input("\nEnter the user ID of whom you would like to extract the save. Example: '80000003'.\n -> ")
        logurl = titleurl.replace("[userid]", userid)

        ftp_host.chdir(logurl)
        names = ftp_host.listdir(ftp_host.curdir)

        print(f"\nThere are {len(names)} log files. They may take a while to download, so please be patient.\n")

        for savefile in names:
            print(f" -> Downloading '{savefile}'...")
            ftp_host.download(f"{logurl}/{savefile}", f"./saves/{savefile}")

        print("\nAll log files have been downloaded.")
    
    print("\nDisconnected from Wii U!")

def PlayStats():

    with open("saves/PlayStats.dat", 'rb') as f:
        data = f.read()

    entry_count = unpack('>I', data[0:4])[0]

    with open('PlayStats.json', 'r') as f:
        playstatsJson = json.load(f)

    playstatsJson['entry_count'] = entry_count

    for val in range(4, 20*entry_count, 20):
        entry = unpack(">QIHHHH", data[val:val+20])

        tid_hi = entry[0] >> 32
        tid_lo = entry[0] & 0xFFFFFFFF
        formatted_tid = f'{tid_hi:08x}{tid_lo:08x}'.upper()

        entry_totaltime = entry[1]
        entry_times = entry[2]

        entry_firstplay = entry[3]
        entry_lastplay = entry[4]

        entry_dict = {
            "tid": formatted_tid,
            "time": entry_totaltime,
            "count": entry_times,
            "first": entry_firstplay,
            "last": entry_lastplay
        }

        if entry_dict not in playstatsJson['entries']:
            playstatsJson['entries'].append(entry_dict)

    with open('PlayStats.json', 'w') as f:
        json.dump(playstatsJson, f, indent=4)

if __name__ == '__main__':
    file_check()
    transfer_saves()
    PlayStats()