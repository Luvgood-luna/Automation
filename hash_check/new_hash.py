# Compare the old hashes with new hash and raise a ticket if there is any error
# Import necessary modules
import hashlib
import os
import pandas as pd
import requests
import json
# Function to create hashes for each file in the directory 
def newHash(file):
    try:
        with open(file,'rb') as f:
            # define the hashfuction
            file_hash = hashlib.sha256()

            # Reading the data as block of 4096 bytes as to not overload the memory
            for byte_block in iter(lambda:f.read(4096), b""):
                # Updating the hash variable with each block of data
                file_hash.update(byte_block)

        return file_hash.hexdigest()

    except Exception as e:
        print(f"Error while processing the file {file} {e}")

# fuction to create a jira ticket

def raise_ticket(summary,description):
    # Creating API endpoints
    jira_url = "https://username.atlassian.net/rest/api/3/issue"
    auth = ("username/email", "apikey")
    ticket_data = { 
        "fields": {
            "project":{"key":"key"},
            "summary":summary,
            "issuetype":{"name":"issue"}
        }
    }

    # Make the post request
    headers = {"Content-Type": "application/json"}
    response = requests.post(jira_url, headers=headers, auth=auth, data=json.dumps(ticket_data))

        # Handle the response
    if response.status_code == 201:
        print("Ticket created successfully:", response.json())
    else:
        print(f"Failed to create ticket: {response.status_code} {response.text}")


dir_path = "path/"

# Creating lists to store list of new hashes and list of files that are currently present
new_hash_list = []
new_file_list = []

# Iterating through the dir_path to get each file inorder to create hash for them
for filename in os.listdir(dir_path):
    file = os.path.join(dir_path,filename)

    if os.path.isfile(file):
        new_file_list.append(filename)
        hash_value = newHash(file)

        if hash_value:
            # print(f"hash is {hash_value}")
            new_hash_list.append(hash_value)



#  Compare old and new 
oldfile = pd.read_csv('oldhash.csv')

old_files = oldfile["FileName"].tolist()
old_hash_list = oldfile["Hash"].tolist()

# Create dictioneries to compare easily

old_hash_map = dict(zip(old_files, old_hash_list))
new_hash_map = dict(zip(new_file_list, new_hash_list))

common_files = set(set(old_files) & set(new_file_list))
new_files = set(set(new_file_list) - set(old_files))
removed_files =set(set(old_files) - set(new_file_list)) 

changed_files = [
    file for file in common_files
    if old_hash_map[file] != new_hash_map[file]
]

if new_files:
    alert_message = f"ALERT: There are new file(s) {new_files}"
    print(alert_message)                

if removed_files:
    alert_message = "ALERT: Some file(s) have been removed: {removed_files}"
    print(alert_message)

if changed_files:
    alert_message = f"ALERT: There are changes in the hash(es) of some file(s); {changed_files}"
    print(alert_message)
    raise_ticket("Files integrity issues found", alert_message)


            
