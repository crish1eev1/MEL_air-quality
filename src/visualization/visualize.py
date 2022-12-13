import pandas as pd
from tabulate import tabulate
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from functools import reduce

import sys


# -----------------------------------------------------------------------------
# Using processed data as starting point
# -----------------------------------------------------------------------------
df = pd.read_pickle("../../data/processed/air-quality-index.pickle")


# -----------------------------------------------------------------------------
# Air quality overview
# -----------------------------------------------------------------------------
sorter = ["bon", "moyen", "dégradé", "mauvais", "très mauvais"]
counts = df["quality_label"].value_counts()
percent = df["quality_label"].value_counts(normalize=True)
percent100 = (
    df["quality_label"].value_counts(normalize=True).mul(100).round(1).astype(str) + "%"
)
global_proportion = pd.DataFrame({"percentage": percent100}).reindex(sorter)
global_proportion.rename(
    index={
        "très mauvais": "very poor",
        "mauvais": "poor",
        "dégradé": "moderate",
        "moyen": "fair",
        "bon": "good",
    },
    inplace=True,
)
print("\nMEL Air Quality Overview: \n")
print(tabulate(global_proportion, headers=["air quality", "%"], tablefmt="github"))

# -----------------------------------------------------------------------------
# # Days with polluted air - table
# -----------------------------------------------------------------------------
polluted_days = (
    df[df["quality_code"] >= 4]["quality_code"]
    .groupby("city")
    .agg("count")
    # .sort_values(ascending=False)
)


observed_days = (
    df["quality_code"]
    .groupby("city")
    .agg("count")
    # .sort_values(ascending=False)
)

polluted_days_table = pd.concat([polluted_days, observed_days], axis=1)
polluted_days_table.columns = ["polluted_days", "days"]
polluted_days_table["Proportion"] = (
    polluted_days_table["polluted_days"] / polluted_days_table["days"]
).round(3)
polluted_days_table.drop(["days"], axis=1, inplace=True)
polluted_days_table["Proportion"] = (polluted_days_table["Proportion"] * 100).astype(
    str
).str[:4] + "%"

print("\nPoor or Very poor air quality days proportion: \n")
print(
    tabulate(
        polluted_days_table,
        headers=["City", "Polluted days", "Proportion"],
        tablefmt="github",
    )
)
print("\n")


# -----------------------------------------------------------------------------
# Days with polluted air (poor or worse) - figure
# -----------------------------------------------------------------------------
# Creating a custom dataframe with days superior of certain index
air_quality_days = pd.DataFrame()

list_quality_code = list(range(1, 7))
df_days = {}
for code in list_quality_code:
    df_days[code] = (
        df[df["quality_code"] >= code]["quality_code"]
        .groupby("city")
        .agg("count")
        .to_frame()
        .reset_index()
    )
    df_days[code].columns = ["city", f"days_{code}_plus"]

df_days = [df_days[1], df_days[2], df_days[3], df_days[4], df_days[5], df_days[6]]

air_quality_days = reduce(
    lambda left, right: pd.merge(left, right, on=["city"], how="outer"), df_days
)

# bar graph styling
plt.style.use("default")
sns.set_theme(style="whitegrid")

# Tick Styling
mpl.rcParams["ytick.labelsize"] = "8"
mpl.rcParams["xtick.labelsize"] = "8"

# Legend Styling
mpl.rcParams["legend.framealpha"] = 0.8
mpl.rcParams["legend.fontsize"] = "x-small"
mpl.rcParams["legend.loc"] = "upper center"

# Title Styling
mpl.rcParams["axes.titlelocation"] = "left"
mpl.rcParams["axes.titlepad"] = 18
mpl.rcParams["axes.titlesize"] = 14
mpl.rcParams["axes.titleweight"] = "bold"

# Sorting df by Poor or worse
air_quality_days.sort_values(
    by=["days_4_plus", "days_5_plus", "days_6_plus"], ascending=False, inplace=True
)
air_quality_days["city"] = air_quality_days["city"].str.capitalize()

# Plot generation
f, ax = plt.subplots(figsize=(6, 18))

# Bars with conditional display for extreme values
sns.set_color_codes("pastel")
sns.barplot(y="city", x="days_4_plus", data=air_quality_days, label="Poor", color="r")

sns.set_color_codes("muted")
sns.barplot(
    y="city", x="days_5_plus", data=air_quality_days, label="Very poor", color="r"
)

if air_quality_days["days_6_plus"].notnull().sum() > 0:
    sns.set_color_codes("muted")
    sns.barplot(
        y="city",
        x="days_6_plus",
        data=air_quality_days,
        label="Extremely poor",
        color="k",
    )

