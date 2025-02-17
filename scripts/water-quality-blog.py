#!/usr/bin/env python

import pandas as pd
import requests
from datetime import datetime

# Google Sheet CSV export URL
url = "https://docs.google.com/spreadsheets/d/1YFSx__TXpx66LwODJISEisWmgKOZQVSMcMi1gJHfNfo/export?format=csv"

# Read data into DataFrame
data = pd.read_csv(url)

# Get the last row
last_row = data.iloc[-1]

date = last_row["Date"]
sample_time = last_row["Sample Time"]
flow_severity = last_row["Flow Severity"]
algae = last_row["Algae"]
water_surface = last_row["Water Surface"]
water_conditions = last_row["Water Conditions"]
present_weather = last_row["Present Weather"]
days_since_precip = last_row["Days Since Last Significant Precipitation"]
rainfall_accumulation = last_row[
    "Rainfall Accumulation (inches within the last 3 days)"
]
water_color = last_row["Water Color"]
water_clarity = last_row["Water Clarity"]
water_odor = last_row["Water Odor"]
air_temp = last_row["Air Temperature (celcius)"]
water_temp = last_row["Water Temperature (celcius)"]
pH = last_row["pH (standard units)"]
conductivity = last_row["Conductivity (microseimens/centimeter)"]
dissolved_oxygen = last_row["Dissolved Oxygen (milligram/liter)"]

# Analyze the data
analysis = []
if water_temp > 25:
    analysis.append(
        "The water temperature is high, which can reduce oxygen levels and affect aquatic life."
    )
if pH < 6.5 or pH > 8.5:
    analysis.append(
        "The pH level is outside the optimal range for most aquatic organisms."
    )
if conductivity > 5:
    analysis.append(
        "High conductivity can reduce light penetration and harm aquatic plants and animals."
    )
if dissolved_oxygen < 5:
    analysis.append(
        "Low dissolved oxygen levels can be harmful to fish and other aquatic organisms."
    )

if not analysis:
    analysis = ["Water quality parameters are within acceptable ranges."]

# Create Jekyll post
post_date = datetime.now().strftime("%Y-%m-%d")
file_name = f"_posts/{post_date}-water-quality.md"

content = f"""---
title: Water Quality Report for {date}
layout: post
date: {post_date}
author: jtdub
tags:
- jtdub.com
- community-science
- water quality
- san gabriel river
---

### Water Quality Data
- **Date:** {date}
- **Water Temperature:** {water_temp} °C
- **pH:** {pH}
- **Conductivity:** {conductivity} NTU
- **Dissolved Oxygen:** {dissolved_oxygen} mg/L

### Analysis
{" ".join(analysis)}

### Conclusion
This report provides insights into the current state of water quality. Continuous monitoring is essential to ensure a safe and healthy aquatic environment.
"""

with open(file_name, "w") as file:
    file.write(content)
