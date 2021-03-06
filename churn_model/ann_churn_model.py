import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from keras.models import Sequential
from keras.layers import Dense

# ###########
# IMPORT DATA
# ###########
query = """
SELECT
    *
FROM
    [newsuk-datatech-datatonic:tutorial_data.churn_data]
"""
dataset = pd.io.gbq.read_gbq(query=query,
                             project_id="newsuk-datatech-datatonic")
X = dataset.iloc[:, 3:13].values
y = dataset.iloc[:, 13].values

# ##################
# DATA PREPROCESSING
# ##################
# Encoding categorical data
labelencoder_X_1 = LabelEncoder()
X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1])
labelencoder_X_2 = LabelEncoder()
X[:, 2] = labelencoder_X_2.fit_transform(X[:, 2])
onehotencoder = OneHotEncoder(categorical_features=[1])
X = onehotencoder.fit_transform(X).toarray()
X = X[:, 1:]

# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=0)
# Feature Scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# #########
# BUILD ANN
# #########
# Initialising the ANN
classifier = Sequential()

# Add layers
classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu',
                     input_dim=11))
classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu'))
classifier.add(Dense(units=1, kernel_initializer='uniform',
                     activation='sigmoid'))
classifier.compile(optimizer='adam', loss='binary_crossentropy',
                   metrics=['accuracy'])
classifier.fit(X_train, y_train, batch_size=10, epochs=100)

# ################
# MAKE PREDICTIONS
# ################
# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)
# Making the Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
