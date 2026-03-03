import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

df = pd.read_csv("D:/final2 jee.csv")

X = df[["Marks"]]
y = df["Percentile"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

prediction = model.predict(X_test)

print("MAE:", round(mean_absolute_error(y_test, prediction), 4))
print("R2:", round(r2_score(y_test, prediction), 4))

joblib.dump(model, "model1_marks_to_percentile.pkl")

print("Model saved successfully")
