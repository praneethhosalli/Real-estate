import streamlit as st
from joblib import load
import numpy as np

# Load the pre-trained model and the scaler pipeline (if included in the pipeline)
model = load('Draagon.joblib')

# Custom CSS to style the app
st.markdown("""
    <style>
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
        }
        .description {
            font-size: 18px;
            color: #555555;
            text-align: center;
            margin-bottom: 20px;
        }
        .input-box {
            margin-bottom: 20px;
        }
        .input-label {
            font-size: 14px;
            color: #333333;
        }
        .prediction-result {
            font-size: 20px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            margin-top: 20px;
        }
        .error-message {
            font-size: 16px;
            color: #FF6347;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Title of the app
st.markdown('<div class="title"> Real Estate Price Predictor</div>', unsafe_allow_html=True)

# Description
st.markdown('<div class="description">Enter the feature values to predict the property price:</div>', unsafe_allow_html=True)

# Creating input fields for each feature (in table form)
crim = st.number_input("CRIM - per capita crime rate by town", value=0.0, key="crim")
zn = st.number_input("ZN - proportion of residential land zoned for lots over 25,000 sq.ft.", value=0.0, key="zn")
indus = st.number_input("INDUS - proportion of non-retail business acres per town", value=0.0, key="indus")
chas = st.number_input("CHAS - Charles River dummy variable", value=0.0, key="chas")
nox = st.number_input("NOX - nitric oxides concentration (parts per 10 million)", value=0.0, key="nox")
rm = st.number_input("RM - average number of rooms per dwelling", value=0.0, key="rm")
age = st.number_input("AGE - proportion of owner-occupied units built prior to 1940", value=0.0, key="age")
dis = st.number_input("DIS - weighted distances to five Boston employment centres", value=0.0, key="dis")
rad = st.number_input("RAD - index of accessibility to radial highways", value=0.0, key="rad")
tax = st.number_input("TAX - full-value property-tax rate per $10,000", value=0.0, key="tax")
ptratio = st.number_input("PTRATIO - pupil-teacher ratio by town", value=0.0, key="ptratio")
b = st.number_input("B - 1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town", value=0.0, key="b")
lstat = st.number_input("LSTAT - % lower status of the population", value=0.0, key="lstat")

# Adding a separator between input and prediction button
st.markdown("<hr>", unsafe_allow_html=True)

# Predict button
if st.button("Predict"):
    try:
        # Create a NumPy array with the feature values entered by the user
        features = np.array([[crim, zn, indus, chas, nox, rm, age, dis, rad, tax, ptratio, b, lstat]])

        # Perform prediction
        prediction = model.predict(features)

        # Multiply by 1000 to get the predicted price in actual dollars
        predicted_price_in_dollars = prediction[0] * 10000

        # Add conditional statements to adjust the prediction
        adjusted_price = predicted_price_in_dollars

        # Adjustments based on CRIM (Crime Rate)
        if crim < 1:
            adjusted_price *= 1.1  # Increase by 10%
        elif 1 <= crim < 5:
            adjusted_price *= 1.05  # Increase by 5%
        elif 5 <= crim < 10:
            adjusted_price *= 0.95  # Decrease by 5%
        else:
            adjusted_price *= 0.85  # Decrease by 15%

        # Adjustments based on ZN (Residential land zoned for large lots)
        if zn > 25:
            adjusted_price *= 1.15  # Increase by 15%
        elif 10 <= zn <= 25:
            adjusted_price *= 1.05  # Increase by 5%
        else:
            adjusted_price *= 0.9  # Decrease by 10%

        # Adjustments based on INDUS (Non-retail business acres)
        if indus < 5:
            adjusted_price *= 1.1  # Increase by 10%
        elif 5 <= indus < 15:
            adjusted_price *= 1.05  # Increase by 5%
        else:
            adjusted_price *= 0.95  # Decrease by 5%

        # Adjustments based on CHAS (Charles River proximity)
        if chas == 1:
            adjusted_price *= 1.2  # Increase by 20%
        else:
            adjusted_price *= 0.95  # Decrease by 5%

        # Adjustments based on NOX (Nitric Oxide Pollution)
        if nox < 0.4:
            adjusted_price *= 1.1  # Increase by 10%
        elif 0.4 <= nox < 0.6:
            adjusted_price *= 0.95  # Decrease by 5%
        elif 0.6 <= nox < 0.8:
            adjusted_price *= 0.9  # Decrease by 10%
        else:
            adjusted_price *= 0.85  # Decrease by 15%

        # Adjustments based on RM (Number of Rooms)
        if rm > 8:
            adjusted_price *= 1.2  # Increase by 20%
        elif 7 <= rm <= 8:
            adjusted_price *= 1.1  # Increase by 10%
        elif 5 <= rm < 7:
            adjusted_price *= 1.05  # Increase by 5%
        else:
            adjusted_price *= 0.9  # Decrease by 10%

        # Adjustments based on AGE (Building Age)
        if age < 50:
            adjusted_price *= 1.1  # Increase by 10%
        elif 50 <= age < 70:
            adjusted_price *= 1.05  # Increase by 5%
        elif 70 <= age < 90:
            adjusted_price *= 0.95  # Decrease by 5%
        else:
            adjusted_price *= 0.85  # Decrease by 15%

        # Adjustments based on DIS (Distance to Employment Centres)
        if dis < 3:
            adjusted_price *= 1.1  # Increase by 10%
        elif 3 <= dis < 6:
            adjusted_price *= 1.05  # Increase by 5%
        else:
            adjusted_price *= 0.9  # Decrease by 10%

        # Adjustments based on RAD (Access to Radial Highways)
        if rad <= 3:
            adjusted_price *= 1.1  # Increase by 10%
        elif 3 < rad <= 5:
            adjusted_price *= 1.05  # Increase by 5%
        else:
            adjusted_price *= 0.95  # Decrease by 5%

        # Adjustments based on TAX (Property Tax)
        if tax <= 200:
            adjusted_price *= 1.1  # Increase by 10%
        elif 200 < tax <= 400:
            adjusted_price *= 0.95  # Decrease by 5%
        else:
            adjusted_price *= 0.85  # Decrease by 15%

        # Adjustments based on PTRATIO (Pupil-Teacher Ratio)
        if ptratio < 12:
            adjusted_price *= 1.1  # Increase by 10%
        elif 12 <= ptratio < 15:
            adjusted_price *= 1.05  # Increase by 5%
        else:
            adjusted_price *= 0.95  # Decrease by 5%

        # Adjustments based on LSTAT (Lower Status of Population)
        if lstat < 5:
            adjusted_price *= 1.2  # Increase by 20%
        elif 5 <= lstat < 10:
            adjusted_price *= 1.1  # Increase by 10%
        else:
            adjusted_price *= 0.8  # Decrease by 20%

        # Display the final adjusted price
        st.markdown(f'<div class="prediction-result">Adjusted Predicted Price: ${adjusted_price:,.2f}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.markdown(f'<div class="error-message">Error: {str(e)}</div>', unsafe_allow_html=True)
