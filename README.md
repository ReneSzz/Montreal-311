# Montreal 311 Service Request Analysis

A Python data cleaning and analysis pipeline for 3,034,731 city service requests submitted to Montreal's 311 system between 2022 and 2026, using open data published by the Ville de Montréal.

![Requests by Borough](screenshots/01_requests_by_borough.png)

---

## Project Goals
- Practice real-world data cleaning on a large, messy civic dataset
- Demonstrate Python and pandas skills beyond basic tutorials
- Surface meaningful patterns in how Montreal residents interact with city services
- Export a clean, analysis-ready dataset for downstream BI use

---

## Dataset
- **Source:** [Ville de Montréal Open Data Portal](https://donnees.montreal.ca/dataset/requetes-service-311)
- **Licence:** Creative Commons 4.0 Attribution (CC-BY) — Québec
- **Coverage:** 2022 – 2026
- **Raw records:** 3,034,731 service requests
- **Fields:** Request type, topic, borough, submission date, submission channel (phone/web/mobile/etc.), status, coordinates

> **Note:** The raw CSV (`requetes311.csv`) is ~200MB and not included in this repo. Download it directly from the link above and place it in the same folder as the script before running.

---

## What the Script Does

### 1. Loads safely
Reads all rows with `dtype=str` to avoid type inference errors on messy data, then applies explicit type conversions.

### 2. Cleans
- Strips whitespace from all columns to prevent silent grouping mismatches
- Parses two date columns (`DDS_DATE_CREATION`, `DATE_DERNIER_STATUT`) with `errors="coerce"` to handle malformed values gracefully
- Extracts `year`, `month`, and `month_label` features from raw timestamps for trend analysis
- Collapses 9 binary `PROVENANCE_*` columns into a single `channel` field (Téléphone, Mobile, Site internet, etc.)
- Drops rows with no `NATURE` value (unclassifiable records)
- Fills missing `ARRONDISSEMENT` values with `"Non précisé"` rather than dropping rows, preserving total counts

### 3. Analyzes
Five analyses printed to terminal:
1. Request type breakdown (Requête, Information, Plainte, Commentaire)
2. Top 15 boroughs by volume
3. Annual request volume
4. Top 15 request topics (`ACTI_NOM`)
5. Submission channel breakdown

### 4. Generates 5 charts
Saved to `/screenshots/`:
- `01_requests_by_borough.png` — horizontal bar, top 15 boroughs by total volume
- `02_monthly_volume.png` — line chart with area fill, monthly trend 2022–2026
- `03_request_types.png` — pie chart by request type
- `04_submission_channels.png` — horizontal bar by submission channel
- `05_types_by_borough.png` — stacked bar showing request type breakdown per borough

### 5. Exports clean CSV
Reduces the raw 29-column file to 13 analysis-ready columns, saved to `output/montreal_311_clean.csv`.

> A 1,000-row sample is included in this repo at `output/montreal_311_sample.csv` for reference.

---

## Key Findings

**1. Phone dominates submissions at 75.6% — digital channels combined account for only 11.1%.**
Of 3,034,731 total submissions, 2,295,671 (75.6%) came in by phone. Mobile, web, and email combined account for just 11.1% (336,259 requests). A further 7.8% (237,006) have no channel recorded, suggesting gaps in data capture for older records. Despite the availability of digital alternatives, the 311 system remains overwhelmingly phone-driven.

![Submission Channels](screenshots/04_submission_channels.png)

**2. Nearly all borough-level requests are Requêtes — complaints and comments are negligible.**
Across every borough in the top 15, Requête (service requests) make up the overwhelming majority of volume. Plainte (complaints) and Commentaire are barely visible even at scale, confirming that residents use 311 primarily to request services, not to formally complain.

![Request Types by Borough](screenshots/05_types_by_borough.png)

**3. Mercier–Hochelaga-Maisonneuve leads all boroughs with 162,204 requests.**
The top 6 boroughs — Mercier–Hochelaga-Maisonneuve (162,204), Rosemont–La Petite-Patrie (139,199), Ahuntsic–Cartierville (135,281), Ville-Marie (134,482), Saint-Laurent (131,722), and Le Plateau-Mont-Royal (131,130) — are closely clustered, each handling between 131k and 162k requests over the period.

![Requests by Borough](screenshots/01_requests_by_borough.png)

**4. Annual volume is stable with a slight upward trend — 2025 was the busiest year on record.**
Yearly volumes were consistent from 2022 (660,554) through 2024 (639,090), with 2025 seeing the highest volume at 696,479 — a 5.4% increase over 2022. The 2026 figure (398,677) reflects a partial year. Monthly volume shows a clear seasonal rhythm peaking in spring and summer, driven by outdoor service requests like pothole repairs and waste collection.

![Monthly Volume](screenshots/02_monthly_volume.png)

**5. Requête and Information together account for 98.2% of all requests.**
Requête makes up 52.3% (1,588,391) and Information 45.9% (1,391,644) of total volume. Plainte and Commentaire each represent just 0.9% — confirming that 311 functions as a service request and information line, not a complaints channel. The top request topics are Taxes foncières (188,884), Collecte de déchets (147,665), and Dépôt illégal (109,929).

![Request Types](screenshots/03_request_types.png)

---

## Tools Used
- **Python 3** — core language
- **pandas** — data loading, cleaning, transformation, aggregation
- **matplotlib** — chart generation
- **seaborn** — plot styling

---

## How to Run

```bash
# 1. Install dependencies
pip install pandas matplotlib seaborn

# 2. Download the raw data from donnees.montreal.ca and place it here:
#    requetes311.csv  ← same folder as the script

# 3. Run
python montreal_311_analysis.py

# Output will be saved to /screenshots/ and /output/
```

---

## Repository Structure

```
montreal-311-analysis/
│
├── README.md
├── montreal_311_analysis.py
├── output/
│   └── montreal_311_sample.csv        ← 1,000-row sample of cleaned data
└── screenshots/
    ├── 01_requests_by_borough.png
    ├── 02_monthly_volume.png
    ├── 03_request_types.png
    ├── 04_submission_channels.png
    └── 05_types_by_borough.png
```
