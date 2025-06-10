import os
import shutil

# path to source directory
src_dir = '/Users/seamanj/Documents/TEMPLATES/Woolworths Job Number  - CAMPAIGN - TEMPLATE'

# path to destination directory
dest_dir = '/Users/seamanj/Documents/Test Destination/Woolworths Job Number  - CAMPAIGN - TEMPLATE'

# getting all the files in the source directory
files = os.listdir(src_dir)

shutil.copytree(src_dir, dest_dir)

jobNumber = input("Enter your job number:")
description = input("Enter your description:")

os.rename(dest_dir, f"/Users/seamanj/Documents/Test Destination/{jobNumber}  - CAMPAIGN - {description}")
