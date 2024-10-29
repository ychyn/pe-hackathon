# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# Analysis

# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# %%
# %pip install xlrd==2.0.1

# %%
df = pd.read_excel('DataForTable2023.xls')

# %%
df.head(5)

# %%
country = 'Country name'
year = 'year'
happiness = 'Life Ladder'
GDP = 'Log GDP per capita'
freedom = 'Freedom to make life choices'
life_exp = 'Freedom to make life choices'

# %%
df[df['Country name'] == 'Afghanistan'].plot(x = 'year')

# %%
afghanistan = df[df['Country name'] == 'Afghanistan']

fig, ax1 = plt.subplots()

# Plot the first y-axis
ax1.plot(afghanistan['year'], afghanistan[freedom], 'b-', label='y1')
ax1.set_ylabel(freedom + ' (blue)', color='b')
ax1.tick_params(axis='y', labelcolor='b')

# Create a second y-axis
ax2 = ax1.twinx()
ax2.plot(afghanistan['year'], afghanistan[happiness], 'r-', label='y2')
ax2.set_ylabel(happiness + ' (red)', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Optional: Add title and legend
plt.title('Multiple Y Axes Example')
fig.tight_layout()  # Adjust layout to prevent clipping
plt.show()

# %%
countries = df[country].unique()[:16]
num_countries = len(countries)
num_cols = 3  # Number of columns
num_rows = (num_countries + num_cols - 1) // num_cols  # Calculate number of rows needed

fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
axs = axs.flatten()  # Flatten the 2D array of axes for easy iteration

for i, countr in enumerate(countries):
    country_data = df[df[country] == countr]

    ax1 = axs[i]
    ax1.plot(country_data[year], country_data[happiness], 'b-', label='y1')
    ax1.set_ylabel(happiness, color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()
    ax2.plot(country_data[year], country_data[freedom], 'r-', label='y2')
    ax2.set_ylabel(freedom, color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    ax1.set_title(f'Data for {countr}')
    ax1.set_xlabel('X-axis')

plt.tight_layout()  # Adjust layout to prevent clipping
plt.show()

# %%
data_2022 = df[ df[year] == 2022]

# %%
data_2022[freedom]
data_2022[happiness]

# %%
fig, ax1 = plt.subplots()

# Plot the first y-axis
ax1.scatter(data_2022[freedom], data_2022[happiness], 'b-', label='y1')
ax1.set_ylabel(happinness + ' (blue)', color='b')
ax1.tick_params(axis='y', labelcolor='b')

# Optional: Add title and legend
plt.title('Multiple Y Axes Example')
fig.tight_layout()  # Adjust layout to prevent clipping
plt.show()

# %%
