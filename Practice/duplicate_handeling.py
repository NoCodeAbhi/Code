#duplicate handeling

records = [
 {"id":1,"ts":"2025-01-01 10:00:00"},
 {"id":1,"ts":"2025-01-01 11:00:00"},
 {"id":2,"ts":"2025-01-01 09:00:00"}
]

unique_records = {}

for record in records:
    k = record["id"]
    v = record["ts"]
    if k not in unique_records:
        unique_records[k] = v
print(unique_records)