import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import pycountry # for plotting values in world map
import plotly as pl
import plotly.express as px # for plotting values in world map

import matplotlib.dates as mdate  # used to change date formats
import sys  # sys is used for using exit command


# Read the excel file
data = pd.ExcelFile(r'E:\DataAnalysis\Covid19\Worldwide_owid-covid-data\owid-covid-data_November-1.xlsx')

# Get all sheets names
sheets = data.sheet_names
print(sheets)


## Get information of one sheet
df = pd.read_excel(data, "Sheet1")
# print(df.head())




## Setting the index of the dataframe to a prticular column
df2 = df.set_index("location", drop=False)
# print(df2.head())

## Extracting elements from a dataframe column

# print(df[df["location"].str.contains('India')])  # Extracts all the data which contains "India" in the column "location"

countries = ['United States', 'India', 'Brazil', 'Russia', 'France', 'Spain', 'Italy', 'Germany'] # Countries to be analysed

print(countries[2])


df_countries = list()  # Creating an empty list for storing the various dataframr
countries_population = list() # Creating an empty list for storing the polpulation of each country in the list
for num, country in enumerate(countries):
    dff = df[df["location"].str.contains(country+'$')]  # Makes a new dataframe which contains "country name" in the
    # column "location" and the added '$' sign gives 'India$' command which means it will only choose those str which
    # ends with "India". i.e if there is some string with “India Population”, then this command will not choose that string.
    dff = dff.replace(np.nan, 0) # Replace the NaN values with 0 in dataframe
    df_countries.append(dff)  # Storing dataframe in a list
    popultn = (df_countries[num]['population']).mean()
    countries_population.append(popultn)
print(df_countries[5]['total_deaths'])

# sys.exit()

# plt.bar(countries, countries_population)
# plt.show()

# sys.exit() # Exit from the script

## Plotting covid cases in world map online.

plot_map = ['total_cases', 'total_deaths']

for variabl in plot_map:
    fig = px.choropleth(data_frame = df,
                    locations= "iso_code", # Location of the map in world map
                    color= variabl,  # value in column 'total_cases' determines color of the map
                    hover_name= "location", # Name of the country
                    color_continuous_scale= 'Viridis',  #   color scale red, yellow green .. can use px.colors.sequential.Plasma instead of 'RdYlGn'
                    # range_color = (0, 10000000), # Takes upper limit of color bar as 10M (Million)
                    animation_frame= "date") # The slider axis of the plot.

    fig.update_layout(
    title_text = 'Country wise development of covid cases with time throughout the World'  ## Updatin
    )

    # Save to html
    pl.offline.plot(fig, filename='E:\DataAnalysis\Covid19\All_Project_Covid\worldwide_' + variabl + '_covid_map_Santanu.html') ## Saves the plotted map

# fig.show()

sys.exit() # Exit from the script

def millions(x, pos):  # converting the number to millions
    'The two args are the value and tick position'
    return '%1.1fM' % (x * 1e-6)

def thousands(x, pos): # converting the number to thousand
    'The two args are the value and tick position'
    return '%1.1fK' % (x * 1e-3)


## Plot for a specific country "India"

fig, axs1 = plt.subplots()
color = 'tab:blue'
axs1.yaxis.set_major_formatter(FuncFormatter(thousands))
axs1.bar(df_countries[1]["date"], df_countries[1]['new_cases'], color=color)
axs1.set_xlabel("Date", fontsize=20)
axs1.set_ylabel("New cases each day", color=color, fontsize=20)
axs1.set_ylim([0, None])  # sets the y-limit of the plot 0 to end
# axs1.set_xticks([])
axs1.set_xticks(df_countries[1]["date"][::30])  # sets only 30th value as tick
axs1.set_xticklabels(df_countries[1]["date"][::30], rotation=90) # Print each 30th x_value at 90 degree
axs1.tick_params(axis='y', labelcolor=color)

axs2 = axs1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:red'
axs2.plot(df_countries[1]["date"], df_countries[1]["total_cases"], color=color, linewidth=3)
axs2.yaxis.set_major_formatter(FuncFormatter(millions))
axs2.set_ylabel("Total Number of cases", color=color, fontsize=20)
axs2.set_ylim([0, None])  # sets the y-limit of the plot 0 to end
axs2.set_xticks(df_countries[1]["date"][::30])  # Print each 30th x_value
axs2.set_xticklabels(df_countries[1]["date"][::30], rotation=90)
axs2.tick_params(axis='y', labelcolor=color)

plt.tight_layout()  # otherwise the labels (x,y) are slightly clipped
plt.subplots_adjust(top=0.92) # Reduce the plot space to make space for title (title will not be clipped)
plt.title("India's Total and Daily Covid-19 Cases", fontsize=20)
plt.savefig('E:\DataAnalysis\Covid19\All_Project_Covid\India_Total_and_Daily_Covid-19_Cases.png') # SAVING THE FIGURE

# plt.show()
# sys.exit()
## Plot of highly increasing covid-19 cases in different Countries

