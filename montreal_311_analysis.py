"""
Montreal 311 Service Requests — Data Cleaning & Analysis
=========================================================
Source: Ville de Montréal Open Data Portal (donnees.montreal.ca)
Data:   requetes311.csv (2022 to present, ~973k rows)

What this script does:
  1. Loads the raw 311 data
  2. Cleans and transforms it (dates, nulls, encoding, channel column)
  3. Runs 5 analyses and prints findings
  4. Exports a clean CSV for use in Power BI or Tableau
  5. Saves 4 matplotlib charts to /output/

Usage:
  pip install pandas matplotlib seaborn
  python montreal_311_analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

#  Config
INPUT_FILE  = "requetes311.csv"   
OUTPUT_DIR  = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Consistent plot style
sns.set_theme(style="whitegrid", palette="Blues_d")
plt.rcParams.update({"figure.dpi": 150, "font.family": "sans-serif"})

# 1. LOAD 
print("Loading data…")
df = pd.read_csv(
    INPUT_FILE,
    encoding="utf-8-sig",
    low_memory=False,
    dtype=str,   # load everything as string first — avoids mixed-type warnings
)
print(f"  Raw shape: {df.shape[0]:,} rows × {df.shape[1]} columns")


# 2. CLEAN
print("\nCleaning…")

# 2a. Strip whitespace from all string columns
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

# 2b. Parse dates
for col in ["DDS_DATE_CREATION", "DATE_DERNIER_STATUT"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# 2c. Extract useful date parts from creation date
df["year"]  = df["DDS_DATE_CREATION"].dt.year.astype("Int64")
df["month"] = df["DDS_DATE_CREATION"].dt.month.astype("Int64")
df["month_label"] = df["DDS_DATE_CREATION"].dt.to_period("M").astype(str)

# 2d. Collapse 9 binary PROVENANCE columns into one clean channel column
provenance_map = {
    "PROVENANCE_TELEPHONE":     "Téléphone",
    "PROVENANCE_COURRIEL":      "Courriel",
    "PROVENANCE_PERSONNE":      "En personne",
    "PROVENANCE_COURRIER":      "Courrier",
    "PROVENANCE_TELECOPIEUR":   "Télécopieur",
    "PROVENANCE_INSTANCE":      "Instance",
    "PROVENANCE_MOBILE":        "Mobile",
    "PROVENANCE_MEDIASOCIAUX":  "Médias sociaux",
    "PROVENANCE_SITEINTERNET":  "Site internet",
}

def get_channel(row):
    for col, label in provenance_map.items():
        if row.get(col) == "1":
            return label
    return "Inconnu"

print("  Mapping provenance columns to single channel column…")
df["channel"] = df.apply(get_channel, axis=1)

# 2e. Drop rows with no arrondissement AND no nature (essentially empty rows)
before = len(df)
df = df.dropna(subset=["NATURE"])
print(f"  Dropped {before - len(df):,} rows with no NATURE value")

# 2f. Normalize ARRONDISSEMENT — fill blanks with "Non précisé"
df["ARRONDISSEMENT"] = df["ARRONDISSEMENT"].fillna("Non précisé").str.strip()
df.loc[df["ARRONDISSEMENT"] == "", "ARRONDISSEMENT"] = "Non précisé"

# 2g. Convert coordinates to numeric
df["LOC_LAT"]  = pd.to_numeric(df["LOC_LAT"],  errors="coerce")
df["LOC_LONG"] = pd.to_numeric(df["LOC_LONG"], errors="coerce")

print(f"  Clean shape: {df.shape[0]:,} rows × {df.shape[1]} columns")


# 3. ANALYSIS 
print("\n── Analysis ──────────────────────────────────────────────────────────")

# 3a. Request type breakdown
print("\n[1] Request type breakdown (NATURE):")
nature_counts = df["NATURE"].value_counts()
print(nature_counts.to_string())

# 3b. Top 15 arrondissements by volume
print("\n[2] Top 15 arrondissements by request volume:")
arr_counts = (
    df[df["ARRONDISSEMENT"] != "Non précisé"]["ARRONDISSEMENT"]
    .value_counts()
    .head(15)
)
print(arr_counts.to_string())

# 3c. Volume by year
print("\n[3] Requests per year:")
yearly = df.groupby("year").size().reset_index(name="count")
print(yearly.to_string(index=False))

# 3d. Top 15 request topics (ACTI_NOM)
print("\n[4] Top 15 request topics (ACTI_NOM):")
topic_counts = df["ACTI_NOM"].value_counts().head(15)
print(topic_counts.to_string())

# 3e. Channel breakdown
print("\n[5] Submission channel breakdown:")
channel_counts = df["channel"].value_counts()
print(channel_counts.to_string())


# 4. CHARTS 
print("\n── Generating charts ─────────────────────────────────────────────────")

# Chart 1 — Requests by arrondissement (top 15)
fig, ax = plt.subplots(figsize=(10, 7))
arr_plot = arr_counts.sort_values()
arr_plot.plot(kind="barh", ax=ax, color="#2b6cb0")
ax.set_title("311 Requests by Borough — Top 15 (2022–2025)", fontsize=13, fontweight="bold")
ax.set_xlabel("Number of Requests")
ax.set_ylabel("")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_requests_by_borough.png")
plt.close()
print("  Saved: 01_requests_by_borough.png")

# Chart 2 — Monthly request volume (line chart)
monthly = df.groupby("month_label").size().reset_index(name="count")
monthly = monthly.sort_values("month_label")

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(monthly["month_label"], monthly["count"], color="#2b6cb0", linewidth=2)
ax.fill_between(monthly["month_label"], monthly["count"], alpha=0.15, color="#2b6cb0")
ax.set_title("Monthly 311 Request Volume (2022–2025)", fontsize=13, fontweight="bold")
ax.set_xlabel("")
ax.set_ylabel("Number of Requests")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
# Only show every 6th label so x-axis isn't crowded
tick_positions = range(0, len(monthly), 6)
ax.set_xticks([monthly["month_label"].iloc[i] for i in tick_positions if i < len(monthly)])
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_monthly_volume.png")
plt.close()
print("  Saved: 02_monthly_volume.png")

# Chart 3 — Request type breakdown (pie chart)
fig, ax = plt.subplots(figsize=(8, 8))
colors = ["#2b6cb0", "#4299e1", "#90cdf4", "#bee3f8"]

labels = nature_counts.index.tolist()
sizes  = nature_counts.values.tolist()

# Pull small slices outward so their labels don't collide
explode = [0.05 if s / sum(sizes) < 0.05 else 0 for s in sizes]

wedges, texts, autotexts = ax.pie(
    sizes,
    labels=None,          # we'll add labels via legend instead
    autopct="%1.1f%%",
    colors=colors[:len(sizes)],
    startangle=90,
    explode=explode,
    pctdistance=0.75,     # push % labels inward so they sit inside each slice
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
)

# Make percentage text white on dark slices, dark on light slices
for i, at in enumerate(autotexts):
    at.set_fontsize(11)
    at.set_fontweight("bold")
    at.set_color("white" if i < 2 else "#2d3748")

# Use a legend instead of labels directly on the chart — avoids all overlap
ax.legend(
    wedges, labels,
    title="Type",
    loc="lower center",
    bbox_to_anchor=(0.5, -0.08),
    ncol=2,
    fontsize=10,
)

ax.set_title("311 Request Types", fontsize=13, fontweight="bold", pad=20)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_request_types.png", bbox_inches="tight")
plt.close()
print("  Saved: 03_request_types.png")

# Chart 4 — Submission channel breakdown (horizontal bar)
fig, ax = plt.subplots(figsize=(9, 5))
channel_plot = channel_counts.sort_values()
channel_plot.plot(kind="barh", ax=ax, color="#2b6cb0")
ax.set_title("How Residents Submit 311 Requests", fontsize=13, fontweight="bold")
ax.set_xlabel("Number of Requests")
ax.set_ylabel("")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_submission_channels.png")
plt.close()
print("  Saved: 04_submission_channels.png")


# Chart 5 — Request type by arrondissement
top_arr = (
    df[df["ARRONDISSEMENT"] != "Non précisé"]["ARRONDISSEMENT"]
    .value_counts()
    .head(15)
    .index
)

arr_nature = (
    df[df["ARRONDISSEMENT"].isin(top_arr)]
    .groupby(["ARRONDISSEMENT", "NATURE"])
    .size()
    .unstack(fill_value=0)
)

# Sort by total volume
arr_nature = arr_nature.loc[arr_nature.sum(axis=1).sort_values().index]

fig, ax = plt.subplots(figsize=(11, 7))
arr_nature.plot(kind="barh", stacked=True, ax=ax, colormap="Blues")
ax.set_title("Request Types by Borough — Top 15 (2022–2025)", fontsize=13, fontweight="bold")
ax.set_xlabel("Number of Requests")
ax.set_ylabel("")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.legend(title="Request Type", bbox_to_anchor=(1.01, 1), loc="upper left")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_types_by_borough.png", bbox_inches="tight")
plt.close()
print("  Saved: 05_types_by_borough.png")


# 5. EXPORT CLEAN CSV 
print("\n── Exporting clean CSV ───────────────────────────────────────────────")

clean_cols = [
    "ID_UNIQUE", "NATURE", "ACTI_NOM",
    "ARRONDISSEMENT", "ARRONDISSEMENT_GEO",
    "DDS_DATE_CREATION", "DATE_DERNIER_STATUT",
    "year", "month", "month_label",
    "channel",
    "DERNIER_STATUT",
    "LOC_LAT", "LOC_LONG",
]

# Only keep columns that actually exist in the dataframe
clean_cols = [c for c in clean_cols if c in df.columns]
df_clean = df[clean_cols].copy()

out_path = f"{OUTPUT_DIR}/montreal_311_clean.csv"
df_clean.to_csv(out_path, index=False, encoding="utf-8-sig")
print(f"  Saved: {out_path}")
print(f"  Shape: {df_clean.shape[0]:,} rows × {df_clean.shape[1]} columns")

print("\nDone.")