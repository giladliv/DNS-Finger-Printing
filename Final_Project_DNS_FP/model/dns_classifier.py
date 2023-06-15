import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from model.utils import *
import ipaddress


def preprocess_dns_data(dns_packets):
    # Create a mapping dictionary for categorical variables
    categorical_mapping = {
        'response_code': {'NOERROR': 0, 'NXDOMAIN': 1},
        'target': {'benign': 0, 'malicious': 1}
    }

    # Iterate over each DNS packet dictionary
    for packet in dns_packets:
        # Convert categorical variables to numerical values
        for key, mapping in categorical_mapping.items():
            packet[key] = mapping.get(packet[key], packet[key])

        # Convert IP addresses to numerical values
        packet['source_ip'] = int(ipaddress.IPv4Address(packet['source_ip']))
        packet['destination_ip'] = int(ipaddress.IPv4Address(packet['destination_ip']))
        packet['response'] = int(ipaddress.IPv4Address(packet['response']))
        del packet['query']

    return dns_packets


def load_data(list_dict):
    return pd.DataFrame(preprocess_dns_data(list_dict))




# Convert the list of dictionaries to a pandas DataFrame
data = load_data(dns_packets)
print(data)

# Step 1: Prepare the data

# Split the data into features (X) and the target variable (y)
X = data.drop('target', axis=1)
y = data['target']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 2: Train the Random Forest classifier
# Create a Random Forest classifier with 100 trees
rf_classifier = RandomForestClassifier(n_estimators=100)

# Train the classifier on the training data
rf_classifier.fit(X_train, y_train)

# Step 3: Make predictions on the test data
# Use the trained classifier to make predictions on the test data
predictions = rf_classifier.predict(X_test)

# Step 4: Evaluate the model
# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)
