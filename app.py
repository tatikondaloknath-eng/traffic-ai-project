from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

# ---------------------------------------
# DATASET PATH
# ---------------------------------------

DATASET_PATH = os.path.join("data", "traffic_dataset.csv")


# ---------------------------------------
# LOAD DATASET
# ---------------------------------------

def load_dataset():

    df = pd.read_csv(DATASET_PATH)

    # Remove unnecessary index column
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # Remove duplicate records
    df = df.drop_duplicates()

    # Remove rows containing missing values
    df = df.dropna()

    return df


# ---------------------------------------
# TRAFFIC LEVEL
# ---------------------------------------

def calculate_traffic_level(row):

    vehicle_count = row["vehicle_count"]
    waiting_time = row["waiting_time"]
    lane_occupancy = row["lane_occupancy"]

    # High traffic
    if (
        vehicle_count >= 100
        or waiting_time >= 60
        or lane_occupancy >= 75
    ):
        return "HIGH"

    # Medium traffic
    elif (
        vehicle_count >= 60
        or waiting_time >= 30
        or lane_occupancy >= 50
    ):
        return "MEDIUM"

    # Low traffic
    else:
        return "LOW"


# ---------------------------------------
# DASHBOARD
# ---------------------------------------

@app.route("/")
def dashboard():

    df = load_dataset()

    # Add traffic level
    df["traffic_level"] = df.apply(
        calculate_traffic_level,
        axis=1
    )

    # Statistics
    total_records = len(df)

    total_vehicles = int(
        df["vehicle_count"].sum()
    )

    average_waiting_time = round(
        df["waiting_time"].mean(),
        2
    )

    average_speed = round(
        df["average_speed"].mean(),
        2
    )

    average_occupancy = round(
        df["lane_occupancy"].mean(),
        2
    )

    high_traffic = int(
        (df["traffic_level"] == "HIGH").sum()
    )

    medium_traffic = int(
        (df["traffic_level"] == "MEDIUM").sum()
    )

    low_traffic = int(
        (df["traffic_level"] == "LOW").sum()
    )

    # Latest/sample records
    records = df.head(20).to_dict(
        orient="records"
    )

    return render_template(
        "dashboard.html",
        total_records=total_records,
        total_vehicles=total_vehicles,
        average_waiting_time=average_waiting_time,
        average_speed=average_speed,
        average_occupancy=average_occupancy,
        high_traffic=high_traffic,
        medium_traffic=medium_traffic,
        low_traffic=low_traffic,
        records=records
    )


# ---------------------------------------
# DATA API
# ---------------------------------------

@app.route("/api/traffic")
def traffic_api():

    df = load_dataset()

    df["traffic_level"] = df.apply(
        calculate_traffic_level,
        axis=1
    )

    return jsonify(
        df.head(100).to_dict(
            orient="records"
        )
    )


# ---------------------------------------
# RUN APPLICATION
# ---------------------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
