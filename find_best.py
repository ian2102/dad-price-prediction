import pandas as pd
import joblib
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.linear_model import LinearRegression, Ridge, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from sklearn.base import BaseEstimator, TransformerMixin

class AbsoluteValueTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.abs(X)

df = pd.read_csv("data/data6.csv")
X = df.drop(columns=['price'])
y = df['price']

X = X.fillna(0)
y = y.fillna(0)

y = np.log1p(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "LinearRegression": LinearRegression(),
    "Ridge": Ridge(),
    "ElasticNet": ElasticNet(),
    "RandomForest": RandomForestRegressor(),
    "GradientBoosting": GradientBoostingRegressor(),
    "SVR": SVR(),
    "KNeighbors": KNeighborsRegressor(),
    "MLPRegressor": MLPRegressor(),
    "ExtraTrees": ExtraTreesRegressor(),
    "XGBoost": XGBRegressor(),
    "LightGBM": LGBMRegressor(),
    "CatBoost": CatBoostRegressor(verbose=0),
}

log_transform = FunctionTransformer(np.log1p, validate=True)

best_model = None
best_score = float('-inf')
num_samples = int(len(df) / 1000)

for name, model in models.items():
    pipeline = make_pipeline(
        StandardScaler(),
        AbsoluteValueTransformer(),
        log_transform,
        model
    )
    
    score = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='r2').mean()
    
    print(f"{name}: {score:.4f}")

    pipeline.fit(X_train, y_train)
    model_filename = f"price_{num_samples}K_{datetime.now().date()}_{name}.joblib"
    joblib.dump(pipeline, "models/" + model_filename)

    if score > best_score:
        best_score = score
        best_model = (pipeline, model_filename)

if best_model:
    best_pipeline, best_model_filename = best_model
    best_model_filename_best = "models/" + f"BEST-{best_model_filename}"
    joblib.dump(best_pipeline, best_model_filename_best)
    print(f"Best model saved as {best_model_filename_best}")