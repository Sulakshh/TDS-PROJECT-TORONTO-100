import requests
import csv

# Set up API token and headers
api_token = "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"  # PAT
headers = {
    "Authorization": f"token {api_token}",
    "Accept": "application/vnd.github+json",
}

# Endpoint and initial parameters
url = "https://api.github.com/search/users"
params = {
    "q": "location:Toronto followers:>100",
    "per_page": 100,  # Maximum allowed per page
    "page": 1         # Start with the first page
}

# Initialize a list to hold all user data formatted for CSV
all_users_data = []

# Loop through pages to retrieve all users
while True:
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        users_data = response.json().get("items", [])
        
        # If no more users are returned, break the loop
        if not users_data:
            break

        # Fetch details for each user and format data
        for user in users_data:
            user_url = f"https://api.github.com/users/{user['login']}"
            user_response = requests.get(user_url, headers=headers)
            if user_response.status_code == 200:
                user_info = user_response.json()
                user_data = {
                    "login": user_info.get("login"),
                    "name": user_info.get("name", ""),
                    "company": user_info.get("company", "").strip('@').upper() if user_info.get("company") else "",
                    "location": user_info.get("location", ""),
                    "email": user_info.get("email", ""),
                    "hireable": user_info.get("hireable", ""),
                    "bio": user_info.get("bio", ""),
                    "public_repos": user_info.get("public_repos", 0),
                    "followers": user_info.get("followers", 0),
                    "following": user_info.get("following", 0),
                    "created_at": user_info.get("created_at", ""),
                }
                all_users_data.append(user_data)

        # Increment the page number for the next request
        params["page"] += 1
    else:
        print("Error:", response.status_code, response.json())
        break

# Write the collected data to users.csv
with open("users.csv", "w", newline='', encoding='utf-8') as f:
    fieldnames = ["login", "name", "company", "location", "email", "hireable", "bio", "public_repos", "followers", "following", "created_at"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_users_data)

print("Data has been written to users.csv")
