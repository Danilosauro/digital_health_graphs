import pandas as pd

data = pd.read_parquet('../data/mock_data.parquet') 
data = data.sort_values('data') 
data.to_parquet('../data/mock_data.parquet', engine='pyarrow') 

