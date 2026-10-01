# File : fertilizer recommendation system

# import required libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from pathlib import Path
import joblib


# Step 2: Load the dataset
project_root = Path(__file__).resolve().parents[2]
data_path = project_root / "data" / "fertilizer_recommendation.csv"
df = pd.read_csv(data_path)

# Step 3: Preprocess the data
df = df.dropna(how ='all')

# Remove duplicate rows
df = df.drop_duplicates()

#clean columns name 
df.columns = df.columns.str.strip()
print(df.columns.tolist())
print("=" * 100)

# find the unique values in categorical columns
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
for col in categorical_columns:
    print(f"Unique values in {col}: {df[col].unique()}")

print("=" * 100)

# clean the categorical columns
for col in categorical_columns:
    df[col] = (df[col].astype(str).str.strip())

print("Cleaned categorical columns:", df[categorical_columns].head())

print("=" * 100)

# Step 4: Split the dataset into features and target variable
X = df.drop('Recommended_Fertilizer', axis=1)
y = df['Recommended_Fertilizer']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

categorical_features = X.select_dtypes(include=['object']).columns.tolist()
numerical_features = X.select_dtypes(exclude=['object']).columns.tolist()

preprocessor = ColumnTransformer([
    ('num', Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
    ]), numerical_features),
    ('cat', Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
    ]), categorical_features),
])

model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
    )),
])

model.fit(X_train, y_train)
predictions = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
print(f"Precision (macro): {precision_score(y_test, predictions, average='macro', zero_division=0):.4f}")
print(f"Recall (macro): {recall_score(y_test, predictions, average='macro', zero_division=0):.4f}")
print(f"F1-score (macro): {f1_score(y_test, predictions, average='macro', zero_division=0):.4f}")

model_path = project_root / "backend" / "app" / "models" / "fertilizer_model.pkl"
model_path.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, model_path)
print(f"Model saved successfully at: {model_path}")