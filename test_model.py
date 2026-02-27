import joblib
import pandas as pd

# Load model
model = joblib.load('model/best_model.pkl')

print("="*60)
print("MODEL ENCODING TEST")
print("="*60)

# Test different performance levels
tests = [
    {"name": "Excellent", "data": {'Attendance': 100, 'Internal Test 1': 40, 'Internal Test 2': 40, 'Assignment': 10, 'Study Hours': 8}},
    {"name": "Good", "data": {'Attendance': 85, 'Internal Test 1': 35, 'Internal Test 2': 35, 'Assignment': 8, 'Study Hours': 5}},
    {"name": "Average", "data": {'Attendance': 75, 'Internal Test 1': 28, 'Internal Test 2': 28, 'Assignment': 7, 'Study Hours': 3}},
    {"name": "Poor", "data": {'Attendance': 50, 'Internal Test 1': 15, 'Internal Test 2': 15, 'Assignment': 4, 'Study Hours': 1}}
]

for test in tests:
    df = pd.DataFrame([test['data']])
    prediction = model.predict(df)[0]
    print(f"\n{test['name']} Student → Model Output: {prediction}")

print("\n" + "="*60)
print("ACTUAL DATA FROM YOUR CSV:")
print("="*60)

# Load your actual training data
data = pd.read_csv("data/clean_final_data.csv")

print("\nPerformance Categories in your data:")
print(data['Performance'].value_counts())

print("\nSample 'Excellent' students from your data:")
excellent = data[data['Performance'] == 'Excellent'].head(3)
print(excellent)

print("\n" + "="*60)