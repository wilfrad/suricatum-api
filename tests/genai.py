#from app.surveys.validation import AiPostGeneratorChecker

#ints = AiPostGeneratorChecker()

import json

def json_to_array(json_str):
    # Parse JSON string
    data = json.loads(json_str)
    
    # Initialize empty array
    result = []
    
    # Iterate through each object in the JSON
    for obj in data:
        # Iterate through each key in the object
        for key in obj:
            # Append the string value to the result array
            result.append(obj[key]["1"])
    
    return result

# JSON string
json_str = '''
[
    { "1": { "1": "text" } },
    { "2": { "1": "text" } },
    { "3": { "1": "text" } },
    { "4": { "1": "text" } }
]
'''

# Convert JSON to array
result_array = json_to_array(json_str)
print(result_array)