# Add legend, title and labels
ax.set_title("Number of days with polluted air")
ax.set(xlabel="Days", ylabel="")
ax.legend(ncol=1, frameon=True)
ax.tick_params(
    axis="x", bottom=True, top=True, labelbottom=True, labeltop=True, labelsize=8
)

observed_days = len(df.unstack(level="city"))

# Subtitle
ax.text(
    x=0.138,
    y=-2.9,
    s='Days with "Poor" or worst air quality based on EAQI for a total of '
    + str(observed_days)
    + " days observed",
    # transform=fig.transFigure,
    ha="left",
    fontsize=6.5,
    alpha=0.7,
)
plt.savefig("..\\..\\reports\\figures\\polluted_days_poor.png")
print("polluted_days_poor.png saved\n")


# -----------------------------------------------------------------------------
# Days with polluted air (moderate or worse) - figure
# -----------------------------------------------------------------------------

# Sorting df by Moderate or worse
air_quality_days.sort_values(
    by=["days_3_plus", "days_4_plus", "days_5_plus", "days_6_plus"],
    ascending=False,
    inplace=True,
)
air_quality_days

air_quality_days["city"] = air_quality_days["city"].str.capitalize()


# Plot generation
f, ax = plt.subplots(figsize=(6, 18))

# Bars with conditional display for extreme values
sns.set_color_codes("pastel")
sns.barplot(
    y="city",
    x="days_3_plus",
    data=air_quality_days,
    label="Moderate",
    color="yellow",
    alpha=0.5,
)

sns.set_color_codes("pastel")
sns.barplot(y="city", x="days_4_plus", data=air_quality_days, label="Poor", color="r")

sns.set_color_codes("muted")
sns.barplot(
    y="city", x="days_5_plus", data=air_quality_days, label="Very poor", color="r"
)

if air_quality_days["days_6_plus"].notnull().sum() > 0:
    sns.set_color_codes("muted")
    sns.barplot(
        y="city",
        x="days_6_plus",
        data=air_quality_days,
        label="Extremely poor",
        color="k",
    )

# Add legend, title and labels
ax.set_title("Number of days with polluted air")
ax.set(xlabel="Days", ylabel="")
ax.legend(ncol=1, frameon=True)
ax.tick_params(
    axis="x", bottom=True, top=True, labelbottom=True, labeltop=True, labelsize=8
)

# Subtitle
ax.text(
    x=0.138,
    y=-2.9,
    s='Days with "Moderate" or worst air quality based on EAQI for a total of '
    + str(observed_days)
    + " days observed",
    # transform=fig.transFigure,
    ha="left",
    fontsize=6.5,
    alpha=0.7,
)

plt.savefig("..\\..\\reports\\figures\\polluted_days_moderate.png")
print("polluted_days_moderate.png saved\n")


# -----------------------------------------------------------------------------
# Evolution of each pollutant measurement in each city versus the agglomeration average
# -----------------------------------------------------------------------------

# Reset to default plot style just in case
plt.style.use("default")

# Style spines
mpl.rcParams["axes.linewidth"] = 0.8  # Spine edge line width
mpl.rcParams["axes.spines.top"] = False  # Removing top spine
mpl.rcParams["axes.spines.left"] = True  # default
mpl.rcParams["axes.spines.right"] = False  # Removing right spine
mpl.rcParams["axes.spines.bottom"] = True  # default

# Set line styling for line plots
mpl.rcParams["lines.linewidth"] = 2  # line width
mpl.rcParams[
    "lines.solid_capstyle"
] = "butt"  # Makes a square ending of the line stopping at datapoint

# Grid style
mpl.rcParams["axes.grid"] = True  # Adding grid
mpl.rcParams["axes.grid.axis"] = "y"  # default = 'both'
mpl.rcParams["grid.linewidth"] = 0.8
mpl.rcParams["grid.color"] = "#b0b0b0"
mpl.rcParams["axes.axisbelow"] = True  # default = 'line'

# Set spacing for figure and also DPI.
mpl.rcParams["figure.subplot.left"] = 0.125
mpl.rcParams["figure.subplot.right"] = 0.90
mpl.rcParams["figure.subplot.bottom"] = 0.10
mpl.rcParams["figure.subplot.top"] = 0.88
# mpl.rcParams['figure.figsize'] = 8, 4.8
mpl.rcParams["figure.dpi"] = 100

# Legend Styling
mpl.rcParams["legend.framealpha"] = 0.8
mpl.rcParams["legend.fontsize"] = "x-small"
mpl.rcParams["legend.loc"] = "best"

# Properties for saving the figure. Ensure a high DPI when saving so we have a good resolution.
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["savefig.facecolor"] = "white"
mpl.rcParams["savefig.bbox"] = "tight"
mpl.rcParams["savefig.pad_inches"] = 0.2

