import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler



def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    df.drop(['monthlycharges', 'typeofsale', 'country', 'floodingzone'], axis=1, inplace=True)

    df['subtypeofproperty'] = df['subtypeofproperty'].apply(lambda x: 'apartment' if x in ['apartment', 'ground_floor', 'apartment_block', 'flat_studio', 'service_flat', 'kot'] else ('house' if x in ['country_cottage','pavilion', 'mansion', 'manor_house', 'castle', 'chalet','triplex', 'farmhouse', 'town_house', 'house', 'villa', 'duplex', 'penthouse'] else 'other'))
    one_hot_sub = pd.get_dummies(df['subtypeofproperty']).astype('int64')
    one_hot_df = pd.get_dummies(df['region']).astype('int64')
    df = pd.concat([df, one_hot_sub, one_hot_df], axis=1)
    df= df.drop(['subtypeofproperty', 'region'], axis=1)

    region_dict = {'Hainaut': 1, 'Namur': 2, 'Liège': 3, 'Luxembourg': 4, 'Limburg': 5, 'East Flanders': 6, 'West Flanders': 7, 'Antwerp': 8, 'Brussels': 9, 'Walloon Brabant': 10, 'Flemish Brabant': 11}
    df['province'] = df['province'].map(region_dict)   
    rating_dict = {'A++': 1, 'A+': 2, 'A': 3, 'A_A+': 4, 'E_C': 5, 'G_C': 6, 'B': 7, 'B_A': 8, 'C': 9, 'D': 10, 'E': 11, 'F_C': 12, 'F': 13, 'F_D': 14, 'E_D': 15, 'F_E': 16, 'G': 17}
    df['peb'] = df['peb'].map(rating_dict)

    df.drop(['locality', 'district'], axis=1, inplace=True)

    X = df.drop('price', axis=1)
    y = df['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    without_scaler(X_train, X_test, y_train, y_test)
    with_scaler(X_train, X_test, y_train, y_test)


def without_scaler(X_train, X_test, y_train, y_test):
    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    test_score = model.score(X_test, y_test)
    mae = mean_absolute_error(y_test, y_pred)

    print('Test Score:', test_score)
    print('Mean Absolute Error:', mae)

    mean_price = y_test.mean()
    relative_error = mae / mean_price
    print('Relative Error:', relative_error)    

def with_scaler(X_train, X_test, y_train, y_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    test_score = model.score(X_test_scaled, y_test)
    mae = mean_absolute_error(y_test, y_pred)

    print('Test Score:', test_score)
    print('Mean Absolute Error:', mae)

    mean_price = y_test.mean()
    relative_error = mae / mean_price
    print('Relative Error:', relative_error)

preprocess_data('01.IMMOELIZA/03.Machine_Learning/cleaned_dataset.csv')



    # scaler = StandardScaler()
    # X_train_scaled = scaler.fit_transform(X_train)
    # X_test_scaled = scaler.transform(X_test)

    # model = GradientBoostingRegressor()
    # model.fit(X_train_scaled, y_train)

    # y_pred = model.predict(X_test_scaled)
    # test_score = model.score(X_test_scaled, y_test)
    # mae = mean_absolute_error(y_test, y_pred)

    # print('Test Score:', test_score)
    # print('Mean Absolute Error:', mae)


    #To see if MAE is good or not, you can check it with the mean or median of the price column

    # mean_price = y_test.mean()
    # relative_error = mae / mean_price
    # print('Relative Error:', relative_error)

