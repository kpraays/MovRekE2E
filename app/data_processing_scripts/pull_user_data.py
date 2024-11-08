# python3 pull_user_data.py ending_num starting_num

import requests
import sys
import csv

num_users = sys.argv[1]
start_user = sys.argv[2]
print(num_users)

csv_name = "users"+str(num_users) + ".csv"

with open(csv_name, mode="w", newline='') as file:
    writer = csv.writer(file)
    row = ['userid', 'age', 'occupation', 'gender']
    writer.writerow(row)

    for users in range(int(start_user), int(num_users)+1):
        response = requests.get("http://fall2023-comp585.cs.mcgill.ca:8080/user/"+str(users))

        if response.status_code != 200:
            print("Response not successful")

        row = [str(users), str(response.json()['age']), str(response.json()['occupation']), str(response.json()['gender'])]
        writer.writerow(row)

print(f"{csv_name} file created")
    
