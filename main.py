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
    for i, message in enumerate(mbox):
        # log(f"[{datetime.now().isoformat()}] Processing mail: {i}\n")
        mailBytes = message.as_bytes();
        
        if message.is_multipart():
            messagebody = ''.join(part.get_payload().__str__() for part in message.get_payload())
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
            startTime = datetime.now()
            
            FILE_PATH = arg
            FILE_NAME = f"{os.path.basename(os.path.splitext(FILE_PATH)[0])}.json"
            print("Processing: ", FILE_PATH)
            
            mbox = mailbox.mbox(FILE_PATH)
            print(FILE_PATH, "Contains:", len(mbox), "emails")
            arr = mboxToJson(mbox)
            
            print("Total parsed emails:", len(arr))
            saveJson(arr, FILE_NAME)
            
            endTime = datetime.now()
            print("timetaken:", (endTime - startTime).total_seconds(), "Seconds")
        else:
            print(f"{arg} is not a file")
    
def test():
    PATHS = [
        "./data/fradulent_emails.txt",
        "./data/phishing-chorpus.txt"
        ]
    for PATH in PATHS:
        startTime = datetime.now()
        
        print("Processing: ", PATH)
        FILE_NAME = f"{os.path.basename(os.path.splitext(PATH)[0])}.json"
        
        mbox = mailbox.mbox(PATH)
        print(PATH, "Contains:", len(mbox), "emails")
        
        arr = mboxToJson(mbox)
        print("Total parsed emails:", len(arr))
        saveJson(arr, FILE_NAME)
        
        endTime = datetime.now()
        print("timetaken:", (endTime - startTime).total_seconds(), "Seconds")
    
if __name__ == "__main__":
    sys.exit(test())
    # sys.exit(main())