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
    template = {}
    try:
        for i, message in enumerate(mbox):
            log(f"[{datetime.now().isoformat()}] Processing mail: {i}\n")
            mailBytes = message.as_bytes();
            
            if message.is_multipart():
                messagebody = ''.join(part.get_payload() for part in message.get_payload())
            else:
                messagebody = message.get_payload()
                
            template[i] = {
                "raw_mail": mailBytes.decode('ascii', 'ignore'),
                "subject": f'{message["Subject"]}',
                "from": f'{message["From"]}',
                "to": f'{message["To"]}',
                "status": f'{message["Status"]}',
                "date": f'{message["Date"]}',
                # "date_dtype": f'{type(message["Date"])}',
                "body": f'{messagebody}',
                # "body_dtype": f'{type(messagebody)}'
                }
            
    except Exception as e:
        log(e.__str__())
    return template

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
            # FILE_NAME = f"[{datetime.now().timestamp()}]{os.path.basename(os.path.splitext(FILE_PATH)[0])}.json"
            FILE_NAME = f"{os.path.basename(os.path.splitext(FILE_PATH)[0])}.json"
            
            mbox = mailbox.mbox(FILE_PATH)
            arr = mboxToJson(mbox)
            saveJson(arr, FILE_NAME)
        else:
            print(f"{arg} is not a file")
    
def test():
    PATH = "./data/fradulent_emails.txt"
    FILE_NAME = f"{os.path.basename(os.path.splitext(PATH)[0])}.json"
    mbox = mailbox.mbox(PATH)
    arr = mboxToJson(mbox)
    saveJson(arr, FILE_NAME)
    
if __name__ == "__main__":
    sys.exit(test())
    # sys.exit(main())