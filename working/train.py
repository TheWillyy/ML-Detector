import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
import joblib

# Load and preprocess the data
data = pd.read_csv('final_output_dataset.csv')
data = data.dropna()
data = data.drop_duplicates()
data = data.sample(frac=0.001, random_state=100)
data.to_csv("zzextract.csv", index=False)

# Encode the labels
label_encoder = LabelEncoder()
data['result'] = label_encoder.fit_transform(data['result'])

# Define features and target
X = data.drop(columns=['url', 'label', 'result'])
y = data['result']

# Split the data into training, validation, and testing sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=100, stratify=y)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=100, stratify=y_temp)

# Train the Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=100)
rf_model.fit(X_train, y_train)

# Evaluate the Random Forest model on the validation set
y_pred = rf_model.predict(X_test)
print(classification_report(y_test, y_pred))
y_val_pred = rf_model.predict(X_val)

val_accuracy = accuracy_score(y_val, y_val_pred)
val_precision = precision_score(y_val, y_val_pred)
val_recall = recall_score(y_val, y_val_pred)
val_f1 = f1_score(y_val, y_val_pred)

print("RF Validation Accuracy:", val_accuracy)
print("RF Validation Precision:", val_precision)
print("RF Validation Recall:", val_recall)
print("RF Validation F1 Score:", val_f1)
print("Validation Confusion Matrix:\n", confusion_matrix(y_val, y_val_pred))
print("Validation Classification Report:\n", classification_report(y_val, y_val_pred))

# Fine-tune the model using GridSearchCV with the validation set
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_features': [None, 'sqrt', 'log2'],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(estimator=RandomForestClassifier(random_state=100),
                           param_grid=param_grid,
                           cv=5,
                           n_jobs=-1,
                           verbose=2,
                           error_score='raise')

grid_search.fit(X_train, y_train)
best_rf_model = grid_search.best_estimator_

# Evaluate the best Random Forest model on the test set
y_test_pred = best_rf_model.predict(X_test)

test_accuracy = accuracy_score(y_test, y_test_pred)
test_precision = precision_score(y_test, y_test_pred)
test_recall = recall_score(y_test, y_test_pred)
test_f1 = f1_score(y_test, y_test_pred)

print("Best Model Test Accuracy:", test_accuracy)
print("Best Model Test Precision:", test_precision)
print("Best Model Test Recall:", test_recall)
print("Best Model Test F1 Score:", test_f1)
print("Test Confusion Matrix:\n", confusion_matrix(y_test, y_test_pred))
print("Test Classification Report:\n", classification_report(y_test, y_test_pred))

# Save the best RandomForest model from GridSearchCV
joblib.dump(best_rf_model, 'best_random_forest_model.joblib')

# Train the XGBoost model
xgb_model = XGBClassifier(n_estimators=100, random_state=100)
xgb_model.fit(X_train, y_train)

# Evaluate the XGBoost model on the validation set
xgb_val_pred = xgb_model.predict(X_val)

xgb_val_accuracy = accuracy_score(y_val, xgb_val_pred)
xgb_val_precision = precision_score(y_val, xgb_val_pred)
xgb_val_recall = recall_score(y_val, xgb_val_pred)
xgb_val_f1 = f1_score(y_val, xgb_val_pred)

print("\nXGBoost Validation Performance:")
print(f'Accuracy: {xgb_val_accuracy:.4f}')
print(f'Precision: {xgb_val_precision:.4f}')
print(f'Recall: {xgb_val_recall:.4f}')
print(f'F1 Score: {xgb_val_f1:.4f}')

# Evaluate the XGBoost model on the test set
xgb_test_pred = xgb_model.predict(X_test)

xgb_test_accuracy = accuracy_score(y_test, xgb_test_pred)
xgb_test_precision = precision_score(y_test, xgb_test_pred)
xgb_test_recall = recall_score(y_test, xgb_test_pred)
xgb_test_f1 = f1_score(y_test, xgb_test_pred)

print("\nXGBoost Test Performance:")
print(f'Accuracy: {xgb_test_accuracy:.4f}')
print(f'Precision: {xgb_test_precision:.4f}')
print(f'Recall: {xgb_test_recall:.4f}')
print(f'F1 Score: {xgb_test_f1:.4f}')

# Save the trained XGBoost model
joblib.dump(xgb_model, 'xgb_model.joblib')
