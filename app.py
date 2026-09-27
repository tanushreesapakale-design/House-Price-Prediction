import streamlit as st
import pandas as pd
import joblib


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide"
)


# --------------------------------------------------
# Load Trained Models
# --------------------------------------------------

@st.cache_resource
def load_models():
    regression_model = joblib.load(
        "models/house_price_regression_model.pkl"
    )

    classification_model = joblib.load(
        "models/house_price_classification_model.pkl"
    )

    return regression_model, classification_model


rf_model, rf_classifier = load_models()


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🏠 House Price Prediction & Classification")

st.write(
    "Enter the details of a house to predict its estimated "
    "price and price category."
)

st.divider()


# --------------------------------------------------
# Input Section
# --------------------------------------------------

st.subheader("Enter House Details")


col1, col2, col3 = st.columns(3)


# Column 1
with col1:

    bedrooms = st.number_input(
        "Bedrooms",
        min_value=0,
        max_value=20,
        value=3,
        step=1
    )

    bathrooms = st.number_input(
        "Bathrooms",
        min_value=0.0,
        max_value=10.0,
        value=2.0,
        step=0.25
    )

    sqft_living = st.number_input(
        "Living Area (sqft)",
        min_value=100,
        max_value=20000,
        value=2000,
        step=100
    )

    sqft_lot = st.number_input(
        "Lot Area (sqft)",
        min_value=100,
        max_value=1000000,
        value=5000,
        step=500
    )

    floors = st.number_input(
        "Floors",
        min_value=1.0,
        max_value=10.0,
        value=1.0,
        step=0.5
    )

    waterfront = st.selectbox(
        "Waterfront",
        ["No", "Yes"]
    )


# Column 2
with col2:

    view = st.number_input(
        "View Rating",
        min_value=0,
        max_value=4,
        value=0,
        step=1
    )

    condition_label = st.selectbox(
        "Condition",
        [
            "Poor",
            "Fair",
            "Average",
            "Good",
            "Very Good"
        ],
        index=2
    )

    grade = st.number_input(
        "House Grade",
        min_value=1,
        max_value=13,
        value=7,
        step=1
    )

    sqft_above = st.number_input(
        "Above Ground Area (sqft)",
        min_value=0,
        max_value=20000,
        value=1800,
        step=100
    )

    sqft_basement = st.number_input(
        "Basement Area (sqft)",
        min_value=0,
        max_value=10000,
        value=200,
        step=100
    )

    yr_built = st.number_input(
        "Year Built",
        min_value=1800,
        max_value=2026,
        value=1990,
        step=1
    )


# Column 3
with col3:

    yr_renovated = st.number_input(
        "Year Renovated (0 if never renovated)",
        min_value=0,
        max_value=2026,
        value=0,
        step=1
    )

    lat = st.number_input(
        "Latitude",
        min_value=-90.0,
        max_value=90.0,
        value=47.5,
        step=0.0001,
        format="%.4f"
    )

    long = st.number_input(
        "Longitude",
        min_value=-180.0,
        max_value=180.0,
        value=-122.2,
        step=0.0001,
        format="%.4f"
    )

    sqft_living15 = st.number_input(
        "Average Living Area of Nearby Houses (sqft)",
        min_value=100,
        max_value=20000,
        value=1900,
        step=100
    )

    sqft_lot15 = st.number_input(
        "Average Lot Area of Nearby Houses (sqft)",
        min_value=100,
        max_value=1000000,
        value=5000,
        step=500
    )

    sale_year = st.number_input(
        "Sale Year",
        min_value=1900,
        max_value=2026,
        value=2014,
        step=1
    )

    sale_month = st.number_input(
        "Sale Month",
        min_value=1,
        max_value=12,
        value=6,
        step=1
    )


# --------------------------------------------------
# Convert Input Values
# --------------------------------------------------

waterfront_value = 1 if waterfront == "Yes" else 0

condition_map = {
    "Poor": 1,
    "Fair": 2,
    "Average": 3,
    "Good": 4,
    "Very Good": 5
}

condition_value = condition_map[condition_label]


# --------------------------------------------------
# Prediction Button
# --------------------------------------------------

st.divider()

if st.button("🔮 Predict House Price", use_container_width=True):

    # Basic validation

    if sqft_above > sqft_living:
        st.warning(
            "Above-ground area is greater than total living area. "
            "Please check the values."
        )

    elif yr_renovated != 0 and yr_renovated < yr_built:
        st.warning(
            "Renovation year cannot be earlier than the year the house was built."
        )

    elif yr_built > sale_year:
        st.warning(
            "Year built cannot be later than the sale year."
        )

    else:

        # --------------------------------------------------
        # Create Input DataFrame
        # --------------------------------------------------

        input_data = pd.DataFrame([[
            bedrooms,
            bathrooms,
            sqft_living,
            sqft_lot,
            floors,
            waterfront_value,
            view,
            condition_value,
            grade,
            sqft_above,
            sqft_basement,
            yr_built,
            yr_renovated,
            lat,
            long,
            sqft_living15,
            sqft_lot15,
            sale_year,
            sale_month
        ]], columns=[
            "bedrooms",
            "bathrooms",
            "sqft_living",
            "sqft_lot",
            "floors",
            "waterfront",
            "view",
            "condition",
            "grade",
            "sqft_above",
            "sqft_basement",
            "yr_built",
            "yr_renovated",
            "lat",
            "long",
            "sqft_living15",
            "sqft_lot15",
            "sale_year",
            "sale_month"
        ])


        # --------------------------------------------------
        # Make Predictions
        # --------------------------------------------------

        predicted_price = rf_model.predict(input_data)[0]

        predicted_category = rf_classifier.predict(
            input_data
        )[0]


        # --------------------------------------------------
        # Display Results
        # --------------------------------------------------

        st.success("Prediction completed successfully!")

        result_col1, result_col2 = st.columns(2)

        with result_col1:

            st.metric(
                "Predicted House Price",
                f"${predicted_price:,.2f}"
            )

        with result_col2:

            st.metric(
                "Price Category",
                str(predicted_category)
            )


        st.divider()

        st.subheader("Prediction Details")

        st.write(
            f"**Estimated Price:** ${predicted_price:,.2f}"
        )

        st.write(
            f"**Predicted Category:** {predicted_category}"
        )