import csv
from flask import Flask, redirect, request, jsonify, render_template, send_file, url_for
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from pymongo import MongoClient
import pymongo
app = Flask(__name__, static_url_path='/static')

# Load the dataset
df = pd.read_csv("C:/Users/KIRAN KUMAR/Downloads/SNO_23-20240324T030541Z-001/SNO_23/23finance/transactiondata.csv")

# Preprocessing
# Drop unnecessary columns
df = df.drop('TransactionID', axis=1)

# Split the 'Timestamp' column into minutes and seconds
df[['Minutes', 'Seconds']] = "57:31.1".split(':')

# Convert minutes and seconds to float
df['Minutes'] = df['Minutes'].astype(float)
df['Seconds'] = df['Seconds'].astype(float)

# Convert the time to seconds
df['Timestamp_seconds'] = df['Minutes'] * 60 + df['Seconds']

# Drop the original 'Timestamp' column and the intermediate columns
df = df.drop(['Timestamp', 'Minutes', 'Seconds'], axis=1)

# Encode categorical variables using one-hot encoding
encoder = OneHotEncoder()
df_encoded = pd.DataFrame(encoder.fit_transform(df[['TransactionLocation']]).toarray(), columns=encoder.categories_[0])

# Concatenate the encoded features with the original dataframe
df = pd.concat([df.drop(['TransactionLocation'], axis=1), df_encoded], axis=1)

# Splitting the data into features (X) and target variable (y)
X = df.drop('IsFraud', axis=1)
y = df['IsFraud']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest classifier
random_forest = RandomForestClassifier(random_state=42)

# Train the Random Forest classifier
random_forest.fit(X_train, y_train)

@app.route("/")
def index():
    return render_template('login.html')
@app.route("/menu" , methods=['GET'])
def menu():
    return render_template('menus.html')
@app.route("/frontend" , methods=['GET'])
def frontend():
    return render_template('frontend.html')
@app.route('/dataset', methods=['GET'])
def dataset():
    return render_template('dataset.html')
@app.route('/report', methods=['GET'])
def report():
    return send_file('MAIN REPORT_merged.pdf')
@app.route('/team', methods=['GET'])
def team():
    return render_template('team.html')
@app.route('/uml', methods=['GET'])
def uml():
    return render_template('uml.html')
@app.route('/intro', methods=['GET'])
def intro():
    return render_template('intro.html')
@app.route('/backend', methods=['GET'])
def backend():
    return render_template('Finance.html')
@app.route('/login', methods=['POST'])
def login():
    username=request.form.get("username")
    password=request.form.get("password")
    uri = "mongodb://localhost:27017"
    db_name = "USER_DETAILS"
    collection = "SIGNUP"
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection]
    query={"username": username, "password" : password}
    result=collection.find_one(query)
    print(query, result)
    if result:
         return jsonify({"stat": True})
    else:
        return jsonify({"stat" : False})
@app.route('/signup', methods=['POST'])
def signup():
    username=request.form.get("susername")
    password=request.form.get("spassword")
    email=request.form.get("semail")
    uri = "mongodb://localhost:27017"
    db_name = "USER_DETAILS"
    collection_name = "SIGNUP"
    data=[{"username": username, "password" : password, "Email" : email}]
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    result = collection.insert_many(data)
    client.close()
    return jsonify({"stat": True})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        amount = float(request.form.get("amount"))
        location = request.form.get("location")
        timestamp = request.form.get("timestamp")
        data = pd.DataFrame({"Amount": [amount], "TransactionLocation": [location], "Timestamp": [timestamp]})
        data[['Minutes', 'Seconds']] = "57:31.1".split(':')
        data['Minutes'] = data['Minutes'].astype(float)
        data['Seconds'] = data['Seconds'].astype(float)
        data['Timestamp_seconds'] = data['Minutes'] * 60 + data['Seconds']
        data = data.drop(['Minutes', 'Seconds', 'Timestamp'], axis=1)
        encoded_data = pd.DataFrame(encoder.transform(data[['TransactionLocation']]).toarray(), columns=encoder.categories_[0])
        data = pd.concat([data.drop(['TransactionLocation'], axis=1), encoded_data], axis=1)
        prediction = random_forest.predict(data)
        return jsonify({"prediction": int(prediction[0])})

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)