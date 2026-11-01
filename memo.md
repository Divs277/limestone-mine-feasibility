# Recommendation Memo: 1 Mtpa Open-Pit Limestone Mine

**Prepared by:** Diya Sharma, 2nd-year Mining Engineering
**Date:** November 2026
**Question:** Should an investor fund a small open-pit limestone mine producing about 1 million tonnes a year?

## 1. Recommendation

**Conditional go.** On my base-case assumptions the mine returns more than it costs (NPV about ₹16 crore at 12%, IRR about 15.7%), but the margin is thin. A fall of only about 7% in the limestone price makes the NPV negative. I would only invest if the buyer's price is secured through a long-term supply contract, or the royalty and costs are confirmed to be no worse than assumed here.

## 2. The project in brief

| Item | Assumption |
|---|---|
| Production | 1 Mtpa of limestone |
| Reserve and mine life | 15 Mt, so 15 years |
| Stripping ratio | 0.5 t waste per t ore |
| Selling price | ₹595 per tonne |
| Capital cost | ₹80 crore |
| Discount rate | 12% |
| Tax | 25% |

Moving ore and waste means about 5,000 tonnes a day. One 35 t truck can haul about 914 t a day, so the mine needs about **6 trucks**.

## 3. Base-case results

| Result | Value |
|---|---|
| Revenue per year | ₹59.5 crore |
| Operating cost per year (incl. royalty) | ₹42.4 crore |
| EBITDA per year | ₹17.1 crore |
| **NPV at 12%** | **₹16.4 crore** |
| **IRR** | **15.7%** |
| Payback | 5.7 years |

The project clears the 12% hurdle, but not by a wide margin: an IRR of 15.7% leaves only about 3.7 percentage points of cushion.

## 4. What could make it fail

I changed each input by 20% up and down and checked the effect on NPV (see `tornado.png`).

1. **Price is the biggest risk.** A 20% change moves NPV by about ₹49 crore, which is three times the base-case NPV. The break-even price is about ₹555 per tonne, only about 7% below the base case.
2. **Production volume.** A 20% shortfall cuts NPV by about ₹18 crore, because fixed costs and capital are spread over fewer tonnes.
3. **Capital cost and discount rate.** Each can move NPV by about ₹11 to ₹14 crore.
4. **Mining and processing costs** matter, but less than price. Stripping ratio had the smallest effect in this model (about ₹5 crore for a 20% change).

Royalty is also important. At about 20% of price it takes a large share of revenue. When I tested a 10% royalty instead, NPV rose to about ₹47 crore, so the royalty rate and local levies need to be checked carefully for any real site.

## 5. Conditions for a "go"

- A supply agreement fixing a price of at least about ₹600 per tonne, or a buyer that pays a premium for grade.
- Confirmation of the current royalty, DMF and NMET charges for the state.
- Proof that the deposit can sustain 1 Mtpa for 15 years (drilling data and a proper reserve estimate).
- A firm quote for the crusher and truck fleet to confirm the ₹80 crore capital figure.

I would say **no-go** if the achievable price is below about ₹555 per tonne, or if royalty and levies are higher than assumed.

## 6. About the data and limits of this study

- **Sourced:** the price (₹595/t, a 2023-24 average ex-mine price for limestone in Jaisalmer, Rajasthan) and royalty (about ₹120/t, around 20% of price) come from a single news article, and I have not yet confirmed them against Indian Bureau of Mines data or a company report.
- **Assumed by me:** capital cost, mining cost, processing cost, overhead, stripping ratio, reserve size, truck data and discount rate. I used a captive-mine cost-of-production figure of about ₹281/t from an Indian Bureau of Mines document as a rough cross-check, and my costs came to about ₹265/t.
- **Simplifications:** constant output and price over 15 years, no inflation, no working capital, straight-line depreciation, simplified tax, and no pit optimisation or block model.

This is a screening-level study done to learn the method. A real investment decision would need a site-specific resource estimate and quotations.

## 7. How the model works

The Python model (`src/model.py`) reads all inputs from `data/assumptions.csv`. It calculates annual revenue and cost, applies royalty and tax, discounts the cash flows to get NPV and IRR, sizes the truck fleet, and runs the sensitivity analysis shown in the charts.
