import json
import ast

def read_from_cf():
    with open(f'CF/cf.json',"r") as f:
        json_ = json.load(f) 
    json_ = json.dumps(json_,ensure_ascii = False)
    json_ = ast.literal_eval(json_) 
    return json_