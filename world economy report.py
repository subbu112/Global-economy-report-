#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np
world_bank = pd.read_excel ("WorldBank.xlsx").rename ({"Country Name": "Country"}, axis=1)
world_bank ["Population (M)"] = (world_bank ["GDP (USD)"]/world_bank ["GDP per capita (USD)"] / 1_000_000)
world_bank.head ()


# In[ ]:





# In[7]:


world_bank.info()


# In[8]:


world_bank.describe()


# In[9]:


hdi=pd.read_csv("hdi.csv")
wb_hdi_2014 = world_bank.query("Year == 2014"). merge (hdi [["iso3", "hdi_2014"]], how="left", left_on="Country Code", right_on="iso3")
wb_hdi_2014.head()


# In[10]:


wb_hdi_2014.describe()


# In[11]:


gdp_pivot = world_bank.pivot_table(index="Year", columns="Region", values="GDP (USD)", aggfunc="sum")
gdp_pivot.head()


# In[12]:


pop_pivot = world_bank. pivot_table(index="Year", columns="Region", values="Population (M)", aggfunc="sum")
pop_pivot.head()


# In[13]:


wb_hdi_by_region = wb_hdi_2014.groupby("Region").agg ({"hdi_2014": "mean"}).sort_values ("hdi_2014", ascending=False)
wb_hdi_by_region.head()


# In[14]:


import matplotlib.pyplot as plt
import seaborn as sns

# Assuming gdp_pivot is a pre-defined DataFrame with a proper structure
fig, ax = plt.subplots()
ax.stackplot(
    gdp_pivot.index,
    [gdp_pivot[region]/1_000_000_000_000 for region in gdp_pivot.iloc[-1].sort_values(ascending=False).index],
    labels=[region for region in gdp_pivot.iloc[-1].sort_values(ascending=False).index]
)
ax.legend(loc="upper left")
ax.set_title("GDP has Grown Exponentially")
ax.set_ylabel("GDP in Trillions")
plt.show()




# In[15]:


import matplotlib.pyplot as plt
import seaborn as sns

# Assuming pop_pivot is a pre-defined DataFrame
fig, ax = plt.subplots()
ax.stackplot(
    pop_pivot.index,
    [pop_pivot[region]/1000 for region in pop_pivot.iloc[-1].sort_values(ascending=False).index],
    labels=[region for region in pop_pivot.iloc[-1].sort_values(ascending=False).index]
)
ax.legend(loc="upper left")
ax.set_title("Popluation has Surged from 2.5 billion to 7 billion")
ax.set_ylabel("Population in Billions")
plt.show()


# In[16]:


sns.scatterplot(
data=wb_hdi_2014,
x="Life expectancy at birth (years)",
y="GDP per capita (USD)",
)


# In[18]:


wb_hdi_by_region.plot.bar(title="HDI by region",ylabel="Human Development Index HDI")


# In[19]:


sns.scatterplot(
    data=wb_hdi_2014.query("Country != 'Iceland'"),
    x="Electric power consumption (kWh per capita)",
    y="GDP per capita (USD)",
    hue="hdi_2014",
    palette="coolwarm_r"
).set(title="Electricity Drives Development")


# In[72]:


import seaborn as sns
import matplotlib.pyplot as plt

# Calculating correlation matrix
corr = wb_hdi_2014[['Life expectancy at birth (years)', 'GDP per capita (USD)', ]].corr()

# Plotting heatma
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Correlation between Various Health and Economic Indicators')
plt.show()


# In[76]:


data_for_plotting = wb_hdi_2014[['Life expectancy at birth (years)', 'GDP per capita (USD)', 'Population (M)', 'Region']].dropna()



# In[77]:


# Create the pair plot
pair_plot = sns.pairplot(data=data_for_plotting, hue='Region', height=3,
                         vars=['Life expectancy at birth (years)', 'GDP per capita (USD)', 'Population (M)'],
                         diag_kind='kde',  # KDE plots on the diagonal
                         plot_kws={'alpha': 0.6, 's': 80, 'edgecolor': 'k'},  # Adjust scatter plot properties
                         palette='viridis')  # Color palette for different regions

# Set titles and labels for better readability (optional)
pair_plot.fig.suptitle('Pairwise Relationships Between Life Expectancy, GDP Per Capita, and Population by Region', y=1.02)

# Display the plot
plt.show()


# In[81]:


import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

# Creating the figure and specifying the grid layout
fig = plt.figure(figsize=(15, 30))
gs = GridSpec(6, 1, figure=fig, height_ratios=[2, 2, 1.5, 1.5, 0.1, 1.5])  # Allocate more space to certain plots

# Adjust the spacing more precisely
plt.subplots_adjust(hspace=0.4, top=0.95)

# GDP Stack Plot
ax1 = fig.add_subplot(gs[0, 0])
ax1.stackplot(
    gdp_pivot.index,
    [gdp_pivot[region]/1_000_000_000_000 for region in gdp_pivot.iloc[-1].sort_values(ascending=False).index],
    labels=[region for region in gdp_pivot.iloc[-1].sort_values(ascending=False).index]
)
ax1.legend(loc="upper left")
ax1.set_title("GDP has Grown Exponentially", fontsize=16)
ax1.set_ylabel("GDP in Trillions", fontsize=14)

# Population Stack Plot
ax2 = fig.add_subplot(gs[1, 0])
ax2.stackplot(
    pop_pivot.index,
    [pop_pivot[region]/1000 for region in pop_pivot.iloc[-1].sort_values(ascending=False).index],
    labels=[region for region in pop_pivot.iloc[-1].sort_values(ascending=False).index]
)
ax2.legend(loc="upper left")
ax2.set_title("Population has Surged from 2.5 billion to 7 billion", fontsize=16)
ax2.set_ylabel("Population in Billions", fontsize=14)

# Scatter Plot for Life Expectancy vs GDP Per Capita
ax3 = fig.add_subplot(gs[2, 0])
scatter_plot = sns.scatterplot(
    data=wb_hdi_2014,
    x="Life expectancy at birth (years)",
    y="GDP per capita (USD)",
    ax=ax3,
    s=120  # Increased marker size
)
ax3.set_title("Life Expectancy vs GDP Per Capita", fontsize=16)
ax3.set_xlabel("Life expectancy at birth (years)", fontsize=14)
ax3.set_ylabel("GDP per capita (USD)", fontsize=14)
scatter_plot.grid(False)  # Remove grid

# Bar Chart for HDI by Region
ax4 = fig.add_subplot(gs[3, 0])
wb_hdi_by_region.plot.bar(ax=ax4)
ax4.set_title("HDI by Region", fontsize=16)
ax4.set_ylabel("Human Development Index (HDI)", fontsize=14)

# Add an empty space row for better spacing
ax5 = fig.add_subplot(gs[4, 0])
ax5.axis('off')

# Heatmap for Correlation
ax6 = fig.add_subplot(gs[5, 0])
corr = wb_hdi_2014[['Life expectancy at birth (years)', 'GDP per capita (USD)']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax6)
ax6.set_title('Correlation between Various Health and Economic Indicators', fontsize=16)

# Show the full figure with all plots
plt.show()


# In[ ]:




