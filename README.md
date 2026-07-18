Montreal 311 Service Request Analysis

A Python data cleaning and analysis pipeline for 973,000 city service requests submitted to Montreal's 311 system between 2022 and 2025, using open data published by the Ville de Montréal.



## Number of requests by burough 
<img width="1500" height="1050" alt="01_requests_by_borough" src="https://github.com/user-attachments/assets/59905941-37a2-42eb-8fb5-c0412468e7b0" />

## Monthly Volume
<img width="2100" height="750" alt="02_monthly_volume" src="https://github.com/user-attachments/assets/00e4f206-3075-4077-bc93-023cae5a43a3" />

## Type of request by burough
<img width="1622" height="1026" alt="05_types_by_borough" src="https://github.com/user-attachments/assets/b0d02723-eefb-4044-8062-012d7de6bbc4" />

## Submission Channels 
<img width="1350" height="750" alt="04_submission_channels" src="https://github.com/user-attachments/assets/5a9af164-ca76-45aa-977d-51864bc492f6" />

## Request Types
<img width="1051" height="1183" alt="03_request_types" src="https://github.com/user-attachments/assets/44fc359f-729e-4f42-9331-91cab08766ad" />

Dataset


Source: Ville de Montréal Open Data Portal
Licence: Creative Commons 4.0 Attribution (CC-BY) — Québec
Coverage: 2022 – April 2026
Raw records: ~973,000 service requests
Fields: Request type, topic, borough, submission date, submission channel (phone/web/mobile/etc.), status, coordinates



Note: The raw CSV (requetes311.csv) is ~200MB and not included in this repo. Download it directly from the link above and place it in the same folder as the script before running.




What the Script Does

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




Key Findings

1. Phone calls still dominate despite digital options.
Over 52% of all 311 requests come in by phone, even though residents can submit via mobile app, website, email, and in person. Digital channels have not meaningfully displaced phone as the primary contact method.

2. Requête and Information together account for 98%+ of volume.
Complaints (Plainte) and Comments (Commentaire) are rare — the vast majority of residents are either requesting a service or asking for information, not formally complaining.

3. Plateau-Mont-Royal, Côte-des-Neiges–NDG, and Rosemont–La Petite-Patrie are consistently the highest-volume boroughs.
These three central boroughs account for a disproportionate share of requests relative to their population, suggesting either higher civic engagement or higher service demand.

4. Request volume shows clear seasonal patterns.
Monthly volume peaks in spring and summer months (April–August), likely driven by outdoor service requests such as pothole repairs, park maintenance, and street cleaning.


Tools Used


Python 3 — core language
pandas — data loading, cleaning, transformation, aggregation
matplotlib — chart generation
seaborn — plot styling



