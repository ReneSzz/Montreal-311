# Montreal 311 Service Request Analysis

A Python data cleaning and analysis pipeline for 973,000 city service requests submitted to Montreal's 311 system between 2022 and 2025, using open data published by the Ville de Montréal.


Dataset


Source: Ville de Montréal Open Data Portal
Licence: Creative Commons 4.0 Attribution (CC-BY) — Québec
Coverage: 2022 – April 2026
Raw records: ~973,000 service requests
Fields: Request type, topic, borough, submission date, submission channel (phone/web/mobile/etc.), status, coordinates



Note: The raw CSV (requetes311.csv) is ~200MB and not included in this repo. Download it directly from the link above and place it in the same folder as the script before running.




## What the Script Does

1. Loads safely

Reads all 973k rows with dtype=str to avoid type inference errors on messy data, then applies explicit type conversions.

2. Cleans


Strips whitespace from all columns to prevent silent GROUP BY mismatches
Parses two date columns (DDS_DATE_CREATION, DATE_DERNIER_STATUT) with errors="coerce" to handle malformed values gracefully
Extracts year, month, and month_label features from raw timestamps for trend analysis
Collapses 9 binary PROVENANCE_* columns into a single channel field (Téléphone, Mobile, Site internet, etc.)
Drops rows with no NATURE value (unclassifiable records)
Fills missing ARRONDISSEMENT values with "Non précisé" rather than dropping rows, preserving total counts


3. Analyzes

Five analyses printed to terminal:


Request type breakdown (Requête, Information, Plainte, Commentaire)
Top 15 boroughs by volume
Annual request volume (2022–2025)
Top 15 request topics (ACTI_NOM)
Submission channel breakdown


4. Generates 4 charts

Saved to /output/:


01_requests_by_borough.png — horizontal bar, top 15 boroughs
02_monthly_volume.png — line chart with area fill, monthly trend
03_request_types.png — pie chart by request type
04_submission_channels.png — horizontal bar by submission channel


5. Exports clean CSV

Reduces the raw 29-column file to 13 analysis-ready columns, saved to output/montreal_311_clean.csv.


A 1,000-row sample is included in this repo at output/montreal_311_sample.csv for reference.




## Key Findings

1. Phone dominates submissions at 75.6% — digital channels combined account for only 11.1%.
Of 3,034,731 total submissions, 2,295,671 (75.6%) came in by phone. Mobile, web, and email combined account for just 11.1% (336,259 requests). A further 7.8% (237,006) have no channel recorded, suggesting gaps in data capture for older records. Despite the availability of digital alternatives, the 311 system remains overwhelmingly phone-driven.
<details>
<img width="1350" height="750" alt="04_submission_channels" src="https://github.com/user-attachments/assets/0badb81a-fd55-4a6f-8baa-a2e9e08412df" />
</details>
3. Nearly all borough-level requests are Requêtes — complaints and comments are negligible.
Across every borough in the top 15, Requête (service requests) make up the overwhelming majority of volume. Plainte (complaints) and Commentaire are barely visible even at scale, confirming that residents use 311 primarily to request services, not to formally complain.
<details>
<img width="1622" height="1026" alt="05_types_by_borough" src="https://github.com/user-attachments/assets/1961be28-08d8-4858-b183-3afa20c5f432" />
</details>
5. Mercier–Hochelaga-Maisonneuve leads all boroughs with 162,204 requests.
The top 6 boroughs — Mercier–Hochelaga-Maisonneuve (162,204), Rosemont–La Petite-Patrie (139,199), Ahuntsic–Cartierville (135,281), Ville-Marie (134,482), Saint-Laurent (131,722), and Le Plateau-Mont-Royal (131,130) — are closely clustered, each handling between 131k and 162k requests over the period.
<details>
<img width="1500" height="1050" alt="01_requests_by_borough" src="https://github.com/user-attachments/assets/10dfdfac-f0b7-4591-b55f-51fb225adaef" />
</details>
7. Annual volume is stable with a slight upward trend — 2025 was the busiest year on record.
Yearly volumes were consistent from 2022 (660,554) through 2024 (639,090), with 2025 seeing the highest volume at 696,479 — a 5.4% increase over 2022. The 2026 figure (398,677) reflects a partial year. Monthly volume shows a clear seasonal rhythm peaking in spring and summer, driven by outdoor service requests like pothole repairs and waste collection.
<details>
<img width="2100" height="750" alt="02_monthly_volume" src="https://github.com/user-attachments/assets/48c3c2f7-449c-4a0c-ae71-e828b55b160c" />
</details>
9. Requête and Information together account for 98.2% of all requests.
Requête makes up 52.3% (1,588,391) and Information 45.9% (1,391,644) of total volume. Plainte and Commentaire each represent just 0.9% — confirming that 311 functions as a service request and information line, not a complaints channel. The top request topics are Taxes foncières (188,884), Collecte de déchets (147,665), and Dépôt illégal (109,929).
<details>
<img width="1051" height="1183" alt="03_request_types" src="https://github.com/user-attachments/assets/17566171-87c4-44b3-8020-a36d43c44ee1" />
</details>

###Tools Used

Python 3 — core language
pandas — data loading, cleaning, transformation, aggregation
matplotlib — chart generation
seaborn — plot styling