fig, axes = plt.subplots(2, 2)
fig.set_size_inches(13, 7)  # Sets the overall figure size in inches

for i, axs in enumerate(axes.flatten()):

    color = 'tab:blue'
    axs.yaxis.set_major_formatter(FuncFormatter(thousands))
    axs.bar(df_countries[i]["date"], df_countries[i]['new_cases'], color=color) # Bar plot for showing daily cases
    axs.set_xlabel("Date", fontsize=8, fontweight='bold')
    axs.set_ylabel("New cases each day", color=color, fontsize=8, fontweight='bold')
    axs.set_ylim([0, None])  # sets the y-limit of the plot 0 to end
    # axs[0, 0].set_xticks([])
    axs.set_xticks(df_countries[i]["date"][::30])  # sets only 30th value as tick
    axs.set_xticklabels(df_countries[i]["date"][::30], rotation=90, fontsize=5, fontweight='bold') # Print each 30th x_value at 90 degree
    axs.tick_params(axis='y', labelcolor=color, labelsize=8)

    axs2 = axs.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    axs2.plot(df_countries[i]["date"], df_countries[i]["total_cases"], color=color, linewidth=3)
    axs2.yaxis.set_major_formatter(FuncFormatter(millions))
    axs2.set_ylabel("Total Number of cases", color=color, fontsize=8, fontweight='bold')
    axs2.set_ylim([0, None])  # sets the y-limit of the plot 0 to end
    axs2.set_xticks(df_countries[i]["date"][::30])  # Print each 30th x_value
    axs2.set_xticklabels(df_countries[i]["date"][::30], rotation=90, fontsize=4, fontweight='bold')
    axs2.tick_params(axis='y', labelcolor=color, labelsize=8)
    # axs2.legend(countries[i], fontsize=4)
    plt.title([countries[i], "Covid-19 Cases"], fontsize=8, fontweight='bold')
    plt.tight_layout()  # otherwise the labels (x,y) are slightly clipped
    plt.subplots_adjust(top=0.90)  # Reduce the plot space to make space for title (title will not be clipped)
    fig.suptitle("Top four countries with Covid-19 Cases", fontsize=10, fontweight='bold', color='c')
# plt.subplots_adjust(top=0.92) # Reduce the plot space to make space for title (title will not be clipped)

plt.savefig('E:\DataAnalysis\Covid19\All_Project_Covid\World_Total_and_Daily_Covid-19_Cases.png') # SAVING THE FIGURE
# plt.show()

## Plot to show second waves of covid-19 in different Countries

fig, axes2 = plt.subplots(2, 2)
fig.set_size_inches(13, 7)  # Sets the overall figure size in inches

for nn, axs in enumerate(axes2.flatten()):

    color = 'tab:blue'
    axs.yaxis.set_major_formatter(FuncFormatter(thousands))  # %.0f for no decimal point
    axs.bar(df_countries[nn+4]["date"], df_countries[nn+4]['new_cases'], color=color)
    axs.set_xlabel("Date", fontsize=8, fontweight='bold')
    axs.set_ylabel("New cases each day", color=color, fontsize=8, fontweight='bold')
    axs.set_ylim([0, None])  # sets the y-limit of the plot 0 to end
    # axs[0, 0].set_xticks([])
    axs.set_xticks(df_countries[nn+4]["date"][::30])  # sets only 30th value as tick
    axs.set_xticklabels(df_countries[nn+4]["date"][::30], rotation=90, fontsize=5, fontweight='bold') # Print each 30th x_value at 90 degree
    axs.tick_params(axis='y', labelcolor=color, labelsize=8)

    axs2 = axs.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    axs2.plot(df_countries[nn+4]["date"], df_countries[nn+4]["total_cases"], color=color, linewidth=3)
    axs2.yaxis.set_major_formatter(FuncFormatter(millions))
    axs2.set_ylabel("Total Number of cases", color=color, fontsize=8, fontweight='bold')
    axs2.set_ylim([0, None])  # sets the y-limit of the plot 0 to end
    axs2.set_xticks(df_countries[nn+4]["date"][::30])  # Print each 30th x_value
    axs2.set_xticklabels(df_countries[nn+4]["date"][::30], rotation=90, fontsize=4, fontweight='bold')
    axs2.tick_params(axis='y', labelcolor=color, labelsize=8)
    # axs2.legend(countries[nn+3], fontsize=4)
    plt.title([countries[nn+4], "Covid-19 Cases"], fontsize=8, fontweight='bold')
    plt.tight_layout()  # otherwise the labels (x,y) are slightly clipped
    plt.subplots_adjust(top=0.90)  # Reduce the plot space to make space for title (title will not be clipped)
    fig.suptitle("Covid 2nd-wave in European Countries", fontsize=10, fontweight='bold', color='c')
# plt.subplots_adjust(top=0.92) # Reduce the plot space to make space for title (title will not be clipped)
# plt.title("India's Total and Daily Covid-19 Cases", fontsize=20)
plt.savefig('E:\DataAnalysis\Covid19\All_Project_Covid\Europe_2nd_Covid-19_Cases.png') # SAVING THE FIGURE

