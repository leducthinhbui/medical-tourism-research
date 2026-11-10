"""Build index.html (charts embedded) for the medical tourism study from the CSVs in data/.

    python scripts/make_report.py data index.html
Then print index.html to PDF (Chrome: --headless --print-to-pdf).
"""
import base64
import io
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA, OUT = sys.argv[1], sys.argv[2]
VN, TH, AU, MUTED, INK = "#b5452d", "#d9a441", "#4b6c8f", "#c9c4bd", "#2b2522"
plt.rcParams.update({"font.family": "Arial", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#999999", "axes.titleweight": "bold", "axes.titlesize": 10,
                     "axes.titlelocation": "left", "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK})


def png(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


age = pd.read_csv(f"{DATA}/abs_vietnam_born_age_2021.csv")
summ = pd.read_csv(f"{DATA}/abs_vietnam_born_summary_2021.csv").set_index("measure")
trips = pd.read_csv(f"{DATA}/trips_to_vietnam.csv")
prices = pd.read_csv(f"{DATA}/procedure_prices_aud.csv")
bench = pd.read_csv(f"{DATA}/vietnam_vs_thailand.csv")

born = int(summ.loc["People born in Vietnam", "value"])
ancestry = int(summ.loc["People with Vietnamese ancestry", "value"])
median_age = int(summ.loc["Median age, born in Vietnam", "value"])
female = summ.loc["Female share, born in Vietnam (%)", "value"]
older = age[age.age_group.isin(["45-54", "55-64", "65+"])].people.sum()
older_pct = older / born * 100
growth = (trips.short_term_resident_returns.iloc[-1] / trips.short_term_resident_returns.iloc[0] - 1) * 100
for c in ("vietnam", "thailand", "australia"):
    prices[f"{c}_mid"] = (prices[f"{c}_low"] + prices[f"{c}_high"]) / 2
prices["saving_vs_au"] = (1 - prices.vietnam_mid / prices.australia_mid) * 100
dental = prices.set_index("procedure").loc["Dental work"]

# Chart 1: Vietnam-born residents by age
fig, ax = plt.subplots(figsize=(3.6, 2.4))
ax.bar(age.age_group, age.people / 1000, color=[VN if g in ("45-54", "55-64", "65+") else MUTED for g in age.age_group], width=0.65)
ax.set_title("Australians born in Vietnam, by age (thousands)")
ax.yaxis.grid(True, color="#eeeeee"); ax.set_axisbelow(True)
c1 = png(fig)

# Chart 2: trips to Vietnam
fig, ax = plt.subplots(figsize=(3.6, 2.4))
ax.bar(trips.financial_year, trips.short_term_resident_returns / 1000, color=VN, width=0.55)
for i, v in enumerate(trips.short_term_resident_returns):
    ax.text(i, v / 1000 + 8, f"{v / 1000:,.0f}k", ha="center", fontsize=8)
ax.set_ylim(0, trips.short_term_resident_returns.max() / 1000 * 1.18)
ax.set_title("Trips by Australian residents to Vietnam")
ax.yaxis.grid(True, color="#eeeeee"); ax.set_axisbelow(True)
c2 = png(fig)

# Chart 3: price ranges by procedure and country
fig, ax = plt.subplots(figsize=(7.4, 2.8))
order = prices.sort_values("australia_mid").reset_index(drop=True)
for i, r in order.iterrows():
    for j, (c, col, lab) in enumerate([("vietnam", VN, "Vietnam"), ("thailand", TH, "Thailand"), ("australia", AU, "Australia")]):
        y = i + (j - 1) * 0.22
        ax.plot([r[f"{c}_low"], r[f"{c}_high"]], [y, y], color=col, lw=5, solid_capstyle="butt", label=lab if i == 0 else None)
ax.set_yticks(range(len(order))); ax.set_yticklabels(order.procedure)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"${v / 1000:.0f}k"))
ax.xaxis.grid(True, color="#eeeeee"); ax.set_axisbelow(True)
ax.legend(frameon=False, loc="lower right", ncol=3)
ax.set_title("Typical price range for each procedure, A$")
c3 = png(fig)

rows = "".join(f"<tr><td>{r.measure}</td><td>{r.vietnam}</td><td>{r.thailand}</td></tr>" for r in bench.itertuples())
srows = "".join(f"<tr><td>{r.procedure}</td><td>{r.saving_vs_au:.0f}%</td></tr>" for r in prices.sort_values("saving_vs_au", ascending=False).itertuples())

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Medical Travel to Vietnam</title>
<style>
@page {{ size: A4; margin: 14mm 15mm 12mm; }}
body {{ font-family: Arial, sans-serif; font-size: 9.8pt; line-height: 1.45; color: #2b2522; margin: 0 auto; max-width: 780px; padding: 0 16px; }}
h1 {{ font-size: 19pt; margin: 14px 0 2pt; color: #6e2a1b; }}
.by {{ color: #6b625c; font-size: 9pt; margin-bottom: 8pt; }}
h2 {{ font-size: 11.5pt; color: #6e2a1b; margin: 12pt 0 4pt; border-bottom: 1px solid #e3d9d2; padding-bottom: 2pt; }}
p {{ margin: 0 0 6pt; }}
ul {{ margin: 0 0 6pt; padding-left: 16pt; }} li {{ margin-bottom: 3pt; }}
.pair {{ display: flex; flex-wrap: wrap; gap: 10pt; margin: 4pt 0 6pt; }} .pair img {{ width: calc(50% - 5pt); min-width: 260px; flex: 1; }}
img.wide {{ width: 100%; margin: 4pt 0 6pt; }}
.box {{ background: #f8f3ef; border-left: 3px solid #b5452d; padding: 7pt 10pt; margin: 6pt 0; }}
table {{ break-inside: avoid; width: 100%; border-collapse: collapse; font-size: 9pt; margin: 4pt 0 8pt; }}
th {{ text-align: left; background: #f8f3ef; padding: 4pt 6pt; border-bottom: 1px solid #e3d9d2; }}
td {{ padding: 4pt 6pt; border-bottom: 1px solid #efe8e3; vertical-align: top; }}
.small {{ font-size: 8pt; color: #6b625c; }}
.pb {{ break-before: page; }}
</style></head><body>
<h1>Medical Travel to Vietnam: Sizing the Vietnamese-Australian Market</h1>
<div class="by">Daniel Bui &middot; Research completed in 2025, public version November 2026 &middot; Public data only</div>
<div class="box">There are <b>{born:,}</b> Australians born in Vietnam and <b>{ancestry:,}</b> with Vietnamese ancestry (ABS Census 2021).
<b>{older_pct:.0f}%</b> of those born in Vietnam are aged 45 or over, and trips by Australian residents to Vietnam grew
<b>{growth:.0f}%</b> in two years. Common procedures cost far less in Vietnam than in Australia (about <b>{dental.saving_vs_au:.0f}%</b> less for dental work),
which makes a combined family-visit and health-care trip a realistic product for this group.</div>

<h2>Who the customers are</h2>
<div class="pair"><img src="{c1}" alt="Vietnam-born Australians by age"><img src="{c2}" alt="Trips by Australian residents to Vietnam"></div>
<ul>
<li><b>An older, established community.</b> The median age of Vietnam-born Australians is {median_age}, against 38 for all Australians, and
{female:.0f}% are women. {older:,} people, {older_pct:.0f}% of the group, are 45 or older: the ages when health checks, dental work and
specialist care become regular needs.</li>
<li><b>They already travel to Vietnam.</b> Australian residents made {trips.short_term_resident_returns.iloc[-1]:,} trips to Vietnam in
{trips.financial_year.iloc[-1]}, up from {trips.short_term_resident_returns.iloc[0]:,} in {trips.financial_year.iloc[0]}. Many are visits to family,
so health care can be added to a trip people take anyway.</li>
<li><b>Australians already go abroad for treatment.</b> An estimated 15,000 Australians a year travel overseas for procedures such as
dental implants and cosmetic surgery, and dental care is the most common reason.</li>
</ul>

<h2>Price: why Vietnam is attractive</h2>
<img class="wide" src="{c3}" alt="Price ranges by procedure in Vietnam, Thailand and Australia">
<div class="pair" style="align-items:flex-start;break-inside:avoid">
<div style="flex:1;min-width:260px"><table><tr><th>Procedure</th><th>Vietnam saving vs Australia (midpoints)</th></tr>{srows}</table></div>
<div style="flex:1;min-width:260px"><p>Vietnam is far cheaper than Australia for every procedure compared, and close to Thailand. Thailand is cheaper
for breast augmentation and at the low end of dental prices, so price alone does not win against Thailand: service, trust and the family connection have to.</p></div>
</div>

<h2>Vietnam against Thailand</h2>
<table><tr><th>Measure</th><th>Vietnam</th><th>Thailand</th></tr>{rows}</table>
<p>Thailand is the established destination for Australian patients, with ten times the foreign patients and many more internationally
accredited hospitals. Vietnam's market is smaller but growing faster, and Vietnamese-Australians bring something Thailand cannot offer:
family in Vietnam and a language they share with doctors and staff.</p>

<h2>Recommendation</h2>
<ul>
<li><b>Target customer:</b> Vietnamese-Australians aged 45 and over who already visit family in Vietnam.</li>
<li><b>Product:</b> a package that combines a family visit with booked health checks or dental care at internationally accredited
hospitals, such as Vinmec or FV, with flexible dates and Vietnamese-speaking support.</li>
<li><b>What has to be true:</b> clear, fixed prices before travel, accredited hospitals, and help with follow-up care after the customer
returns to Australia. These are the points where Thailand currently leads.</li>
</ul>

<h2>Method and limits</h2>
<p class="small">Population and age figures come directly from the ABS Census 2021 QuickStats for people born in Vietnam. Trip numbers are ABS
Overseas Arrivals and Departures figures as reported by KarryOn; I did not access the ABS release tables directly. Price ranges are
indicative ranges compiled from published clinic and medical-tourism price guides in 2025, not quotes. Market size and accreditation figures
come from the industry reports named in the table. This public version uses public information only. The study grew out of my internship
at Vietravel Australia (July to October 2025), which also included a survey of 53 Vietnamese-Australians; those responses are not
published, to protect the respondents' privacy, and no Vietravel customer, pricing or partner information is included. Full data:
github.com/leducthinhbui/medical-tourism-research.</p>
</body></html>"""
open(OUT, "w").write(html)
print("wrote", OUT, f"older={older} ({older_pct:.1f}%) growth={growth:.1f}% dental_saving={dental.saving_vs_au:.1f}%")
