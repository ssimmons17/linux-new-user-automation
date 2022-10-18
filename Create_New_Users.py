import os
import pandas as pd
from pandas import concat
import re
import subprocess
import numpy

#Check if source file exists; if so, open user list text file
user_source_file = '/home/stephen/Desktop/New_Users_List.txt'
if os.path.exists(user_source_file):
    users_list = open(user_source_file, 'r')
else:
    print("File does not exist. Please ensure that folder path and file name are correct!")

#lists to store regex groups
user_names = []
user_emails = []
user_groups = []

#use regex groups to parse username, email, and user group and append data to empty lists shown above
for line in users_list.readlines():
    new_user_regex = re.search(r"(\w+, \w+) - (\w+@\w+.com) - (\w+\n|\w+ \w+)", line)
    user_name = new_user_regex.group(1)
    user_email = new_user_regex.group(2)
    group = new_user_regex.group(3)
    user_group = group.replace(" ", "")
    user_group = user_group.strip('\n')
    #print(user_group)
    user_names.append(user_name)
    user_emails.append(user_email)
    user_groups.append(user_group)
#print(user_groups)

#create dataframe to store user data - is not necessary for script completion
data = {'Employee_Name': user_names, 'Employee_Email': user_emails, 'Employee_Group': user_groups}
df = pd.DataFrame(data)
df.to_csv()

#Check the user_groups list for unique values and only create group for those values
print("---------Groups-----------")
unique_user_groups = numpy.unique(user_groups)
for my_group in unique_user_groups:
    subprocess.run(['groupadd', my_group])
    print(f'The following group was created successfully: {my_group}')
print(" ")

#create username naming convention - first initial, lastname, lowercase
user_logins = []
logins_with_group = {}
for name in user_names:
    locate_first_letter = re.findall(r'(?<=\s)\w', name)
    for letter in locate_first_letter:
        new_name = letter + name
        user_login = re.sub(',\s\w+', '', new_name).lower()
        user_logins.append(user_login)
        #print(user_login)

#create new users on linux machine
print("-------Added Users---------")
for user in user_logins:
    #print(user)
    subprocess.run(['useradd', user])
    print(f'{user} has been added to the system!')
print(" ")

#create dictionary to match user login names with user group
for i in range(len(user_logins)):
    logins_with_group[user_logins[i]] = user_groups[i]
#print(logins_with_group)

#Add users to their designated groups
print("------Users Added to Groups---------")
cmd = 'sudo usermod -aG'
for k, v in logins_with_group.items():
    subprocess.Popen(['usermod', '-a','-G', f'{v}', f'{k}'])
    print(f'{k} has been added to the {v} group')





