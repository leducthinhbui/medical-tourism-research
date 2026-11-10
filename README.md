# Medical Travel to Vietnam: Sizing the Vietnamese-Australian Market

A market study of medical travel from Australia to Vietnam, focused on Vietnamese-Australians who already travel home to visit family. Built from public data only: ABS Census figures, ABS overseas travel figures, published procedure prices and industry reports.

**Read the findings:** https://leducthinhbui.github.io/medical-tourism-research/ (also as `Medical_Tourism_Findings.pdf`)

## Key findings

- **Market:** 257,997 Australians were born in Vietnam and 334,785 report Vietnamese ancestry (ABS Census 2021). 57% of those born in Vietnam are aged 45 or over, with a median age of 48 against 38 for all Australians.
- **Travel:** trips by Australian residents to Vietnam rose 46% in two years, from 388,580 in 2023–24 to 567,480 in 2025–26.
- **Price:** common procedures cost far less in Vietnam than in Australia, about 81% less for dental work and 77% to 80% less for facelifts and rhinoplasty, at the midpoint of typical price ranges. Thailand is cheaper for breast augmentation and at the low end of dental prices.
- **Competition:** Thailand treats about ten times as many foreign patients and has 61 JCI-accredited hospitals, but Vietnam's medical tourism market is growing faster (17.8% a year to 2033, against 10.5% for Thailand to 2030).
- **Recommendation:** target Vietnamese-Australians aged 45 and over with packages that combine a family visit with booked health checks or dental care at accredited hospitals such as Vinmec or FV, with fixed prices and follow-up support.

## Files

| Path | What it holds |
|---|---|
| `index.html` | The findings report as a web page (served by GitHub Pages) |
| `Medical_Tourism_Findings.pdf` | The same report as a PDF |
| `data/abs_vietnam_born_age_2021.csv` | Australians born in Vietnam by age group (ABS Census 2021) |
| `data/abs_vietnam_born_summary_2021.csv` | Population, ancestry, median age and sex split, with links to the ABS source |
| `data/trips_to_vietnam.csv` | Trips by Australian residents to Vietnam by financial year |
| `data/procedure_prices_aud.csv` | Typical price ranges for five procedures in Vietnam, Thailand and Australia (A$) |
| `data/vietnam_vs_thailand.csv` | Patient numbers, market size, growth and accreditation, with sources |
| `scripts/make_report.py` | Builds the report and charts from the data files |

## Method and limits

- **Population and age:** taken directly from the ABS Census 2021 QuickStats for people born in Vietnam.
- **Trips:** ABS Overseas Arrivals and Departures figures as reported by KarryOn. I did not access the ABS release tables directly.
- **Prices:** indicative ranges compiled from published clinic and medical-tourism price guides in 2025, not quotes. Savings use the midpoint of each range.
- **Market size and accreditation:** from the industry reports named in `data/vietnam_vs_thailand.csv`.
- **What is not included:** the study grew out of my internship at Vietravel Australia (July to October 2025), which also included a survey of 53 Vietnamese-Australians. Those responses are not published, to protect the respondents' privacy, and no Vietravel customer, pricing or partner information is included.

## Rebuild

```bash
python scripts/make_report.py data index.html
```

Requires Python 3 with pandas and matplotlib.
