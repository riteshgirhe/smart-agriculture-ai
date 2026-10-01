
# Step1 : import required libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
import joblib
from pathlib import Path



# Step 2: Load the dataset
project_root = Path(__file__).resolve().parents[2]
data = pd.read_csv(project_root / "data" / "yield_dataset.csv")

print("=" * 100)
# check the missing values
print(data.isnull().sum())

print("=" * 100)

# check the data types
print(data.dtypes)

print("=" * 100)

# check the info
print(data.info())

print("=" * 100)

# Step 3: Preprocess the data
# Drop rows with missing values
data = data.dropna()

print("=" * 100)

#check the unique values in categorical columns
print(data['Crop Type'].unique())

print("=" * 100)

# check the duplicate values in the dataset
print(data.duplicated().sum())

print("=" * 100)

# drop the duplicate values in the dataset
data = data.drop_duplicates()

print("=" * 100)

# check the unique values in categorical columns after dropping duplicates
categorical_columns = ['Crop Type', 'Soil Type', 'Fertilizer Used', 'Irrigation Type']
for col in categorical_columns:
    print(f"Unique values in {col}: {data[col].unique()}")

print("=" * 100)

# clean text/ categorical columns
for col in categorical_columns:
    data[col] = data[col].astype(str).str.strip().str.title()

print("=" * 100)

# check the unique value
for col in categorical_columns:
    print(f"Unique values in {col}: {data[col].unique()}")

print("=" * 40)

# Convert the planting date properly
data['Planting Date'] = pd.to_datetime(data['Planting Date'],
    format='%d-%m-%Y',
    errors='coerce'
    )

# extract the year, month, and day from the planting date
data['Planting_Year'] = data['Planting Date'].dt.year
data['Planting_Month'] = data['Planting Date'].dt.month
data['Planting_Day'] = data['Planting Date'].dt.day
data['Planting_DayOfYear'] = data['Planting Date'].dt.dayofyear
data['Planting_Quarter'] = data['Planting Date'].dt.quarter

# drop the original planting date column
data = data.drop(columns=['Planting Date'])

print("=" * 100)

# check the invalid values in the dataset
print("Fields size <= 0",(data[['Field Size (hectares)']] <= 0).sum())

# check the invalid values in the Yield_t_per_ha column
print("Yield_t_per_ha <= 0",(data[['Yield_t_per_ha']] <= 0).sum())

#  Check the outliers in the in Yield_t_per_ha column using IQR method
Q1 = data['Yield_t_per_ha'].quantile(0.25)
Q3 = data['Yield_t_per_ha'].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = data[(data['Yield_t_per_ha'] < lower_bound) | (data['Yield_t_per_ha'] > upper_bound)]
print("Number of outliers in Yield_t_per_ha:", outliers.shape[0])

print("=" * 100)

# divide the dataset into features and target variable
X = data.drop(columns=['Yield_t_per_ha'])
y = data['Yield_t_per_ha']

print("=" * 100)

#check the shape of the features and target variable
print("Shape of features:", X.shape)
print("Shape of target variable:", y.shape)

print("=" * 100)

# Step 4: Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# identify categorical and numerical columns
categorical_features =[
    'Crop Type',
    'Soil Type',
    'Fertilizer Used',
    'Irrigation Type'
]

numerical_features = [
    'Field Size (hectares)',
    'Planting_Year',
    'Planting_Month',
    'Planting_Day',
    'Planting_DayOfYear',
    'Planting_Quarter'
]

# Handle the missing value inside pipeline using SimpleImputer
numerical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median'))
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehotencoder', OneHotEncoder(handle_unknown='ignore',sparse_output=False))
])

# create the preprocessor using ColumnTransformer
preprocessor = ColumnTransformer([
    ('num', numerical_pipeline, numerical_features),
    ('cat', categorical_pipeline, categorical_features)
])

# first model:Random Forest Regressor
model = RandomForestRegressor(
    n_estimators=100, 
    random_state=42,
    n_jobs=-1)

# create the pipeline with preprocessor and model
rf_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', model)
])

# Step 5: Train the model
rf_pipeline.fit(X_train, y_train)

# make predictions on the test set
y_pred = rf_pipeline.predict(X_test)

# Step 6: Evaluate the model
print(f"MAE: {mean_absolute_error(y_test, y_pred):.4f}")
print(f"RMSE: {mean_squared_error(y_test, y_pred) ** 0.5:.4f}")
print(f"R-squared: {r2_score(y_test, y_pred):.4f}")

# save the trained model using joblib
# Create model directory if it does not exist
model_dir = project_root / "backend" / "app" / "models"
model_dir.mkdir(parents=True, exist_ok=True)

# Save trained pipeline
model_path = model_dir / "random_forest_model.pkl"

joblib.dump(rf_pipeline, model_path)

print("=" * 100)
print(f"Model saved successfully at: {model_path.resolve()}")
print("=" * 100)