## Plot of highly increasing covid-19 cases in different Countries

fig, axes = plt.subplots(2, 4)
fig.set_size_inches(13, 7)  # Sets the overall figure size in inches


for i, axs in enumerate(axes.flatten()):

    color = 'tab:blue'
    axs.yaxis.set_major_formatter(FuncFormatter(thousands))
    axs.bar(df_countries[i]["date"], df_countries[i]["new_deaths"], color=color) # Bar plot for showing daily cases
    axs.set_xlabel("Date", fontsize=8, fontweight='bold')
    axs.set_ylabel("New deaths each day", color=color, fontsize=8, fontweight='bold')
    # axs[0, 0].set_xticks([])
    axs.set_ylim([0, None]) # sets the y-limit of the plot
    axs.set_xticks(df_countries[i]["date"][::30])  # sets only 30th value as tick
    axs.set_xticklabels(df_countries[i]["date"][::30], rotation=90, fontsize=5, fontweight='bold') # Print each 30th x_value at 90 degree
    axs.tick_params(axis='y', labelcolor=color, labelsize=8)

    axs2 = axs.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    axs2.plot(df_countries[i]["date"], df_countries[i]["total_deaths"], color=color, linewidth=3)
    axs2.yaxis.set_major_formatter(FuncFormatter(thousands))
    axs2.set_ylabel("Total deaths", color=color, fontsize=8, fontweight='bold')
    axs2.set_ylim([0, None])  # sets the y-limit of the plot
    axs2.set_xticks(df_countries[i]["date"][::30])  # Print each 30th x_value
    axs2.set_xticklabels(df_countries[i]["date"][::30], rotation=90, fontsize=6, fontweight='bold')
    axs2.tick_params(axis='y', labelcolor=color, labelsize=8)
    # axs2.legend(countries[i], fontsize=4)
    plt.title(countries[i], fontsize=8, fontweight='bold')
    plt.tight_layout()  # otherwise the labels (x,y) are slightly clipped
    plt.subplots_adjust(top=0.90)  # Reduce the plot space to make space for title (title will not be clipped)
    fig.suptitle("Covid Deaths in top few countries", fontsize=10, fontweight='bold', color='c')
# plt.subplots_adjust(top=0.92) # Reduce the plot space to make space for title (title will not be clipped)

plt.savefig('E:\DataAnalysis\Covid19\All_Project_Covid\World_Covid-19_deaths_Cases.png') # SAVING THE FIGURE
# plt.show()

## Plot of highly increasing covid-19 cases per million in different Countries

fig, axes = plt.subplots(2, 4)
fig.set_size_inches(13, 7)  # Sets the overall figure size in inches


for i, axs in enumerate(axes.flatten()):

    color = 'tab:blue'
    axs.yaxis.set_major_formatter(FuncFormatter(thousands))
    axs.bar(df_countries[i]["date"], df_countries[i]["total_cases_per_million"], color=color) # Bar plot for showing daily cases
    axs.set_xlabel("Date", fontsize=8, fontweight='bold')
    axs.set_ylabel("total_cases_per_million", color=color, fontsize=8, fontweight='bold')
    # axs[0, 0].set_xticks([])
    axs.set_ylim([0, None]) # sets the y-limit of the plot
    axs.set_xticks(df_countries[i]["date"][::30])  # sets only 30th value as tick
    axs.set_xticklabels(df_countries[i]["date"][::30], rotation=90, fontsize=5, fontweight='bold') # Print each 30th x_value at 90 degree
    axs.tick_params(axis='y', labelcolor=color, labelsize=8)

    axs2 = axs.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    axs2.plot(df_countries[i]["date"], df_countries[i]["total_deaths_per_million"], color=color, linewidth=3)
    # axs2.yaxis.set_major_formatter(FuncFormatter(thousands))
    axs2.set_ylabel("total deaths per million", color=color, fontsize=8, fontweight='bold')
    axs2.set_ylim([0, None])  # sets the y-limit of the plot
    axs2.set_xticks(df_countries[i]["date"][::30])  # Print each 30th x_value
    axs2.set_xticklabels(df_countries[i]["date"][::30], rotation=90, fontsize=6, fontweight='bold')
    axs2.tick_params(axis='y', labelcolor=color, labelsize=8)
    # axs2.legend(countries[i], fontsize=4)
    plt.title(countries[i], fontsize=8, fontweight='bold')
    plt.tight_layout()  # otherwise the labels (x,y) are slightly clipped
    plt.subplots_adjust(top=0.90)  # Reduce the plot space to make space for title (title will not be clipped)
    fig.suptitle("Covid cases and Deaths per million in top few countries", fontsize=10, fontweight='bold', color='c')
# plt.subplots_adjust(top=0.92) # Reduce the plot space to make space for title (title will not be clipped)

plt.savefig('E:\DataAnalysis\Covid19\All_Project_Covid\World_Covid-19_million_Cases.png') # SAVING THE FIGURE
plt.show()
