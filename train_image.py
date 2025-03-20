import pandas as pd
import joblib
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import scheme

df = pd.read_csv('data/2025-03-13.csv', encoding='utf-8', encoding_errors='ignore')
df = df.dropna()

df = df.drop(columns=['text'])
df = pd.get_dummies(df)
item = scheme.get_empty_item()
missing_cols = list(set(item) - set(df.columns))
missing_df = pd.DataFrame(0, index=df.index, columns=missing_cols)
df = pd.concat([df, missing_df], axis=1)

X = df["text"]
df = df.drop(columns=['text'])

df = pd.get_dummies(df)
item = scheme.get_empty_item()
missing_cols = list(set(item) - set(df.columns))
missing_df = pd.DataFrame(0, index=df.index, columns=missing_cols)
df = pd.concat([df, missing_df], axis=1)

y = df.drop(columns=["price"])

vectorizer = TfidfVectorizer(max_features=5000)

mlp_model = MLPRegressor(hidden_layer_sizes=(512, 256, 128), 
                         activation='relu', 
                         solver='adam', 
                         max_iter=1000, 
                         learning_rate='adaptive',
                         random_state=42)

pipeline = Pipeline([
    ('vectorizer', vectorizer),
    ('scaler', StandardScaler(with_mean=False)),
    ('model', mlp_model)
])

pipeline.fit(X, y)

num_samples = len(df) // 1000
model_filename = f"multi_output_{num_samples}K_{datetime.now().date()}_MLPRegressor.joblib"
joblib.dump(pipeline, "image_recognition/" + model_filename)

print(f"Model saved as {model_filename}")
