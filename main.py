import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import rcParams

for dirname, _, filenames in os.walk('/Users/james/Desktop/Project/HIV EDA'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

cases = pd.read_csv("no_of_cases_adults_15_to_49_by_country_clean.csv")
deaths = pd.read_csv("no_of_deaths_by_country_clean.csv")
living = pd.read_csv("no_of_people_living_with_hiv_by_country_clean.csv")
coverage = pd.read_csv("art_coverage_by_country_clean.csv")
pediatric = pd.read_csv("art_pediatric_coverage_by_country_clean.csv")
prevention = pd.read_csv("prevention_of_mother_to_child_transmission_by_country_clean.csv")

cases.head()
cases.info()
deaths.head()
living.head()
coverage.head()
coverage.info()
pediatric.head()
pediatric.info()
prevention.head()
prevention.info()

sns.set(color_codes=True)

casesbyregion = cases.groupby(["WHO Region", "Year"]).mean()["Count_median"]
sns.heatmap(casesbyregion.unstack(level=0), annot=True).set_title("HIV Cases by region and year")
plt.show()

deathbyregion = deaths.groupby(["WHO Region", "Year"]).sum()["Count_median"]
sns.heatmap(deathbyregion.unstack(level=0), annot=True).set_title("HIV deaths by region and year")
plt.show()

livingbyregion = living.groupby(["WHO Region", "Year"]).sum()["Count_median"]
sns.heatmap(livingbyregion.unstack(level=0), annot=True).set_title("People living with HIV by region and year")
plt.show()

death_sort = deaths.sort_values(by="Count_median", ascending=False)
rcParams["figure.figsize"] = 15, 10
death_barplot = sns.barplot(x="WHO Region", y="Count_median", data=death_sort[:]).set_title(
    "NO. of deaths due to HIV by year")
plt.show()

rcParams["figure.figsize"] = 10, 10
death_lineplot = sns.lineplot(x="Year", y="Count_median", data=death_sort[:]).set_title(
    "NO. of deaths due to HIV by year")
plt.show()

living_sort = living.sort_values(by="Count_median", ascending=False)
rcParams["figure.figsize"] = 15, 10
barplot = sns.barplot(x="WHO Region", y="Count_median", data=living_sort[:]).set_title("NO. of living with HIV by year")
plt.show()

rcParams["figure.figsize"] = 10, 10
living_lineplot = sns.lineplot(x="Year", y="Count_median", data=living_sort[:]).set_title(
    "NO. of living with HIV by year")
plt.show()

africa_df = cases[cases['WHO Region'] == 'Africa']
grouped_africa = africa_df.groupby('Country')['Count_median'].sum()
grouped_africa.plot(kind='bar', color='chocolate')
plt.title('HIV Number of 15-49 in African Countries')
plt.xlabel('Country')
plt.ylabel('Number')
plt.show()

plt.figure(figsize=(8, 6))
americas_df = cases[cases["WHO Region"] == "Americas"]
grouped_Americas = americas_df.groupby("Year")["Count_median"].sum()
plt.plot(grouped_Americas, color='blueviolet')
plt.title("Median HIV of 15-49 for Americas by Year")
plt.xlabel("Year")
plt.ylabel("Number")
plt.show()

coverage.hist()
pediatric.hist(color='lime')
prevention.hist(color='tan')

coverage.columns
coverage = coverage.drop([
    'Estimated number of people living with HIV', 'Estimated ART coverage among people living with HIV (%)',
    'Estimated number of people living with HIV_min',
    'Estimated number of people living with HIV_median',
    'Estimated number of people living with HIV_max',
    'Estimated ART coverage among people living with HIV (%)_min',
    'Estimated ART coverage among people living with HIV (%)_max'], axis=1)
coverage["ART"] = coverage["Reported number of people receiving ART"]
coverage["ART"] = pd.to_numeric(coverage["ART"], errors="coerce")
coverage["ART"] = coverage.ART.astype(float)
coverage.info()

coveragebyregion = coverage.groupby("WHO Region").sum()["ART"]
coveragebyregion.plot(kind='bar', subplots=True, figsize=(8, 8))
plt.title("People receiving ART by region")

coveragebyregion1 = coverage.groupby("WHO Region").mean()[
    "Estimated ART coverage among people living with HIV (%)_median"]
plt.figure(figsize=(10, 5))
sns.barplot(x=coveragebyregion1.index, y=coveragebyregion1).set_title("Estimated ART Coverage(%) by region")
plt.show()

grouped_coverage = coverage.groupby('WHO Region')['ART'].sum()
plt.figure(figsize=(10, 8))
plt.pie(grouped_coverage, labels=grouped_coverage.index, autopct='%.2f%%')
plt.title('People receiving ART by region')
plt.legend(loc='upper right')

pediatric.columns
pediatric = pediatric.drop([
    'Estimated number of children needing ART based on WHO methods',
    'Estimated ART coverage among children (%)',
    'Estimated number of children needing ART based on WHO methods_min',
    'Estimated number of children needing ART based on WHO methods_max',
    'Estimated ART coverage among children (%)_min',
    'Estimated ART coverage among children (%)_max'], axis=1)
pediatric["childrenART"] = pediatric["Reported number of children receiving ART"]
pediatric["childrenART"] = pd.to_numeric(pediatric["childrenART"], errors="coerce")
pediatric["childrenART"] = pediatric["childrenART"].astype(float)
pediatric.info()

pediatric_sort = pediatric.sort_values(by="childrenART", ascending=False)
plt.figure(figsize=(20, 5))
sns.barplot(x=pediatric_sort['Country'][:20], y=pediatric["childrenART"]).set_title(
    "Children receiving ART by Country")
plt.show()

pediatricbyregion = pediatric.groupby("WHO Region").sum()
plt.figure(figsize=(10, 5))
sns.barplot(x=pediatricbyregion.index, y=pediatricbyregion["childrenART"]).set_title(
    "Children receiving ART by region")
plt.show()

plt.figure(figsize=(10, 8))
plt.pie(pediatricbyregion['Estimated ART coverage among children (%)_median'],
        labels=pediatricbyregion.index, autopct='%.2f%%')
plt.title('People receiving ART by region')
plt.legend(loc='upper right')

prevention.columns
prevention = prevention.drop(['Needing antiretrovirals',
                              'Percentage Recieved',
                              'Needing antiretrovirals_min', 'Needing antiretrovirals_max',
                              'Percentage Recieved_min',
                              'Percentage Recieved_max'], axis=1)
prevention["recART"] = prevention["Received Antiretrovirals"]
prevention["recART"] = pd.to_numeric(prevention["recART"], errors='coerce')
prevention["recART"] = prevention["recART"].astype(float)
preventionbyregion = prevention.groupby("WHO Region").sum()

plt.figure(figsize=(10, 5))
sns.barplot(x=preventionbyregion.index, y=preventionbyregion["recART"]).set_title(
    "People received Antiretrovirals by region")
plt.show()

greater10 = cases[cases["Count_median"] >= 10]
plt.figure(figsize=(15, 10))
sns.lineplot(data=greater10, x="Year", y="Count_median", hue="Country").set_title(
    "Trend of top 10 countries with highest cases")
plt.show()

highestdeaths = deaths[deaths["Count_median"] >= 50000]
plt.figure(figsize=(15, 10))
sns.lineplot(data=highestdeaths, x="Year", y="Count_median", hue="Country").set_title(
    "Trend in countries with high HIV deaths")
plt.show()

plt.rcParams['font.sans-serif'] = ['SimHei']
preventionbyregion.plot(kind='line')
plt.title('Comparison of the three columns of preventionbyregion data by Region')
plt.show()

prevention.plot.scatter(x='recART', y='Percentage Recieved_median', c='Needing antiretrovirals_median',
                        colormap='viridis', alpha=0.7, s=100, linewidth=2)
plt.title('Scatter plot of three columns of data correlation analysis')
plt.show()
