import json
import pandas as pd

with open('data.json') as f:
	data = json.load(f)

df = pd.DataFrame(data)
print(df)
