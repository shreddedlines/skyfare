#  SKYFARE — Flight Price Intelligence

A machine learning web application that predicts domestic flight prices in India using a Random Forest Regressor, wrapped in a sleek, dark-themed Streamlit interface.

🔗 **Live Demo:** [skyfare-app.streamlit.app](https://skyfare-app.streamlit.app)

---

## Overview

SKYFARE uses a trained ML model to estimate flight ticket prices based on route, airline, schedule, and duration. The model was trained on **10,683 real domestic flight records** and achieves an **R² of 0.80** with a **Mean Absolute Error of ₹1,171**.

---

## Project Structure

```
skyfare/
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
├── app.py                          # Streamlit web application
├── flight_price_prediction.ipynb   # Model training & EDA notebook
├── flight_price_training_data.xlsx # Raw training dataset — 10,683 flights
├── flight_price_model.pkl          # Trained Random Forest model
├── model_meta.json                 # Encoded labels & feature metadata
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

---

## Features

- Predicts Indian domestic flight prices in INR
- Covers major airlines and routes across India
- Supports non-stop to 4-stop flight configurations
- Clean, editorial-style dark UI with custom CSS
- Fully responsive on mobile and desktop

---

## Machine Learning Pipeline

**1. Data Preprocessing**
- Parsed date, departure time, and arrival time into structured features (day, month, hour, minute)
- Extracted flight duration into separate hours and minutes columns
- Dropped low-signal columns: `Route`, `Additional_Info`, `Duration` (raw), `Journey_year`

**2. Feature Engineering**
- One-hot encoded `Source` cities (Bangalore, Delhi, Chennai, Mumbai, Kolkata)
- Mean-price label encoded `Airline` and `Destination`
- Ordinally encoded `Total_Stops` (non-stop → 0, up to 4 stops → 4)

**3. Feature Selection**
- Used `mutual_info_regression` to rank feature importance
- Top features: `Total_Stops`, `Duration_hours`, `Airline`, `Destination`

**4. Model Training**
- Model: `RandomForestRegressor` (scikit-learn)
- Split: 75% train / 25% test (`random_state=42`)
- Outlier analysis performed using IQR method

**5. Model Performance**

| Metric | Value |
|--------|-------|
| R² Score | 0.80 |
| MAE | ₹1,171 |
| Training Samples | 10,683 |

---

## Usage

1. Select your **departure city** and **destination**
2. Choose your **airline** and number of **stops**
3. Pick your **journey date**, **departure** and **arrival times**
4. Enter the **flight duration** (hours and minutes)
5. Click **Calculate Fare →** to get your price estimate

---

## Run Locally

```bash
streamlit run app.py
```

---

## Dataset

The training data (`flight_price_training_data.xlsx`) contains domestic Indian flight records with the following original columns:

`Airline`, `Date_of_Journey`, `Source`, `Destination`, `Route`, `Dep_Time`, `Arrival_Time`, `Duration`, `Total_Stops`, `Additional_Info`, `Price`

**Supported Airlines:** IndiGo, Air India, Jet Airways, SpiceJet, Vistara, GoAir, Multiple Carriers, and more.

**Supported Routes:** Bangalore, Delhi, Chennai, Mumbai, Kolkata to major Indian metros.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit + Custom CSS |
| ML Model | scikit-learn RandomForestRegressor |
| Data Processing | pandas, numpy |
| Model Serialization | joblib |
| Visualization | matplotlib, seaborn |
| Fonts | Bebas Neue, Barlow (Google Fonts) |
| Hosting | Streamlit Community Cloud |

---

## Author

Built by **Kshitish**

---

