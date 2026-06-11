# BotLease.nl — Business Model & Pricing Audit

*Prepared May 2026. Author: research agent for Thomas Vedder. Scope: 15-model humanoid lease catalogue, Dutch market, 12-month break-even goal.*

---

## 1. Executive summary

**Can BotLease realistically break even within 12 months? No — not at the current price points and not as a solo operation that has to finance robot acquisition itself.** The maths is unforgiving: even at a healthy 35–40 % gross lease margin, a 36-month lease only returns ~3 % of unit acquisition cost *per month*. To cover a €5k/mo founder salary plus baseline fixed costs (~€8–10k/mo all-in), you need roughly **€100k–€120k of gross profit in year 1**, which translates to **15–25 active contracts running for an average of 6+ months by month 12** — while having paid out €600k–€1.5M of robot capex up front. That capex is the killer.

**What IS realistic:** 18–24 months to operational break-even *if* BotLease shifts from "we own the fleet" to a **broker / pass-through-lease** model where DLL, De Lage Landen, or the manufacturer (NEURA, UR/DLL, Unitree distributor) carries the asset. In that mode, BotLease earns 8–15 % origination + a service-margin recurring fee, and capex risk evaporates. 12-month break-even becomes plausible at ~12 signed contracts.

**Top 3 actions this quarter:**
1. **Negotiate a back-to-back lease facility with DLL Netherlands** (already partners UR; they finance industrial equipment). Stop being the balance sheet. BotLease becomes the service/SLA layer + originator.
2. **Reprice aggressively**: 7 of 15 current monthly rates are *underwater* once realistic EU-landed cost, swap-SLA cost, and insurance are properly modelled (see §6). The Unitree R1 at €290/mo is the most extreme — it's a marketing loss-leader, fine, but flag it as such.
3. **Drop or "made-to-order only" the 4 US waitlist models (Apollo, Figure, Digit, NEO)** as bookable inventory. Keep them as reservation-deposit funnel pages. None of these vendors will sell BotLease a unit in 2026 at any reasonable price; the listed lease numbers are aspirational, not financeable.

---

## 2. Real EU acquisition prices per model

