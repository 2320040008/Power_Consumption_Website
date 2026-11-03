
import pandas as pd
import os

input_file = "energy_full.csv"
output_file = "energy_website.csv"

selected_columns = [
    "timestamp",
    "active_power_kw",
    "total_energy_kwh",
    "temperature_c",
    "humidity_pct",
    "solar_generation_kw",
    "occupants",
    "weather_condition",
    "holiday_flag",
    "school_holiday_flag",
    "hour",
    "day_of_week",
    "month",
    "power_lag_1",
    "power_lag_2",
    "power_lag_4",
    "power_lag_48",
    "power_lag_336"
]

if os.path.exists(output_file):
    os.remove(output_file)

first_chunk = True
total_rows = 0

for chunk in pd.read_csv(
    input_file,
    usecols=selected_columns,
    chunksize=50000
):
    chunk.to_csv(
        output_file,
        mode="w" if first_chunk else "a",
        header=first_chunk,
        index=False
    )

    total_rows += len(chunk)
    first_chunk = False

    print("Processed rows:", total_rows)

print("\nDataset optimisation completed!")
print("Total rows:", total_rows)
print("Output file:", output_file)
