
import json

json_data = {
  "id": 1,
  "name": "John",
  "address": {
      "city": "Delhi",
      "pin": 110001
  }
}

data = json.loads(json.dumps(json_data))
print(data)
for key, value in data.items():
    if isinstance(value, dict):
        for sub_key, sub_value in value.items():
            print(f"{key}_{sub_key}: {sub_value}")
    else:
        print(f"{key}: {value}")
#write generic code to flatten the json

