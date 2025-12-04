# campus-energy-dashboard-rishika
# Campus Energy Consumption Dashboard

**Submitted by:** RISHIKA BHAMBRI
**Course:** Programming for Problem Solving using Python

## 📌 Project Objective
This project analyzes electricity consumption data from multiple campus buildings to help the facilities team track energy usage. It automates data ingestion, cleaning, aggregation, and visualization.

## 🛠️ Methodology
1. **Data Ingestion:** Used `pandas` and `os` to automatically detect and merge multiple CSV files.
2. **Data Cleaning:** Handled missing values and converted timestamps for time-series analysis.
3. **OOP Implementation:** Designed `Building` and `MeterReading` classes to model the system.
4. **Analysis:** Calculated Daily/Weekly totals and Peak Load times using Pandas resampling.
5. **Visualization:** Created a dashboard with Trend Lines, Bar Charts, and Scatter Plots using `matplotlib`.

## 📊 Key Insights
- The dashboard automatically generates a summary of total energy consumption.
- It identifies the building with the highest energy usage.
- Peak load analysis helps in understanding consumption patterns across different hours.

## 📂 Project Structure
- `data/`: Contains raw CSV files (e.g., Building_Library.csv).
- `output/`: Generated reports and dashboard images.
- `main.py`: The main Python script.