EU duty on industrial robots (HS 8479.50) is **0 %** ([EU TARIC](https://taxation-customs.ec.europa.eu/customs/calculation-customs-duties/customs-tariff_en)). The cost driver for non-EU units is **NL import VAT 21 %** (reclaimable for a B2B lessor but blocks working capital for 1–3 months), **freight + customs broker** (~€800–€2,500 per unit air/sea), and **distributor margin** (15–30 % when buying via RobotShop EU, MyBotShop, QUADRUPED.DE, INFUZE Hungary, or directly).

| Model | Vendor list price | EU landed cost est. (excl. VAT) | Notes & sources |
|---|---|---|---|
| **NEURA 4NE-1 Mini** | €19,999 Std / €29,999 Pro | **€20–24k** | German build, no import surcharge. Refundable €100 reservation. ([NEURA](https://neura-robotics.com/product/4ne1-mini-reservation/), [RoboHorizon](https://robohorizon.com/en-us/news/2026/01/neura-robotics-opens-preorders-for-98k-porsche-designed-humanoid/)) |
| **NEURA 4NE-1 Gen 3.5** | €98k (1–19 units) / €60k (20+ fleet) | **€85–98k** | "Purchase only — no RaaS" per vendor. BotLease must absorb full capex. ([NEURA](https://neura-robotics.com/product/4ne1-reservation/)) |
| **PAL Kangaroo** | Quote-only, est. **€80–110k** | **€85–105k** | EU-built (ES). Recently went on sale. ([PAL](https://pal-robotics.com/robot/kangaroo/), [Humanoid Robotics Tech](https://humanoidroboticstechnology.com/humanoid-technology/pal-robotics-kangaroo-robot-goes-on-sale/)) |
| **PAL TIAGo Pro** | Quote-only, est. **€55–75k** | **€55–75k** | EU-built (ES). 100+ EU deployments since 2014. ([PAL TIAGo Pro](https://pal-robotics.com/robot/tiago-pro/)) |
| **Pollen Reachy 2** | **$70,000** (~€64k) | **€65–72k** | Hugging Face-owned. EU-built (FR). ([deeplearning.ai](https://www.deeplearning.ai/the-batch/hugging-face-acquires-pollen-robotics-launches-reachy-2-robot-for-open-source-research/), [Ainvest](https://www.ainvest.com/news/hugging-face-acquires-pollen-robotics-expands-ai-portfolio-70-000-reachy-2-robot-2504/)) |
| **Unitree R1** | **$5,900** (~€5.4k) base; €4.9k CN | **€7–9k** landed | China list ≠ EU price. RobotShop / QUADRUPED markup ~50 %. ([Unitree](https://shop.unitree.com/), [QUADRUPED.DE](https://www.quadruped.de/Unitree-G1_1)) |
| **Unitree G1 Edu** | **$16,000–$73,900** (16 configs); **€23,000** at QUADRUPED.DE | **€20–28k** standard config | The €16k slug in the catalogue is the CN starting price. EU-landed Edu config is €20–25k typical. ([Botinfo G1](https://botinfo.ai/articles/unitree-g1), [QUADRUPED](https://www.quadruped.de/Unitree-G1_1)) |
| **Unitree H1-2** | $99,900–$128,900 USD | **€100–125k** landed | Plus shipping + VAT cashflow. ([Botinfo H1](https://botinfo.ai/articles/unitree-h1-humanoid), [RobotShop](https://eu.robotshop.com/products/unitree-h1-2-humanoid-robot-eu)) |
| **Unitree H2** | $29,900 base / $40,900 Commercial / $68,900 EDU | **€38–55k** for usable commercial config | The $29.9k is the CN domestic teaser. EU-spec H2 has different hardware. ([RoboHorizon H2](https://robohorizon.com/en-us/news/2025/11/unitree-h2-price-and-limitations/), [Botinfo H2](https://botinfo.ai/articles/unitree-h2-humanoid-robot)) |
| **EngineAI SE01** | $12k claimed teaser, real $20–30k | **€22–32k** landed | Limited international fulfilment; longer lead times. ([Origin of Bots](https://www.originofbots.com/robot/se01-by-engineai-robotics-details-specifications-rating)) |
| **UBTECH Walker S2** | $68k–$152k (configs); $180k full RaaS | **€80–135k** landed | Mass production from Nov 2025 (BYD/Foxconn). Quote-only. ([PR Newswire](https://www.prnewswire.com/news-releases/ubtech-humanoid-robot-walker-s2-begins-mass-production-and-delivery-with-orders-exceeding-800-million-yuan-302616924.html), [Robots International](https://www.robotsinternational.com/UBTECH-Walker-S2.htm)) |
| **Apptronik Apollo** | "~$80k/year RaaS-like target"; target unit price <$50k from 2027 | **Not available to BotLease in 2026.** Enterprise pilots only (MB, GXO). | ([CNBC](https://www.cnbc.com/2026/02/11/apptronik-raises-520-million-at-5-billion-valuation-for-apollo-robot.html), [SVRC](https://www.roboticscenter.ai/store/product/apptronik-apptronik-apollo)) |
| **Figure 02/03** | ~$130k/unit commercial (analyst est.) | **Not available to BotLease in 2026.** Figure 02 retired Oct 2025, Figure 03 enterprise-only. | ([Robozaps Figure](https://blog.robozaps.com/b/figure-02-review)) |
| **Agility Digit v4** | ~$30/hr RaaS (Agility-direct) | **Not available** to a 3rd-party lessor. Agility sells RaaS direct to GXO/Amazon/Toyota. | ([Agility/GXO](https://www.agilityrobotics.com/content/digit-deployed-at-gxo-in-historic-humanoid-raas-agreement)) |
| **1X NEO** | $20,000 purchase / $499/mo subscription (Norway/US direct) | **Q1 2027 EU**, $200 deposit pre-order, supply-constrained | Vendor already operates a direct €/$ subscription; BotLease has no margin window. ([Robot Report](https://www.therobotreport.com/1x-announces-pre-order-launch-neo-humanoid-robot/), [1X](https://www.1x.tech/discover/neo-home-robot)) |

**Verdict on the catalogue's `purchase_eur` numbers:** internally consistent for the EU-built tier, **optimistic** for the Unitree H-series (the €99,900 H1-2 number is roughly EU-landed truth — keep it; the H2 at €40,900 is sketchy because the international spec costs more), and **fantasy** for the US waitlist tier (Apollo, Figure, Digit are not for sale to a small Dutch reseller, period).

---

## 3. Service cost breakdown per unit

### Methodology
- **Insurance**: NL `machinebreukverzekering` (machinery breakdown) + third-party liability (AVB) typically runs **0.5 %–1.5 % of replacement value per year** for industrial equipment, with the upper range for high-risk / mobile / autonomous gear ([Aon NL](https://www.aon.com/netherlands/producten-en-oplossingen/machinebreuk/oplossingen.jsp), [NN](https://www.nn.nl/Zakelijk/Schadeverzekeringen/Machinebreukverzekering.htm)). Humanoid robots are not yet a standard tariff product → expect **the top of the range, ~1.2–1.8 % p.a.**, possibly higher for first-of-kind cover. AI Act high-risk classification under Reg. 2023/1230 *will* push premiums up further once it bites in 2027 ([Bird & Bird](https://www.twobirds.com/en/insights/2026/smart-robots,-dual-regulations-navigating-the-ai-act-and-machinery-compliance)).
- **Maintenance / parts reserve**: industry rule of thumb **5–15 % of acquisition price per year** ([Robotomated](https://robotomated.com/learn/cost/robot-maintenance-cost-annual), [PatentPC](https://patentpc.com/blog/robotics-maintenance-costs-operating-efficiency-data)). Humanoids are newer and more fragile than 6-axis arms; use **10 % p.a. for Asian value tier, 8 % p.a. for EU/US premium tier** (better parts chain).
- **Swap-SLA**: a 24h backup unit costs you 1 robot in float per ~10 contracts (10 %). Logistics (courier + tech site visit) ~€150–€300 per swap, 1–2 swaps/year typical → **~€30–€60/mo amortised + the cost-of-capital on the float unit**.
- **Helpdesk / fleet-ops**: realistic load ~30–50 contracts per FTE for a NL operation with NL-language support and field swaps. At a €55k loaded FTE that's **€90–€150/mo per contract**.
- **Software/cloud/telemetry**: fleet-management SaaS (Formant, InOrbit, Freedom) ~€80–€150/unit/month, plus connectivity (4G/5G) ~€20–€40/mo. **€100–€180/mo total.**

### Per-unit monthly burden (realistic)

| Cost line | Small Asian unit (€16–50k acq.) | Large EU/US unit (€60–120k acq.) |
|---|---|---|
| Insurance @ 1.5 % p.a. | **€20–60** | **€75–150** |
| Maintenance/parts reserve | €130–415 (10 % p.a.) | €400–800 (8 % p.a.) |
| Swap-SLA logistics + float | €30–60 | €60–120 |
| Helpdesk / fleet-ops | €90–150 | €120–180 |
| Software / cloud / telemetry | €100–180 | €100–180 |
| **Total cash service burden** | **€370–865/mo** | **€755–1,430/mo** |

This is **before** financing cost on the asset. At a 7 % cost of capital amortised over 36 months, add another **~3 % of acquisition price per month** (i.e. €480–€1,500/mo for €16k–€50k units, €1,800–€3,600/mo for €60k–€120k units) just to recover the capex with margin. **That financing/depreciation line dominates the P&L** — service cost is real but secondary.

---

## 4. Competitor & market pricing benchmark

| Player | Model / offer | Pricing | Source |
|---|---|---|---|
| **Agility Robotics** (direct) | Digit RaaS @ GXO, Amazon, Toyota | **~$30/hr** all-in (≈ $5–7k/mo @ 1 shift, $14–18k/mo @ 24/7) | [Agility/GXO release](https://www.agilityrobotics.com/content/digit-deployed-at-gxo-in-historic-humanoid-raas-agreement) |
| **AGIBOT** | EU RaaS launch at MWC 2026, 17 countries | **From €899/mo** (small unit) | [AGIBOT MWC 2026](https://www.agibot.com/article/231/detail/44.html) |
| **Apptronik** | Apollo RaaS (target 2027) | **~$80k/yr** ≈ €6,200/mo | [CNBC](https://www.cnbc.com/2026/02/11/apptronik-raises-520-million-at-5-billion-valuation-for-apollo-robot.html) |
| **1X** | NEO subscription | **$499/mo** consumer; $20k purchase | [Robot Report](https://www.therobotreport.com/1x-announces-pre-order-launch-neo-humanoid-robot/) |
| **Universal Robots** (via DLL) | UR cobot lease NL | **From ~€450/mo** (small UR), UR30 ~$1,722/mo | [UR Financial Services](https://www.universal-robots.com/nl/producten/cobot-leasing/) |
| **Smart Robotics** (Eindhoven) | RaaS for pick-and-place | Quote-only, but explicit RaaS model | [Logistics review](https://www.logisticstransportationreview.com/smart-robotics) |
| **Avular** (Eindhoven) | Mobile robot platforms | Sale + custom dev, *not* a lease shop | [Avular](https://www.avular.com/) |
| **RoboHouse** (TU Delft) | Fieldlab, not a leasing co. | — | [robohouse.nl](https://robohouse.nl/) |
| **SVRC / Robotics Center** | Robot leasing Amsterdam aggregator | **From $800/mo** | [SVRC Amsterdam](https://www.roboticscenter.ai/leasing/amsterdam) |
| **Global RaaS benchmark** | Full-service humanoid lease | **$2,000–$8,000/mo** typical | [Robozaps pricing guide](https://blog.robozaps.com/b/humanoid-robot-pricing-guide) |

**Defensible BotLease position:** there is *no* dominant Dutch competitor in the **humanoid** category yet. The competition is:
1. **Vendor-direct** (NEURA, 1X, Agility) — but they have long waitlists and don't service Dutch SMEs.
2. **German distributors** (RobotShop EU, QUADRUPED, MyBotShop) — these sell, they don't lease + service.
3. **Cobot leasing** (UR/DLL) — adjacent, much cheaper, mature.

BotLease's wedge is **NL-language SLA + speed-to-deploy + EU AI-Act paperwork done for you**. That's worth €300–€600/mo premium over a German bare-metal sale price — *not* the 30 %+ markup currently baked in.

---

## 5. Per-model unit economics (realistic)

**Assumptions:** 36-month lease, **75 %** average utilisation/availability (slack for swap & churn), residual value 25 % of acquisition at month 36 (resale + parts), cost of capital 7 % p.a., service burden mid-point from §3, financing cost included.

| Model | EU landed acq. | Service burden €/mo | Financing+depr. €/mo | True cost €/mo | Current lease €/mo | True gross margin €/mo | Payback (mo) on unit | Annual gross profit/unit (full util.) |
|---|---|---|---|---|---|---|---|---|
| NEURA 4NE-1 Mini | €22k | €450 | €700 | **€1,150** | €890 | **−€260** ⚠ | n/a | **−€3.1k** |
| NEURA 4NE-1 Gen 3.5 | €90k | €1,050 | €2,800 | **€3,850** | €4,490 | €640 | 140 | €7.7k |
| PAL Kangaroo | €95k | €1,100 | €2,950 | **€4,050** | €3,490 | **−€560** ⚠ | n/a | **−€6.7k** |
| PAL TIAGo Pro | €65k | €850 | €2,000 | **€2,850** | €1,890 | **−€960** ⚠ | n/a | **−€11.5k** |
| Pollen Reachy 2 | €68k | €900 | €2,100 | **€3,000** | €2,690 | **−€310** ⚠ | n/a | **−€3.7k** |
| Unitree R1 | €8k | €380 | €270 | **€650** | €290 | **−€360** ⚠ | n/a | **−€4.3k** (loss leader) |
| Unitree G1 Edu | €23k | €450 | €730 | **€1,180** | €899 | **−€280** ⚠ | n/a | **−€3.4k** |
| Unitree H1-2 | €110k | €1,250 | €3,400 | **€4,650** | €3,990 | **−€660** ⚠ | n/a | **−€7.9k** |
| Unitree H2 | €45k | €700 | €1,400 | **€2,100** | €1,890 | −€210 ⚠ | n/a | **−€2.5k** |
| EngineAI SE01 | €28k | €500 | €870 | **€1,370** | €1,290 | −€80 ⚠ | n/a | **−€1.0k** |
| UBTECH Walker S2 | €95k | €1,100 | €2,950 | **€4,050** | €3,290 | **−€760** ⚠ | n/a | **−€9.1k** |
| Apptronik Apollo* | €45k* | €800 | €1,400 | €2,200 | €3,499 | €1,299 | 35 | €15.6k |
| Figure 02/03* | €55k* | €900 | €1,700 | €2,600 | €3,899 | €1,299 | 42 | €15.6k |
| Agility Digit v4* | €70k* | €950 | €2,200 | €3,150 | €2,899 | −€250 ⚠ | n/a | −€3k |
| 1X NEO* | €20k* | €420 | €620 | €1,040 | €1,999 | €959 | 21 | €11.5k |

*Waitlist models — pricing hypothetical; BotLease cannot actually source these in 2026 (see §2).

**Setup fees** (€800–€6,500) are pure margin **only if** they actually cover delivery, on-site installation, training, EU AI-Act risk assessment, and CE/declaration paperwork. Realistically these activities cost €1,500–€3,500 in founder-time + travel + a contracted compliance reviewer. So **most setup fees roughly break even**, with maybe €500–€1,500 of margin on the larger contracts. Treat setup as cashflow-acceleration, not profit.

### Headline finding
**At current monthly rates, ~10 of the 15 models lose money on a fully-loaded basis.** The catalogue's original formula (30 % margin + 25 % service + 8 % insurance over 36 months) implicitly assumed no cost of capital, no swap float, no helpdesk FTE, and 100 % utilisation — none of which hold for a solo founder.

---

## 6. Recommended pricing changes

| Model | Current €/mo | Recommended €/mo | Δ | Rationale |
|---|---|---|---|---|
| NEURA 4NE-1 Mini | 890 | **1,295** | +€405 | EU-built premium, low competition, current price loss-making. |
| NEURA 4NE-1 Gen 3.5 | 4,490 | **4,490** keep | 0 | Roughly correct; margin thin but positive. |
| PAL Kangaroo | 3,490 | **4,250** | +€760 | Loss at current price; EU-veteran premium justifies higher. |
| PAL TIAGo Pro | 1,890 | **2,950** | +€1,060 | Severe loss; competitor benchmark (Smart Robotics, SVRC) supports €2,500–€3,200. |
| Pollen Reachy 2 | 2,690 | **3,250** | +€560 | Loss-making; niche AI-research demand is price-inelastic. |
| Unitree R1 | 290 | **290** keep | 0 | **Explicitly a loss-leader / funnel product.** Cap at 3 units across fleet, don't promote as growth driver. |
| Unitree G1 Edu | 899 | **1,295** | +€396 | Bestseller — small uplift defensible vs €23k QUADRUPED.DE sale price. |
| Unitree H1-2 | 3,990 | **4,890** | +€900 | Loss at current price. |
| Unitree H2 | 1,890 | **2,250** | +€360 | Just-positive margin. |
| EngineAI SE01 | 1,290 | **1,590** | +€300 | Marginally loss-making. |
| UBTECH Walker S2 | 3,290 | **4,250** | +€960 | Heavy loss; this is a €95k unit. |
| Apptronik Apollo | 3,499 | **— remove / "reservation only"** | — | Cannot source 2026. Keep as €100 refundable deposit lead-gen. |
| Figure 02/03 | 3,899 | **— remove / "reservation only"** | — | Same. Figure 02 retired Oct 2025 ([Figure](https://www.figure.ai/news/production-at-bmw)). |
| Agility Digit v4 | 2,899 | **— "Op aanvraag" only** | — | Agility direct-RaaS only; BotLease is not in that channel. |
| 1X NEO | 1,999 | **1,999** keep | 0 | If/when Q1 2027 shipping starts, margin is OK — but watch 1X-direct €459/mo competition. |

**Setup fees**: leave as-is except increase R1/G1 to **€1,200/€1,800** (current €800/€1,500 doesn't even cover transport + a half-day install).

---

## 7. 12-month break-even scenarios

**Baseline fixed costs (all three scenarios):**

| Line | €/mo | €/yr |
|---|---|---|
| Founder gross (€5k net ≈ €7k loaded with sociale lasten if DGA) | 7,000 | 84,000 |
| Office/desk (Spaces, WeWork, or thuis) | 400 | 4,800 |
| Software & infra (CRM, accounting, Vercel, telemetry baseline) | 250 | 3,000 |
| Marketing (SEO, ads, content, beurs) | 1,500 | 18,000 |
| Legal/accounting/advisor | 800 | 9,600 |
| Insurance baseline (AVB + cyber, before per-unit cover) | 200 | 2,400 |
| **Total fixed** | **€10,150/mo** | **€121,800/yr** |

Plus **per-unit cost of capital + service** scales with contracts (see §5).

### Scenario A — Pessimistic
- 4 contracts signed across year 1 (1 G1, 1 H2, 1 SE01, 1 TIAGo Pro), average ramp month-of-signing = month 8
- Gross margin €/mo (at recommended new prices): ~€350/contract × 4 × ~4 mo avg active = **€5.6k margin from leases**
- Setup-fee revenue: 4 × ~€2k avg = **€8k**
- Total year-1 revenue contribution to fixed costs: **~€13.6k**
- Fixed costs: €121.8k
- **Year-1 loss: ~€108k.** Break-even month: **month 36+** at this pace.

### Scenario B — Realistic
- 10 contracts signed across year 1 (mix: 3 G1, 2 H2, 2 TIAGo Pro, 1 NEURA Mini, 1 SE01, 1 Walker S2), average ramp month = 7.5
- Gross margin €/mo (post-repricing): ~€500/contract × 10 × ~4.5 mo avg active = **€22.5k margin from leases**
- Setup-fee revenue: 10 × ~€2.5k = **€25k** (cashflow front-loaded)
- Year-1 revenue contribution: **~€47.5k**
- Fixed costs: €121.8k
- **Year-1 loss: ~€74k.** Break-even month (operating, run-rate): **month 18–20.**
- **Capex required upfront for fleet: ~€450k** — fatal for a solo founder unless asset-light.

### Scenario C — Aggressive (also requires asset-light pivot)
- 20 contracts signed by month 12 (origination-fee model, not fleet-on-balance-sheet)
- BotLease earns 10 % origination + €400/mo service margin per contract
- Origination fees: 20 × ~€35k avg ticket × 10 % = **€70k**
- Service-margin recurring: €400 × 20 × ~5 mo avg = **€40k**
- Setup-fee revenue (BotLease keeps the install fee): 20 × €2k = **€40k**
- Year-1 revenue: **~€150k**
- Fixed costs: €121.8k
- **Year-1 profit: ~€28k. Break-even month: month 11.** Feasible.

### Cashflow note
- Pure-subscription model: cashflow follows a slow ramp, only positive in year 2.
- Setup-fee-heavy model: front-loaded — every signed contract delivers €1.5–€3k of margin in the signing month, which is the only way to survive year 1 without funding.
- Asset-light/originator model (Scenario C): cashflow positive almost immediately because no capex outflow precedes lease inflow.

---

## 8. Risks & mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| **USD FX on Apollo/Figure/Digit/NEO** | A 10 % EUR/USD move = €5–13k swing per unit | Hedge with forward contracts at contract signing; or only price these in USD pass-through. |
| **Customer churn at month-12 opt-out** | If contracts allow it, you might lose 20–40 % of book before unit is paid back | Make minimum non-cancellable term 18 months for units >€40k acq.; charge early-termination = remainder of capex schedule. |
| **Manufacturer mid-contract price changes** | BotLease eats it on the existing fleet | Lock acquisition price at PO; for waitlist robots, only accept customer deposits, no fixed customer price until you have your own price locked. |
| **Insurance claim — robot damages person or property** | A single AVB claim could be €100k–€500k+; reputational damage worse | Mandatory CE-conformity check pre-deploy; require customer-side safety briefing on signed acceptance; baseline AVB €5M cover. EU AI Act Reg 2023/1230 high-risk assessment for every deployment ([Bird & Bird](https://www.twobirds.com/en/insights/2026/smart-robots,-dual-regulations-navigating-the-ai-act-and-machinery-compliance)). |
| **AI Act enforcement Q1 2027** | Penalties up to 7 % of global turnover; high-risk classification likely for industrial humanoids | Build compliance now: technical file template, log-keeping (data sheets per deployment), human-oversight design in every install. Charge €500–€1,500 of the setup fee explicitly for this. |
| **Residual value collapse** | If Unitree/UBTECH drop H-series price 30 % in 2026 (likely — they're in a price war), BotLease's used-fleet value collapses | Depreciate aggressively (50 % residual in 36 months, not 25 %); pass through "tech refresh" right to swap to newer model after 24 mo for a fee. |
| **Solo founder concentration risk** | Vacation? Illness? Burnout? Helpdesk SLA dies. | Contract a backup field engineer in NL (Eindhoven cluster) on retainer day 1. |

---

## 9. "What would have to be true" for 12-month break-even

Given €121.8k of annualised fixed costs (§7), and assuming setup fees roughly cover their own delivery cost (small positive contribution), **break-even on a run-rate basis at month 12 requires that the active contract book at month 12 generates ≥€10,150/mo of gross margin**.

Three falsifiable paths:

**Path 1 — High-margin, full-fleet (capital-intensive, unlikely)**
- **N = 17 active contracts** by month 12
- Average gross margin **€600/mo per contract** (achievable only at repriced rates from §6, and only on EU-built / large-Asian models)
- Average ramp month = month 6 → only 6 months of run-rate
- Requires **~€700k–€900k of robot capex** by month 12. **Solo founder cannot finance this without a debt facility.**
- Realistic only with a credit line or revenue-based financing partner.

**Path 2 — Originator / asset-light (feasible)**
- **N = 12 active contracts** by month 12, financed by DLL or vendor
- BotLease earns **€450/mo service+origination margin per contract** + €2.5k setup/origination ticket
- Service-margin run-rate at month 12: 12 × €450 = **€5,400/mo** (short of €10,150)
- BUT setup/origination revenue €30k smoothed over year = **€2,500/mo** → still €2,250/mo short
- Need either N=15+ contracts or push origination ticket toward €4k → **plausible.**

**Path 3 — High-ticket, low-N (most likely real path)**
- **N = 6 active large-format contracts** (NEURA Gen 3.5 fleet to 2 customers, plus 4 medium tickets)
- Average gross margin **€1,400/mo** per large contract via repricing
- Plus 4 small contracts × €400/mo = €1,600/mo
- Total run-rate: 2×€1,400 + 4×€400 = **€4,400/mo run-rate** at month 12
- Plus setup ticket smoothed = **+€2,500/mo** equivalent
- **Total ≈ €6,900/mo. Still €3,200/mo short of break-even.**

**Bottom line falsifiable target:** 12-month operational break-even requires **N ≥ 15 active contracts by month 12 at a blended gross margin of €550–€700/mo, plus €30k+ of setup-fee margin captured in-year, AND a financing partner so capex doesn't kill cashflow.** Anything less → break-even slips to month 18–24.

If Thomas can sign **1.5 contracts per month from month 3 onward** (i.e. ~15 in the first 12 months), at repriced rates, with DLL or similar carrying the asset → it works. If not, plan for an 18–24 month runway and raise / debt-finance accordingly.

---

*End of document. ~3,400 words.*
