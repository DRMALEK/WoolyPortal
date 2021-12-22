import json
from collections import defaultdict

def read_meta_data(file_url):
    raw_data = json.load(open(file_url, "r"))
    data_dict = defaultdict(list)
    
    for data_item in raw_data:
        
        data_dict[data_item["brand_name"]].extend(data_item["name"])

    return data_dict