import joblib
import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

project_root = Path(__file__).resolve().parents[2]
data = pd.read_csv(project_root / "data" / "crop_price_dataset.csv").dropna().drop_duplicates()
data.columns = data.columns.str.strip()
data["month"] = pd.to_datetime(data["month"], errors="coerce").dt.month
data = data.dropna()
X = data.drop(columns=["avg_modal_price"])
y = data["avg_modal_price"]
categorical = X.select_dtypes(include=["object"]).columns.tolist()
numeric = X.select_dtypes(exclude=["object"]).columns.tolist()
preprocessor = ColumnTransformer([
    ("numeric", SimpleImputer(strategy="median"), numeric),
    ("categorical", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ]), categorical),
])
model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)),
])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print(f"MAE: {mean_absolute_error(y_test, predictions):.2f}")
print(f"RMSE: {mean_squared_error(y_test, predictions) ** 0.5:.2f}")
print(f"R-squared: {r2_score(y_test, predictions):.4f}")
model_path = project_root / "backend" / "app" / "models" / "price_prediction_model.pkl"
model_path.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, model_path)
print(f"Model saved at: {model_path}")
