import pandas as pd
import ast 
import json

df = pd.read_csv("Clean Dataset CSV.csv")

def try_eval(val):
    try:
        if isinstance(val, str) and (val.startswith("[") and val.endswith("]")):
            return ast.literal_eval(val)
        return val
    except:
        return val

df = df.applymap(try_eval)

json_data = {"data": df.to_dict(orient="records")}

with open("properties.json", "w") as f:
    json.dump(json_data, f, indent=4)

print("CSV converted to JSON with proper lists!")
