# The program to analyze logs.
# Read the file
# Extract ip, errors and successful logs.
# Save the output as csv
# send email.

# Import re module to make sure of ipv4 format.
import re
from pprint import pprint

import pandas as pd
# Read the file
with open('serverlogs.log', 'r') as file:

    # Pattern for IP
    ip_pattern = r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"

    ip_addrs_lst = []
    success_lst = []
    failed_lst = []
    # Get the ip address
    for line in file:
        # ip_addr = ip_pattern.findall(line)
        ip_addr = re.search(ip_pattern,line)
        ip_addrs_lst.append(ip_addr.group())

        list = line.split(" ")
        failed_lst.append(int(list[-1]))
        success_lst.append(int(list[-4]))

    total_success = sum(success_lst)
    total_failed = sum(failed_lst)
    ip_addrs_lst.append("Total")
    failed_lst.append(total_failed)
    success_lst.append(total_success)


# print (success_lst)
df = pd.DataFrame(columns=["IP-Address", "Success", "Failed"])
df["IP-Address"] = ip_addrs_lst
df["Success"] = success_lst
df["Failed"] = failed_lst

df.to_csv('output.csv',index=False)
pprint(df)
# print(ip_addrs_lst)



