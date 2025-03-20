import pandas as pd
import joblib
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
import scheme

df = pd.read_csv('data/2025-03-13.csv', encoding='utf-8', encoding_errors='ignore')
df = df.dropna()

df = df.drop(columns=['text'])
df = pd.get_dummies(df)
item = scheme.get_empty_item()
missing_cols = list(set(item) - set(df.columns))
missing_df = pd.DataFrame(0, index=df.index, columns=missing_cols)
df = pd.concat([df, missing_df], axis=1)
    
X = df.drop(columns=['price'])
y = df['price']

model = RandomForestRegressor()
model.fit(X, y)

num_samples = int(len(df) / 1000)
model_filename = f"price_{num_samples}K_{datetime.now().date()}_RandomForestRegressor.joblib"
joblib.dump(model, "models/" + model_filename)

print(f"Model saved as {model_filename}")
