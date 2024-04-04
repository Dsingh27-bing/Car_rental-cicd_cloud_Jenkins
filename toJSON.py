import pandas as pd

# Read Excel file into pandas DataFrame
df = pd.read_excel('CarData.xls')

# Convert DataFrame to JSON
json_data = df.to_json('output.json', orient='records')

# Print or save the JSON data
print(json_data)