"""
Author : Ryan Mehra
Script to generate charts and trends supporting paper:
Undoing the Damage: Holistic Paths to Correcting Social Media-Induced Spinal Health Issues and Mental Well-Being
License: Creative Commons (CC BY 4.0)
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline
from math import pi

# Loading the data
xls = "DataCollection.xlsx" ## Put the appropriate path to the Excel file
df_new = pd.read_excel(xls, sheet_name='Survey Raw')

# Clean column names to remove special characters and spaces
df_new.columns = df_new.columns.str.strip().str.replace(r'\n|\[|\]', '', regex=True)

# Convert relevant columns to numeric where applicable for analysis
df_new['Energy Level 0 - 10 '] = pd.to_numeric(df_new['Energy Level 0 - 10 '], errors='coerce')
df_new['Mood 0 - 10 '] = pd.to_numeric(df_new['Mood 0 - 10 '], errors='coerce')
df_new['Mental Clarity 0 - 10 '] = pd.to_numeric(df_new['Mental Clarity 0 - 10 '], errors='coerce')
df_new['Anxiety 0 - 10 '] = pd.to_numeric(df_new['Anxiety 0 - 10 '], errors='coerce')
df_new['Pain During Yoga 0 - 10 '] = pd.to_numeric(df_new['Pain During Yoga 0 - 10 '], errors='coerce')

# Candidate separation for plotting
candidates = df_new['Candidate'].unique()
colors = sns.color_palette("husl", len(candidates))  # Defining the color palette for candidates

# Dropping any non-numeric or invalid data
df_cleaned_heart_rate = df_new.dropna(subset=['Max Heart Rate During Walk/Run'])

# 1. Energy Level heatmap
energy_pivot = df_new.pivot_table(index='Day', columns='Candidate', values='Energy Level 0 - 10 ')

# Generating the heatmap for energy levels over time
plt.figure(figsize=(10, 6))
sns.heatmap(energy_pivot, cmap="YlGnBu", annot=True)
plt.title('Energy Levels Over Time')
plt.xlabel('Candidate')
plt.ylabel('Day')
plt.show()

# 2. Violin Plot for Mood Levels
plt.figure(figsize=(10, 6))
sns.violinplot(x='Candidate', y='Mood 0 - 10 ', data=df_new, palette="muted")
plt.title('Distribution of Mood Levels')
plt.xlabel('Candidate')
plt.ylabel('Mood Levels')
plt.grid(True)
plt.show()

# 3. Line Plot with Markers for Mental Clarity Levels
plt.figure(figsize=(10, 6))
for i, candidate in enumerate(candidates):
    df_candidate = df_new[df_new['Candidate'] == candidate]
    plt.plot(df_candidate['Day'], df_candidate['Mental Clarity 0 - 10 '], marker='o', linestyle='-', label=f'Candidate {candidate}', color=colors[i])

plt.title('Mental Clarity Levels Over Time')
plt.xlabel('Day')
plt.ylabel('Mental Clarity Levels')
plt.legend()
plt.grid(True)
plt.show()

# 4. Generating a step plot for anxiety levels over time
plt.figure(figsize=(10, 6))
for i, candidate in enumerate(candidates):
    df_candidate = df_new[df_new['Candidate'] == candidate]
    plt.step(df_candidate['Day'], df_candidate['Anxiety 0 - 10 '], where='mid', label=f'Candidate {candidate}', color=colors[i])

plt.title('Anxiety Levels Over Time')
plt.xlabel('Day')
plt.ylabel('Anxiety Level')
plt.legend()
plt.grid(True)
plt.show()

# 5. Heart Rate Trend Spline Plot (Smooth Line Plot)
plt.figure(figsize=(10, 6))

for i, candidate in enumerate(candidates):
    df_candidate = df_new[df_new['Candidate'] == candidate].dropna(subset=['Max Heart Rate During Walk/Run'])  # Dropping invalid heart rate data
    x_new = np.linspace(df_candidate['Day'].min(), df_candidate['Day'].max(), 300)  # Adding more points for smoothness
    spl = make_interp_spline(df_candidate['Day'], df_candidate['Max Heart Rate During Walk/Run'], k=3)
    y_smooth = spl(x_new)
    
    plt.plot(x_new, y_smooth, label=f'Candidate {candidate}', color=colors[i])

plt.title('Heart Rate Trend (Smooth Spline Plot)')
plt.xlabel('Day')
plt.ylabel('Max Heart Rate During Walk/Run')
plt.legend()
plt.grid(True)
plt.show()

# 6. Radar (Spider) Chart
# Replacing the non-numeric values with appropriate numeric equivalents for posture improvement
df_new['Overall Posture Improvement 1 -5 degrees '] = df_new['Overall Posture Improvement 1 -5 degrees '].replace({
    '~1 degree': 1,
    '~ greater than 3 degree': 3,
    '~ greater than 5 degrees': 5
})

# Preparing data for radar chart
overall_posture_correction_normalized = df_new.groupby('Candidate')['Overall Posture Improvement 1 -5 degrees '].max()

categories = list(overall_posture_correction_normalized.index)
N = len(categories)

# Adding the first value to close the radar chart
values = overall_posture_correction_normalized.values.flatten().tolist()
values += values[:1]

# Creating the angles for the radar chart
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Radar chart plot
plt.figure(figsize=(6, 6))
ax = plt.subplot(111, polar=True)
plt.xticks(angles[:-1], categories)

# Plotting the data
ax.plot(angles, values, linewidth=2, linestyle='solid', marker='o')
ax.fill(angles, values, color='orange', alpha=0.4)
plt.show()

# Percentage Gain Calculations
percentage_gains = {}

# 1. Heart Rate Reduction
initial_heart_rate = df_new.groupby('Candidate')['Max Heart Rate During Walk/Run'].first()
final_heart_rate = df_new.groupby('Candidate')['Max Heart Rate During Walk/Run'].last()
heart_rate_reduction = (initial_heart_rate - final_heart_rate) / initial_heart_rate * 100
percentage_gains['Heart Rate Reduction (%)'] = heart_rate_reduction.mean()

# 2. Energy Levels
initial_energy = df_new.groupby('Candidate')['Energy Level 0 - 10 '].first()
final_energy = df_new.groupby('Candidate')['Energy Level 0 - 10 '].last()
energy_increase = (final_energy - initial_energy) / initial_energy * 100
percentage_gains['Energy Level Increase (%)'] = energy_increase.mean()

# 3. Mental Clarity Improvement
initial_clarity = df_new.groupby('Candidate')['Mental Clarity 0 - 10 '].first()
final_clarity = df_new.groupby('Candidate')['Mental Clarity 0 - 10 '].last()
clarity_increase = (final_clarity - initial_clarity) / initial_clarity * 100
percentage_gains['Mental Clarity Increase (%)'] = clarity_increase.mean()

# 4. Anxiety Reduction
initial_anxiety = df_new.groupby('Candidate')['Anxiety 0 - 10 '].first()
final_anxiety = df_new.groupby('Candidate')['Anxiety 0 - 10 '].last()
anxiety_reduction = (initial_anxiety - final_anxiety) / initial_anxiety * 100
percentage_gains['Anxiety Reduction (%)'] = anxiety_reduction.mean()

# 5. Pain Reduction During Yoga
initial_pain = df_new.groupby('Candidate')['Pain During Yoga 0 - 10 '].first()
final_pain = df_new.groupby('Candidate')['Pain During Yoga 0 - 10 '].last()
pain_reduction = (initial_pain - final_pain) / initial_pain * 100
percentage_gains['Pain Reduction (%)'] = pain_reduction.mean()

# 6. Posture Improvement
initial_posture = 0  # Assume no initial improvement
final_posture = df_new.groupby('Candidate')['Overall Posture Improvement 1 -5 degrees '].max()
posture_improvement = (final_posture - initial_posture) / 5 * 100  # Assuming max of 5 degrees improvement
percentage_gains['Posture Improvement (%)'] = posture_improvement.mean()

# 7. Calculating Mood Improvement
initial_mood = df_new.groupby('Candidate')['Mood 0 - 10 '].first()
final_mood = df_new.groupby('Candidate')['Mood 0 - 10 '].last()
mood_increase = (final_mood - initial_mood) / initial_mood * 100
percentage_gains['Mood Improvement (%)'] = mood_increase.mean()

# Display the updated percentage gains including mood improvement
print(percentage_gains)