# Title styling
mpl.rcParams["axes.titlelocation"] = "left"
mpl.rcParams["axes.titlepad"] = 20
mpl.rcParams["axes.titlesize"] = 12
mpl.rcParams["axes.titleweight"] = "bold"

# Setting font sizes and spacing
mpl.rcParams["axes.labelsize"] = "small"
mpl.rcParams["xtick.labelsize"] = "x-small"
mpl.rcParams["ytick.labelsize"] = "small"
mpl.rcParams["font.size"] = 10
mpl.rcParams["xtick.major.pad"] = 3.5
mpl.rcParams["ytick.major.pad"] = 3.5


# Generating a set of cities
index_list = list(df.index.values)

set_city = set()
for i in index_list:
    set_city.add(i[0])

created_files = 0
created_files_list = []
list = [0, 1, 2, 3, 4]
pollutants = ["no2", "so2", "o3", "pm10", "pm2-5"]
colors = ["C0", "C1", "C2", "C3", "C4"]

for i in set_city:
    # Create all plots
    fig, axs = plt.subplots(5, 1, figsize=(8, 12))
    for n, p, c in zip(list, pollutants, colors):
        axs[n].plot(df.loc[(i), (p)].rolling(window=5).mean(), color=c)
        axs[n].plot(
            df.loc[(slice(None),), (p)]
            .groupby("date")
            .agg("mean")
            .rolling(window=3)
            .mean(),
            color=c,
            linewidth=1,
            linestyle=":",
        )

    # Format all plots
    for ax in axs:
        ax.set_ylim(bottom=0, top=5)
        ax.set_yticks(
            ticks=[1, 2, 3, 4, 5],
            labels=[
                "Good (1)",
                "Fair (2)",
                "Moderate (3)",
                "Poor (4)",
                "Very Poor (5)",
            ],
        )
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%Y"))

    # Main title
    axs[0].set_title(
        str(i).capitalize() + " - Air polluants vs agglomeration average", pad=30
    )

    # legends
    axs[0].legend(["Nitrogen dioxide (no2)", "Nitrogen dioxide MEL average"])
    axs[1].legend(["Sulfur dioxide (so2)", "Sulfur dioxide MEL average"])
    axs[2].legend(["Ozone (o3)", "Ozone MEL average"])
    axs[3].legend(["Particulate Matter (pm10)", "Particulate Matter MEL average"])
    axs[4].legend(["Particulate Matter (pm2.5)", "Particulate Matter MEL average"])

    # Subtitle
    axs[0].text(
        x=0.125,
        y=0.89,
        s="3 days rolling average of Nitrogen dioxide sub-Index based on European Air Quality Index (EAQI) standars versus \nthe average of the 95 cities that make up the Lille agglomeration.",
        transform=fig.transFigure,
        ha="left",
        fontsize=7,
        alpha=0.7,
    )

    # Source text
    axs[4].text(
        x=0.08,
        y=0.06,
        s="Source: Atmo Hauts-de-France via https://opendata.lillemetropole.fr",
        transform=fig.transFigure,
        ha="left",
        fontsize=6,
        alpha=0.6,
    )

    # Export plot as .png
    file_name = str(i) + "_air-polluants-vs-agglomeration" + ".png"
    plt.savefig(f"..\\..\\reports\\figures\\{file_name}")
    created_files += 1
    sys.stdout.write("\rSaving files: " + str(created_files) + "/95")
    sys.stdout.flush()

    # Avoid display with close method
    plt.close(fig)

print(f"\nAir pollutants graphs saved for {created_files} cities\n")


# -----------------------------------------------------------------------------
# Concatenating htlm variables to create an automated report
# -----------------------------------------------------------------------------
city_input = input(str("Pick a city from table above: ").lower())
main_title = "<h1> MEL Air Quality </h1>"
title1 = "<h3> MEL Air Quality Overview: </h3>"
title2 = "<h3> Poor or Very poor air quality days proportion: </h3>"
title3 = "<h3> Polluted days per city: </h3>"
title4 = f"<h3> Evolution of air pollutants in {city_input}: </h3>"
global_proportion_html = global_proportion.to_html(justify="right")
polluted_days_html = polluted_days_table.to_html(justify="right")
image_polluted_days1 = (
    '<p><img src="figures/polluted_days_1.png" alt="Polluted days poor and more"></p>'
)
image_polluted_days2 = '<p><img src="figures/polluted_days_2.png" alt="Polluted days average and more"></p>'
air_pollutants_image = f'<p><img src="figures/{city_input}_air-polluants-vs-agglomeration.png" alt="Pollutants" width="800"></p>'


html = (
    main_title
    + title1
    + global_proportion_html
    + title2
    + polluted_days_html
    + title3
    + image_polluted_days1
    + image_polluted_days2
    + title4
    + air_pollutants_image
)

with open("..\\..\\reports\\report.html", "w+") as f:
    f.write(html)

print("html report created")
