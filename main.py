#!/usr/bin/env python3

from datetime import datetime
from genericpath import isfile
import json
import os
import sys
import mailbox

def log(text):
    fs = open("log.txt", mode="a")
    fs.write(text)
    fs.close()

def mboxToJson(mbox: mailbox.mbox):
    temp = {}
    try:
        for i, message in enumerate(mbox):
            log(f"[{datetime.now().isoformat()}] Processing mail: {i}\n")
            mailBytes = message.as_bytes();
            temp[i] = {
                "raw_mail": mailBytes.decode('ascii', 'ignore'),
                "subject": f'{message["Subject"]}',
                "from": f'{message["From"]}',
                "to": f'{message["To"]}',
                "status": f'{message["Status"]}',
                "date": f'{message["Date"]}',
                "date_type": f'{type(message["Date"])}'
                }
    except Exception as e:
        log(e.__str__())
    return temp

def saveJson(arr, filename):
    fs = open(f'{filename}',"w")
    fs.write(json.dumps(arr))
    fs.close()

def main():
    for i, arg in enumerate(sys.argv):
        if(i == 0):
            continue
        if isfile(arg):
            FILE_PATH = arg
            FILE_NAME = f"[{datetime.now().timestamp()}]{os.path.basename(os.path.splitext(FILE_PATH)[0])}.json"
            
            mbox = mailbox.mbox(FILE_PATH)
            arr = mboxToJson(mbox)
            saveJson(arr, FILE_NAME)
        else:
            print(f"{arg} is not a file")
            
if __name__ == "__main__":
    sys.exit(main())