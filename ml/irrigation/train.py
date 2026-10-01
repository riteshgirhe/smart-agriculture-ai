import joblib
import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

project_root = Path(__file__).resolve().parents[2]
data = pd.read_csv(project_root / "data" / "irrigation_prediction.csv").dropna().drop_duplicates()
data.columns = data.columns.str.strip()
X = data.drop(columns=["Irrigation_Need"])
y = data["Irrigation_Need"].astype(str).str.strip()
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
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=1)),
])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
print(f"Precision (macro): {precision_score(y_test, predictions, average='macro', zero_division=0):.4f}")
print(f"Recall (macro): {recall_score(y_test, predictions, average='macro', zero_division=0):.4f}")
print(f"F1-score (macro): {f1_score(y_test, predictions, average='macro', zero_division=0):.4f}")
model_path = project_root / "backend" / "app" / "models" / "irrigation_model.pkl"
model_path.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, model_path)
print(f"Model saved at: {model_path}")
