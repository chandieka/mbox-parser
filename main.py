#!/usr/bin/env python3

from datetime import datetime
import json
import os
import sys
import mailbox

FILE_PATH = './data/fradulent_emails.txt' # change this to ur desired file
FILE_NAME = f"[{datetime.now().timestamp()}]{os.path.basename(os.path.splitext(FILE_PATH)[0])}.json"

def log(text):
    fs = open("log.txt", mode="a")
    fs.write(text)
    fs.close()

def mboxToJson(mbox: mailbox.mbox,mode="raw"):
    temp = {}
    try:
        for i, message in enumerate(mbox):
            print(f"[{datetime.now().isoformat()}] Processing mail: {i}")
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

def saveJson(arr):
    fs = open(f'{FILE_NAME}',"w")
    fs.write(json.dumps(arr))
    fs.close()

def saveRaw(arr):
    fs = open("temp.txt","w")
    fs.write(arr.__str__())
    fs.close()

def main():
    mbox = mailbox.mbox(FILE_PATH)
    arr = mboxToJson(mbox)
    # saveRaw(arr)
    saveJson(arr)
            
if __name__ == "__main__":
    sys.exit(main())