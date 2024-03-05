import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer

# Load the data
data = pd.read_csv('/Users/viktorciroski/Documents/Github/AI-Assistant/src/tmp/indiana_trees_remeasured.csv')

# Check if the data needs preprocessing
print(data.head())

# Assuming 'DBH' is the target variable and the rest are features
# Convert categorical variables into dummy/indicator variables
X = pd.get_dummies(data.drop('DBH', axis=1))
y = data['DBH']

# Handle missing values
imputer = SimpleImputer()
X = imputer.fit_transform(X)
y = imputer.fit_transform(y.values.reshape(-1,1)).ravel()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a linear regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')