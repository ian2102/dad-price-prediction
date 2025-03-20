import lightgbm as lgb
import xgboost as xgb
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.multioutput import MultiOutputRegressor
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
import pandas as pd
from datetime import datetime
import scheme

df = pd.read_csv('data/2025-03-18.csv', encoding='utf-8', encoding_errors='ignore')
df = df.dropna()

X = df["text"]
df = df.drop(columns=['text'])
df = pd.get_dummies(df)
item = scheme.get_empty_item()
missing_cols = list(set(item) - set(df.columns))
missing_df = pd.DataFrame(0, index=df.index, columns=missing_cols)
df = pd.concat([df, missing_df], axis=1)

y = df.drop(columns=["price"])

vectorizer = TfidfVectorizer(max_features=5000)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "LightGBM": MultiOutputRegressor(lgb.LGBMRegressor()),
    "RandomForest": MultiOutputRegressor(RandomForestRegressor()),
    "XGBoost": MultiOutputRegressor(xgb.XGBRegressor()),
    "LinearRegression": MultiOutputRegressor(LinearRegression()),
    "MLPRegressor": MultiOutputRegressor(MLPRegressor())
}

results = []

for model_name, model in models.items():
    print(f"Training {model_name}...")

    pipeline = Pipeline([
        ('vectorizer', vectorizer),
        ('model', model)
    ])
    
    pipeline.fit(X_train, y_train)
    
    y_pred = pipeline.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    results.append({
        'Model': model_name,
        'MSE': mse,
        'R2': r2
    })
    
    num_samples = len(df) // 1000
    model_filename = f"{model_name}_{num_samples}K_{datetime.now().date()}_Model.joblib"
    joblib.dump(pipeline, "image_recognition/" + model_filename)
    print(f"Model saved as {model_filename}")


results_df = pd.DataFrame(results)

print("\nModel Comparison:")
print(results_df)
