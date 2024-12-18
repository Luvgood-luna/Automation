# Compare old hashes and new hashes.
# import the necessary modules

import hashlib
import pandas as pd
import os

hash_list = [ ]
file_list = [ ]


def hashForFile(file):

    try:
        with open(file,'rb') as f:
            file_hash = hashlib.sha256()

            for byte_block in iter(f.read(4096), b""):
                file_hash.update(byte_block)
            
        return file_hash.hexdigest()
        
    except Exception as e:
        print(f"Error while processing the file {file}: {e}")
        return None



file_path = "/path/to/dir/"

for filename in os.listdir(file_path):
    file = os.path.join(file_path, filename)

    if os.path.isfile(file):
        hash_file = hashForFile(file)
        
        if hash_file :
            hash_list.append(hash_file)
            file_list.append(filename)
            

df = pd.DataFrame({
    "FileName":file_list,
    "Hash":hash_list

})

df.to_csv("oldhash.csv", index=False)



