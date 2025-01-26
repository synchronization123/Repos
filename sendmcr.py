import pandas as pd
import requests

# Set the API URL and token
api_url = 'https://demo.defectdojo.org/api/v2/findings/'
api_token = 'Token 45eb3ae97556b9e9e77c3cb32695a03ef64767ba'
headers = {'Content-Type': 'application/json', 'Authorization': api_token}

# Function to feed data to the API
def feed_data_to_api(excel_file):
    try:
        # Load the Excel file
        df = pd.read_excel(excel_file)

        # Ensure the column names are case-sensitive by using the original column names
        # If necessary, print the column names to confirm this:
        print("Columns in the Excel file:", df.columns.tolist())

        # Ensure 'date' and 'assigned_on' columns are in datetime format and converted to 'YYYY-MM-DD'
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')
        df['assigned_on'] = pd.to_datetime(df['assigned_on'], errors='coerce').dt.strftime('%Y-%m-%d')

        # Loop through the rows and prepare data
        for index, row in df.iterrows():
            # Extract and map the required columns (case-sensitive)
            issue_key = row.get('issue_key')  # This should retain the case as it is
            date = row.get('date')
            comments = row.get('comments')
            assigned_to = row.get('assigned_to')
            status = row.get('status')  # Assuming 'status' column exists
            assigned_on = row.get('assigned_on')
            version = row.get('version')

            # Prepare the JSON data to be sent
            payload = {
                "title": issue_key,  # Issue key is kept as is, preserving case
                "date": date,
                "description": comments,
                "mitigation": assigned_to,
                "is_mitigated": False,  # Pending
                "references": "",  # You can add this if necessary
                "verified": False,  # Not Verified
                "assigned_on": assigned_on,
                "planned_remediation_version": version,
                "engagement": 14,  # Set engagement ID
                "test": 33,  # Set test ID
                "found_by": [3],  # Expected as a list
                "severity": "Info",  # Severity level
                "active": "yes",  # Whether the finding is active
                "numerical_severity": 3  # Numerical severity value
            }

            # Send the POST request to the API
            response = requests.post(api_url, headers=headers, json=payload)

            # Check if the request was successful
            if response.status_code == 201:
                print(f"Successfully added: {issue_key}")
            else:
                print(f"Failed to add {issue_key}. Status code: {response.status_code}")
                print(response.text)

    except Exception as e:
        print(f"Error reading the Excel file or sending data: {e}")

# Provide the Excel file path
excel_file = 'data.xlsx'  # Adjust this as needed

# Feed data from the Excel file into the API
feed_data_to_api(excel_file)
