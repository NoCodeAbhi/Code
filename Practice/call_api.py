import request
import json

#concurrent.futures

def processed_data(item):
    retry = 0
    max_retries = 3
    while retry < max_retries:
        url = f"https://jsonplaceholder.typicode.com/users/{item}"
        response = request.get(url)
        if response.status_code == 200:
            data = response.dumps()
            for k,v in data.items():
                print(f"{k}: {v}")
            return response.json()
        else:
            retry += 1
    if retry == max_retries:
        print(f"Failed to fetch data for item {item} after {max_retries} retries.")
        return None

def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        user_id = [1, 2, 3, 4, 5]
        for item in user_id:
           future = executor.processed_data(item)
           result = future.result()
           print(result)

    

if __name__ == "__main__":
    main()