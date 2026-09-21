# WASTR Waste Operations Single Source of Truth

> **Document ID:** WASTR-SSOT-WASTE-001  
> **Status:** Foundation reference — requires location- and receiver-specific validation before operational use  
> **Version:** 1.0.0  
> **Prepared:** 2026-09-17  
> **Primary reference basis:** Retura Norway’s public `Kildesortering` and `Oppsamlingsutstyr` information, supplemented by related Retura fraction and equipment guidance.  
> **Intended use:** Content generation, product design, data modeling, routing logic, equipment recommendations, traceability workflows, and GitHub version control.

---

## Contents

- [1. Governance and scope](#1-governance-and-scope)
- [2. Core principles](#2-core-principles)
- [3. Canonical taxonomy](#3-canonical-taxonomy)
- [4. Canonical equipment catalog](#4-canonical-equipment-catalog)
- [5. Vehicle catalog](#5-vehicle-catalog)
- [6. Fraction knowledge base](#6-fraction-knowledge-base)
- [7. Matching logic](#7-matching-logic)
- [8. Routing and recommendation engine](#8-routing-and-recommendation-engine)
- [9. Data model](#9-data-model)
- [10. API and content schema](#10-api-and-content-schema)
- [11. Validation and traceability](#11-validation-and-traceability)
- [12. Product UX rules](#12-product-ux-rules)
- [13. Localisation and versioning](#13-localisation-and-versioning)
- [14. Glossary](#14-glossary)
- [15. Source and validation notes](#15-source-and-validation-notes)

---

# 1. Governance and scope

## 1.1 Purpose

This file is WASTR’s **canonical operational reference** for waste fractions, source sorting, collection equipment, vehicle matching, collection constraints, and traceability data.

It is designed to support:

- Public-facing waste-sorting content.
- Customer questionnaires and guided disposal flows.
- Container and equipment recommendations.
- Pickup quoting, job creation, and route planning.
- Operator and partner workflows.
- Waste traceability, compliance documentation, and reporting.
- A stable product-design reference in GitHub.

## 1.2 What this file is not

This is not a legally binding receiving specification, waste-acceptance permit, or hazardous-waste assessment. Local rules can differ by municipality, receiving facility, contract, downstream processor, and jurisdiction.

**Mandatory product rule:** WASTR must store each deployed operational rule with a location, receiver/operator, source link or contract reference, validation date, and owner.

## 1.3 Authority hierarchy

When data conflicts, apply this precedence order:

1. Applicable legislation and regulator instructions.
2. Receiving-facility permit and current acceptance specification.
3. Customer contract and service-level agreement.
4. Carrier safety rules and equipment operating limits.
5. WASTR local operational configuration.
6. This reference file’s general guidance.

## 1.4 Canonical terms

| Canonical term | Norwegian term | Definition |
|---|---|---|
| Waste fraction | Avfallsfraksjon | Operational stream that has defined acceptance, collection, and treatment rules |
| Source sorting | Kildesortering | Separating waste where it is generated |
| Bin | Beholder / dunk | Usually a wheeled container, commonly 140–1,000 L |
| Container | Container | Large skip/container, normally collected by lift or hook-lift vehicle |
| Cage | Bur | Metal collection cage, often used for EE waste or palletised material |
| Bulk bag | Storsekk / big bag | Flexible bag for bulky waste or material, commonly 1–2 m3 |
| Contamination | Feilsortering / forurensning | Unwanted material, moisture, residues, or hazardous content in a fraction |
| Receiver | Mottak / behandlingsanlegg | Facility that accepts, sorts, treats, or transfers waste |
| Hazardous waste | Farlig avfall | Waste requiring special management because of environmental or health hazards |
| Risk waste | Risikoavfall | Healthcare/medical waste that may present health or environmental risk |

---

# 2. Core principles

## 2.1 Sorting principle

Waste must be classified and separated as close as possible to the point of generation. Correct sorting protects material quality, supports reuse and recycling, reduces contamination, and can lower residual-waste costs.

## 2.2 Safety-first hierarchy

Apply this decision sequence for every item or load:

1. **Hazard screening:** Does it contain chemicals, oil, paint, batteries, gas, asbestos, PCB, chlorinated paraffin, refrigerants, sharps, biological material, or a hazard label?
2. **Electricity screening:** Has it used or conducted electricity, or does it contain a battery/electronic component?
3. **Packaging screening:** Is it packaging, rather than a product made from the same material?
4. **Material screening:** What are the main material(s): paper, plastic, glass, metal, wood, mineral, textile, food/organic, rubber?
5. **Condition screening:** Is it clean, dry, empty, intact, contaminated, wet, bulky, sharp, or damaged?
6. **Access and logistics screening:** What quantity, weight, density, storage equipment, vehicle access, lifting method, and pickup frequency are required?

## 2.3 Waste hierarchy

Use the following preference order in content, recommendation logic, and reporting:

1. Prevent waste.
2. Reuse.
3. Prepare for reuse.
4. Material recycling.
5. Biological treatment, where applicable.
6. Energy recovery.
7. Disposal / landfill only where permitted and appropriate.

## 2.4 Required distinction rules

- **EE waste overrides material:** An electrical product is EE waste, not ordinary metal or plastic.
- **Hazard overrides ordinary fraction:** An item with hazardous residues must not enter an otherwise compatible recyclable stream.
- **Packaging is not product:** A plastic packaging tray may go to plastic packaging; a plastic toy usually does not.
- **Impregnated wood is hazardous:** It must not enter clean or mixed wood.
- **Window glass is not glass packaging.**
- **Ceramics and porcelain are not glass packaging.**
- **Gypsum must remain dry and separate.**
- **Infectious waste must never enter residual waste or standard containers.**

---

# 3. Canonical taxonomy

## 3.1 Top-level categories

| ID | Category | Norwegian | Typical handling class |
|---|---|---|---|
| CAT-RES | Residual and mixed waste | Restavfall / blandet avfall | Ordinary waste |
| CAT-PAP | Paper, cardboard, cartons | Papp, papir og kartong | Recyclable |
| CAT-PLA | Plastics | Plast | Recyclable |
| CAT-GLM | Glass and metal packaging | Glass- og metallemballasje | Recyclable |
| CAT-MET | Metal scrap | Metall / jern og metaller | Recyclable |
| CAT-ORG | Food and organic waste | Matavfall / organisk avfall | Biological treatment |
| CAT-GAR | Garden waste | Hageavfall | Biological treatment |
| CAT-WOD | Wood | Trevirke | Recyclable / energy / hazardous |
| CAT-MIN | Mineral and construction materials | Masser / byggeavfall | Recycling / landfill / specialist |
| CAT-EE | Electrical and electronic waste | EE-avfall | Regulated producer-responsibility stream |
| CAT-HAZ | Hazardous waste | Farlig avfall | Hazardous |
| CAT-RSK | Risk and healthcare waste | Risikoavfall | Specialist hazardous/healthcare |
| CAT-RUB | Rubber and tires | Gummi / dekk | Specialist recovery |
| CAT-TEX | Textiles and bulky reuse | Tekstiler / møbler | Reuse / recycling / residual |
| CAT-AQU | Aquaculture and fisheries waste | Oppdretts- og fiskeriavfall | Specialist recovery |

## 3.2 Canonical fraction IDs

Fraction IDs must be stable. Display names may be localized; IDs must not be changed after production release.

| Fraction ID | English display name | Norwegian display name | Category | Handling class |
|---|---|---|---|---|
| FR-RES-SORTED | Sorted residual waste | Sortert restavfall | CAT-RES | Ordinary combustible |
| FR-RES-MIXED | Mixed/unsorted waste | Blandet avfall | CAT-RES | Sorting / restricted |
| FR-PAP-MIXED | Mixed paper, cardboard and carton | Blandet papir, papp og kartong | CAT-PAP | Recyclable |
| FR-PAP-CARDBOARD | Corrugated and solid cardboard | Bølgepapp og massiv papp | CAT-PAP | Recyclable |
| FR-PAP-CONF | Confidential paper for shredding | Makulering | CAT-PAP | Secure recycling |
| FR-PLA-PACK | Plastic packaging | Plastemballasje | CAT-PLA | Recyclable |
| FR-PLA-FILM-CLEAR | Clear plastic film | Klar plastfolie | CAT-PLA | Recyclable |
| FR-PLA-FILM-COLOUR | Coloured plastic film | Farget folieplast | CAT-PLA | Recyclable |
| FR-PLA-RIGID-PACK | Rigid plastic packaging | Hardplastemballasje | CAT-PLA | Recyclable |
| FR-PLA-RIGID | Rigid non-packaging plastic | Hardplast | CAT-PLA | Receiver-specific |
| FR-PLA-MIXED | Mixed plastics | Blandet plast | CAT-PLA | Receiver-specific |
| FR-PLA-PPBAG | Polypropylene bulk bags | PP-sekk / bigbag | CAT-PLA | Recyclable |
| FR-PLA-DEPOSIT | Deposit bottles | Panteflasker | CAT-PLA | Deposit system |
| FR-GLM-PACK | Glass and metal packaging | Glass- og metallemballasje | CAT-GLM | Recyclable |
| FR-GLS-FLAT | Flat/window glass | Vindusglass | CAT-GLM | Specialist recycling |
| FR-MET-MIXED | Mixed metals | Blandede metaller | CAT-MET | Recyclable |
| FR-MET-FERROUS | Ferrous metal | Jernholdig metall | CAT-MET | Recyclable |
| FR-MET-NONFERROUS | Non-ferrous metal | Ikke-jernholdig metall | CAT-MET | Recyclable |
| FR-ORG-UNPACKED | Unpackaged food waste | Matavfall uemballert | CAT-ORG | Biological |
| FR-ORG-PACKAGED | Packaged food waste | Matavfall emballert | CAT-ORG | Specialist depackaging |
| FR-ORG-UCO | Used cooking oil | Frityrolje | CAT-ORG | Specialist liquid recovery |
| FR-GAR-GREEN | Garden waste | Hageavfall | CAT-GAR | Biological |
| FR-WOD-CLEAN | Clean untreated wood | Rent trevirke | CAT-WOD | Recycling / energy |
| FR-WOD-MIXED | Mixed treated/surface-coated wood | Blandet trevirke | CAT-WOD | Recycling / energy |
| FR-HAZ-WOOD-IMP | Impregnated wood | Impregnert trevirke | CAT-HAZ | Hazardous |
| FR-MIN-CONC-CLEAN | Concrete without reinforcement | Betong uten armeringsjern | CAT-MIN | Mineral recycling |
| FR-MIN-CONC-REINF | Reinforced concrete | Betong med armeringsjern | CAT-MIN | Mineral/metal recovery |
| FR-MIN-BRICK | Brick and roof tile | Tegl og takstein | CAT-MIN | Mineral recycling |
| FR-MIN-SOIL-CLEAN | Clean soil, stone, sand and gravel | Rene masser | CAT-MIN | Mineral recovery |
| FR-MIN-SOIL-CONTAM | Contaminated soil | Forurenset masse | CAT-HAZ | Controlled treatment |
| FR-MIN-GYPSUM | Gypsum | Gips | CAT-MIN | Dry recycling stream |
| FR-MIN-MINWOOL | Mineral wool/insulation | Mineralull / isolasjon | CAT-MIN | Specialist landfill/recovery |
| FR-MIN-EPS | EPS/XPS insulation | Isopor / EPS/XPS | CAT-MIN | Plastic/mineral specialist |
| FR-MIN-CERAMIC | Ceramics and porcelain | Keramikk og porselen | CAT-MIN | Inert/residual per receiver |
| FR-EE-MIXED | Mixed EE waste | Blandet EE-avfall | CAT-EE | Regulated |
| FR-EE-LARGE | Large appliances | Hvitevarer | CAT-EE | Regulated |
| FR-EE-COLD | Cooling appliances | Kuldemøbler | CAT-EE | Regulated specialist |
| FR-EE-LAMPS | Lamps and fluorescent tubes | Lyspærer og lysstoffrør | CAT-EE | Hazardous/regulated |
| FR-HAZ-OIL | Waste oil | Spillolje | CAT-HAZ | Hazardous |
| FR-HAZ-OILFILTER | Oil filters | Oljefiltre | CAT-HAZ | Hazardous |
| FR-HAZ-PAINT | Paint, glue and varnish | Maling, lim og lakk | CAT-HAZ | Hazardous |
| FR-HAZ-SOLVENT | Solvents and cleaning chemicals | Løsemidler og rengjøringsmidler | CAT-HAZ | Hazardous |
| FR-HAZ-AEROSOL | Aerosols/spray cans | Spraybokser | CAT-HAZ | Hazardous/pressurised |
| FR-HAZ-GAS | Gas cylinders/containers | Gassbeholdere | CAT-HAZ | Pressurised |
| FR-HAZ-BATTERY | Batteries | Batterier | CAT-HAZ | Hazardous/regulated |
| FR-HAZ-EXTING | Fire extinguishers | Brannslukkere | CAT-HAZ | Pressurised |
| FR-HAZ-ASB | Asbestos | Asbest | CAT-HAZ | Hazardous |
| FR-HAZ-PCBWIN | PCB-containing windows | Vindu med PCB | CAT-HAZ | Hazardous |
| FR-HAZ-CPWIN | Chlorinated-paraffin windows | Vindu med klorparafin | CAT-HAZ | Hazardous |
| FR-RSK-INFECT | Infectious waste | Smittefarlig avfall | CAT-RSK | Healthcare specialist |
| FR-RSK-SHARPS | Sharps | Stikkende/skjærende avfall | CAT-RSK | Healthcare specialist |
| FR-RSK-PHARM | Pharmaceutical waste | Medisinavfall | CAT-RSK | Healthcare specialist |
| FR-RSK-CYTO | Cytostatic waste | Cytostatika | CAT-RSK | Healthcare specialist |
| FR-RUB-TIRES | Tires | Dekk | CAT-RUB | Producer-responsibility/specialist |
| FR-RUB-OTHER | Other rubber | Gummi | CAT-RUB | Receiver-specific |
| FR-TEX-REUSE | Reusable textiles | Tekstiler til ombruk | CAT-TEX | Reuse |
| FR-TEX-RECYCLE | Textile recycling | Tekstiler til materialgjenvinning | CAT-TEX | Recycling |
| FR-BULK-FURN | Furniture and fixtures | Møbler og inventar | CAT-TEX | Reuse/disassembly |
| FR-AQU-CAGES | Aquaculture cages | Merder | CAT-AQU | Specialist recovery |
| FR-AQU-ROPE | Ropes and hawsers | Tau og trosser | CAT-AQU | Specialist recycling |
| FR-AQU-FEEDHOSE | PP/PE feed hoses | Fôrslanger (PP/PE-rør) | CAT-AQU | Specialist recycling |
| FR-AQU-NET-CU | Copper-impregnated nets | Kobberimpregnerte nøter | CAT-AQU | Controlled specialist |
| FR-AQU-NET-NCU | Non-copper-impregnated nets | Ikke-kobberimpregnerte nøter | CAT-AQU | Specialist recycling |
| FR-AQU-LICESKIRT | Lice skirts | Luseskjørt | CAT-AQU | Specialist recycling |

---

# 4. Canonical equipment catalog

## 4.1 Equipment class overview

| Equipment class | Primary role | Typical size/capacity | Primary handling method |
|---|---|---:|---|
| Wheeled bin | Small/medium recurring collection | 140–1,000 L | Bin lifter / collection truck |
| Bag stand | Flexible plastic-film collection | Usually 240 L bags | Manual bag swap / box truck or route vehicle |
| Bulk bag | Limited-space or irregular bulky waste | 1–2 m3, often max 1,000 kg | Crane, forklift, or manual/box truck workflow |
| Cage | Secure palletised/bulky collection | Variable | Forklift, crane, box truck |
| Lift container | Medium-volume collection | Approximately 2–20 m3 | Lift truck |
| Hook-lift container | Large-volume/bulk collection | Approximately 22–38 m3 | Hook-lift truck |
| Closed container | Keep fraction dry/secure | Approximately 4.5–10 m3 | Lift / compactor vehicle |
| Compactor | Reduce volume and pickup frequency | Approximately 8–30 m3 system | Compactor/lift/hook vehicle |
| Baler | Compress cardboard/plastic into bales | 50–250 kg/bale typical | Forklift/pallet transport |
| Hazardous-waste package | Safe compliant storage/transport | 2 L–1,000 L | Specialist hazardous transport |
| Risk-waste package | Infectious/sharps containment | 2.1 L–50 L common | Specialist healthcare collection |

## 4.2 Wheeled bins

| Equipment ID | Name | Volume | Typical dimensions (W x D x H) | Max total weight | Typical fractions |
|---|---|---:|---|---:|---|
| EQ-BIN-140 | Wheeled bin 140 L | 140 L | 480 x 560 x 1,070 mm | 70 kg | Food waste, residual, paper |
| EQ-BIN-240 | Wheeled bin 240 L | 240 L | 580 x 740 x 1,070 mm | 110 kg | Residual, paper, plastic according to local system |
| EQ-BIN-360 | Wheeled bin 360 L | 360 L | 625 x 850 x 1,100 mm | 160 kg | Glass/metal packaging, residual, paper |
| EQ-BIN-660 | Wheeled bin 660 L | 660 L | 1,360 x 770 x 1,180 mm | 310 kg | Glass/metal packaging, residual, paper |
| EQ-BIN-1000 | Wheeled bin 1,000 L | 1,000 L | 1,320 x 1,080 x 1,320 mm | 490 kg | Residual, paper, commercial waste |

**Bin operating rules**

- Do not exceed mechanical lifting limits or local collection-service limits.
- Do not place hazardous, pressurised, sharp, hot, or liquid waste into ordinary bins.
- Use lids to manage weather, odor, litter, pests, and unauthorized disposal.
- For food waste, use the approved bag/liner and collection frequency for the site.
- For paper/cardboard, protect from rain and moisture.

## 4.3 Containers

| Equipment ID | Name | Volume | Typical dimensions (L x W x H) | Self-weight | Max total weight | Vehicle family | Typical fractions |
|---|---|---:|---|---:|---:|---|---|
| EQ-CNT-COMBI-4.5-C | Closed combi container | 4.5 m3 | 2.7 x 2.0 x 1.45 m | 530 kg | 2,500 kg | Lift/compactor | Residual, paper, plastic |
| EQ-CNT-COMBI-8-C | Closed combi container | 8 m3 | 3.4 x 2.0 x 1.9 m | 695 kg | 3,500 kg | Lift/compactor | Residual, paper, plastic |
| EQ-CNT-COMBI-10-C | Closed combi container | 10 m3 | 3.9 x 2.0 x 1.9 m | 860 kg | 3,500 kg | Lift/compactor | Residual, paper, plastic |
| EQ-CNT-OPEN-5 | Open lift container | 5 m3 | 3.45 x 2.0 x 1.0 m | 670 kg | 3,000 kg | Lift | Soil/masses, heavy materials |
| EQ-CNT-OPEN-8 | Open combi container | 8 m3 | 3.7 x 1.8 x 1.7 m | 730 kg | 3,500 kg | Lift/compactor | Glass, residual, metal, plastic, wood |
| EQ-CNT-OPEN-10 | Open lift container | 10 m3 | 3.6 x 2.0 x 1.8 m | 680 kg | 5,500 kg | Lift | Glass, residual, metal, plastic, wood |
| EQ-CNT-OPEN-10-COMBI | Open combi container | 10 m3 | 3.5 x 2.0 x 1.8 m | 730 kg | 3,500 kg | Lift/compactor | Glass, residual, metal, plastic, wood |
| EQ-CNT-OPEN-20 | Open lift container | 20 m3 | 5.78 x 2.05 x 2.17 m | 1,420 kg | 6,420 kg | Lift | Bulky/light fractions, construction waste |
| EQ-CNT-HOOK-22 | Open hook-lift container | 22 m3 | 6.0 x 2.5 x 1.8 m | 2,320 kg | 12,000 kg | Hook-lift | Bulk construction, metal, wood |
| EQ-CNT-HOOK-35 | Open hook-lift container | 35 m3 | 6.0 x 2.5 x 2.8 m | 2,880 kg | 12,000 kg | Hook-lift | Bulky low-density waste, wood, packaging |

**Container selection rules**

- Use **closed/covered containers** for dry recyclable material such as paper, cardboard, gypsum, and clean plastic film.
- Use **open heavy-duty containers** for dense mineral material, concrete, metal, soil, brick, and roof tiles, subject to weight limits.
- Use **large hook-lift containers** for high-volume, low-density material or large bulk operations; do not fill by volume with dense material without a weight calculation.
- A 35 m3 container is normally unsuitable for full-volume concrete or soil because legal payload and vehicle limits will be exceeded.

## 4.4 Bags, stands, cages, and pallets

| Equipment ID | Name | Capacity/specification | Best use | Key rule |
|---|---|---|---|---|
| EQ-BAG-RETPLAST-240 | Return-plastic bag | 240 L, often perforated | Plastic film / return plastic | Keep dry and free of paper/metal |
| EQ-STAND-RETPLAST | Plastic bag stand | Fits 240 L bag; approximately 110–112 cm high | Plastic film, flexible packaging | Indoor/outdoor variants; label fraction clearly |
| EQ-BAG-STANDARD-L | Standard bulk bag | 90 x 90 x 100 cm; up to 1,000 kg | Smaller bulky loads | Confirm allowed fractions and lifting access |
| EQ-BAG-XL | XL bulk bag | 95 x 220 x 90 cm; up to 1,000 kg | Large bulky loads | Do not overload; crane access may be needed |
| EQ-BAG-ASB-UN | UN-approved asbestos bag | Dust-tight seams and inner liner | Asbestos | Use only approved packaging and specialist route |
| EQ-CAGE-EE | Lockable EE-waste cage | Variable | Electrical/electronic waste | Secure against weather and theft |
| EQ-CAGE-PALLET | Pallet cage | Variable | Bulky recyclable material / parts | Use forklift/crane compatible setup |
| EQ-PALLET-BULK | Bag on pallet | 800–1,000 L typical | Bulk plastic, canisters, material feedstock | Secure load and identify fraction |

## 4.5 Compaction and baling equipment

| Equipment ID | Name | Capacity / performance | Suitable fractions | Operational benefit |
|---|---|---|---|---|
| EQ-CMP-MOBILE | Mobile compactor | Approx. 8–16 m3 | Residual, paper/cardboard | Reduces collection frequency |
| EQ-CMP-LARGE | Large compactor | Approx. 16–22 m3 | Residual, packaging cardboard | Higher-volume sites |
| EQ-CMP-STATIONARY | Stationary compactor with detachable container | Approx. 30 m3 | Residual, cardboard/paper | Separates press unit from collected container |
| EQ-CMP-ROLL | Roll compactor | Works with 600/800 L bin or bag on pallet | Cardboard, plastic, residual | Approx. 2 m2 footprint; continuous use at source |
| EQ-BALER-PACK | Packaging baler | Approx. 50–250 kg/bale | Cardboard, plastic | Produces transport-efficient bales |

**Compactor exclusions**

Never compact pressurised cylinders, gas containers, aerosols, batteries, hazardous chemicals, flammable liquids, explosive materials, infectious waste, asbestos, or unidentified items.

## 4.6 Hazardous and risk-waste equipment

| Equipment ID | Name | Capacity | Use | Mandatory controls |
|---|---|---:|---|---|
| EQ-HAZ-DRUM-200 | Steel/plastic drum with lid | 200 L | Oils, chemicals, hazardous liquids/solids | Compatibility, labeling, secure closure |
| EQ-HAZ-IBC-1000 | IBC container | 1,000 L | Approved compatible liquids | Certification, secondary containment where required |
| EQ-HAZ-CABINET | Hazardous-waste cabinet | Variable | Secure temporary storage | Locking, segregation, spill control |
| EQ-RSK-SHARP-2 | Sharps container | 2.1–4 L | Needles, syringes, sharps | Puncture resistant, closed before onward packaging |
| EQ-RSK-YELLOW-30 | Infectious-waste container | 30 L | Infectious medical waste | UN-approved, sealable, no reopening |
| EQ-RSK-YELLOW-50 | Infectious-waste container | 50 L | Infectious medical / liquid organic waste | UN-approved, sealable, no reopening |
| EQ-RSK-BOX-44 | Risk-waste box | 44 L | Dry risk waste where approved | Internal yellow liner; not for liquids |

---

# 5. Vehicle catalog

## 5.1 Vehicle classes

| Vehicle ID | Vehicle type | Norwegian | Equipment compatibility | Typical use |
|---|---|---|---|---|
| VEH-BIN | Bin-collection/box truck | Skapbil | Wheeled bins, bag stands, small cages | Dense routes and recurring bins |
| VEH-COMP | Compactor collection truck | Komprimatorbil | Bins, compatible combi containers, compacted waste | High-frequency/compressible collection |
| VEH-LIFT | Lift truck | Liftbil | Containers approximately 2–15 m3 | Standard container collection |
| VEH-HOOK | Hook-lift truck | Krokbil | Containers approximately 22–38 m3 | Large bulk containers and heavy logistics |
| VEH-CRANE | Crane truck | Kranbil | Bulk bags, awkward placement, bulky loads | Restricted access / lifting from distance |
| VEH-FORKBOX | Box truck with forklift | Varebil/lastebil med truck | Pallets, cages, bag-on-pallet | Palletised loads and controlled pickup |
| VEH-HAZ | Hazardous-waste transport | Spesialbil for farlig avfall | UN packages, drums, IBCs | Hazardous-material collection |
| VEH-RISK | Healthcare/risk-waste vehicle | Risikoavfallsbil | Sealed medical containers | Controlled medical-waste route |
| VEH-TANK | Liquid-waste tanker / specialist liquid vehicle | Tankbil | Approved liquid tanks/drums/IBCs | Used cooking oil, approved compatible liquids |

## 5.2 Vehicle selection constraints

A compatible vehicle must satisfy all of the following:

- Container lifting interface and physical dimensions.
- Estimated gross load within vehicle, equipment, and road legal limits.
- Waste class and transport requirements.
- Site access: road width, turning radius, height clearance, slope, ground bearing capacity, gate access, and crane reach.
- Pickup method: swap, empty, lift, crane, forklift, or manual loading.
- Operational time window and local restrictions.
- Required documentation and safety equipment.

---

# 6. Fraction knowledge base

## 6.1 Residual and mixed waste

### FR-RES-SORTED — Sorted residual waste

**Definition:** Combustible residual material remaining after recyclable and separately regulated fractions have been removed.

**Typical accepted material**

- Non-recyclable combustible household-like waste.
- Soiled or composite materials that cannot enter material recycling.
- Diapers, sanitary products, vacuum bags, and comparable residual items.

**Never include**

- Hazardous waste, EE waste, batteries, lamps, gas containers, aerosols, asbestos, risk waste, oil, paint, chemicals.
- Food waste where a separate food-waste system exists.
- Metals, glass/metal packaging, clean paper/cardboard, plastic packaging, gypsum, mineral waste, tires, and other separately collected streams.

**Typical equipment:** EQ-BIN-140 through EQ-BIN-1000; closed containers; compactors.

**Typical vehicles:** VEH-BIN, VEH-COMP, VEH-LIFT, VEH-HOOK depending on equipment.

**Typical treatment:** Energy recovery, subject to receiver specification.

### FR-RES-MIXED — Mixed/unsorted waste

**Definition:** A restricted mixed stream for a permitted receiving/sorting facility where full source separation is incomplete.

**Product warning:** Do not recommend this stream by default. Show it only when a selected local receiver accepts it and all prohibited fractions are excluded.

**Typical equipment:** Open or closed containers, depending on material and weather.

**Typical vehicles:** VEH-LIFT or VEH-HOOK.

## 6.2 Paper, cardboard, and cartons

### FR-PAP-MIXED — Mixed paper, cardboard and carton

**Accept**

- Clean paper.
- Corrugated cardboard.
- Brown paper.
- Solid cardboard.
- Cartons where locally included.

**Quality requirements**

- Keep clean and dry.
- A related Retura fraction guide specifies a maximum 10% moisture content.
- Flatten cardboard to reduce air transport and maximize capacity.

**Exclude**

- Wet or food-soiled paper/cardboard.
- Wet-strength paper.
- Plastic-coated or laminated material where not accepted.
- Tissue paper, napkins, food paper, gift wrap, and non-paper attachments.

**Recommended equipment:** Bins, cages, closed/covered containers, compactors, balers.

**Recommended vehicles:** VEH-BIN, VEH-COMP, VEH-LIFT, VEH-HOOK, VEH-FORKBOX for baled material.

**Treatment:** Sorting and fiber recycling.

### FR-PAP-CONF — Confidential paper for shredding

**Rule:** Use locked collection equipment and a documented chain of custody. Identify secure destruction certificate requirements in the local service configuration.

**Recommended equipment:** Lockable bin/cabinet or secure cage.

**Recommended vehicle:** VEH-BIN or dedicated secure collection vehicle.

## 6.3 Plastics

### FR-PLA-PACK — Plastic packaging

**Accept**

- Clean packaging used to contain or protect products.
- Empty bottles, tubs, trays, flexible packaging, bags, and film where allowed.

**Preparation**

- Empty, clean, and dry.
- Keep packaging with hazardous residues out of this stream.
- Follow local rules for caps, labels, and mixed-material packaging.

**Exclude**

- Plastic products that are not packaging unless the local system accepts mixed/hard plastic.
- Packaging with paint, oil, chemicals, or hazardous residues.
- EE waste and batteries.

**Recommended equipment:** Plastic bag stands, 240 L bags, bins, covered containers, balers.

**Recommended vehicles:** VEH-BIN, VEH-COMP, VEH-LIFT, VEH-FORKBOX.

### FR-PLA-FILM-CLEAR and FR-PLA-FILM-COLOUR — Plastic film

**Accept**

- Stretch wrap, shrink wrap, clean bags, and flexible packaging film.

**Quality requirements**

- Keep dry, clean, and free of paper, cardboard, strapping, metal, wood, and non-film plastic.
- Separate clear and coloured film when required; clear film can have a higher-quality recovery route.

**Recommended equipment:** EQ-BAG-RETPLAST-240 with EQ-STAND-RETPLAST; baler for high volumes.

**Recommended vehicles:** VEH-BIN, VEH-FORKBOX, VEH-LIFT depending on equipment.

### FR-PLA-RIGID-PACK — Rigid plastic packaging

**Accept:** Bottles, canisters, pots, tubs, trays, pails, and packaging crates where accepted.

**Critical rule:** Packaging contaminated by chemicals, oils, or hazardous substances must be classified through the hazardous-waste route.

### FR-PLA-PPBAG — Polypropylene bulk bags

**Accept:** Clean PP woven sacks/big bags where the receiver has a dedicated collection stream.

**Preparation:** Empty completely; remove product residues and non-plastic attachments where required.

### FR-PLA-DEPOSIT — Deposit bottles

**Rule:** Route to the deposit-return system, not ordinary plastic packaging collection.

## 6.4 Glass and metal packaging

### FR-GLM-PACK — Glass and metal packaging

**Accept**

- Jam jars and non-deposit bottles.
- Food tins and metal packaging.
- Aluminum trays/foil and metal lids.

**Preparation**

- Empty and rinse to remove food residues.
- Keep packaging loose unless local rules say otherwise.

**Exclude**

- Window glass, mirrors, drinking glasses, cookware, ceramics, porcelain, crystal/lead glass.
- Bulbs, fluorescent tubes, batteries.
- Spray cans or chemical containers.

**Recommended equipment:** Sturdy bins, containers, return-point systems.

**Recommended vehicles:** VEH-BIN, VEH-LIFT.

**Treatment:** Sorting; glass and metals are recovered separately.

### FR-GLS-FLAT — Flat/window glass

**Rule:** Keep separate from packaging glass. Screen for hazardous windows such as PCB- or chlorinated-paraffin-containing units, which require hazardous-waste classification.

## 6.5 Metals

### FR-MET-MIXED — Mixed metals

**Accept**

- Magnetic and non-magnetic metals.
- Brass, copper, aluminum, zinc, lead, tin, nickel, chromium, stainless steel.
- Mixed fittings, taps, cables, and machine parts where locally accepted.

**Exclude**

- EE waste, appliances, hazardous/pressurised items, gas cylinders, metal packaging where a separate stream exists, and excessive non-metal contamination.

**Recommended equipment:** Open containers, cages, pallets.

**Recommended vehicles:** VEH-LIFT, VEH-HOOK, VEH-FORKBOX, VEH-CRANE.

**Treatment:** Sorting, metal separation, remelting/refining.

## 6.6 Food and organic waste

### FR-ORG-UNPACKED — Unpackaged food waste

**Accept**

- Food scraps, coffee grounds, suitable tea bags, eggshells, and other biodegradable kitchen waste accepted locally.

**Exclude**

- Plastic, metal, glass, packaging, textiles, wood, garden waste, soil, sand, gravel, diapers, and residual waste.

**Recommended equipment:** Food-waste caddy/bag, lidded food-waste bin, specialized organic-waste compactor where supported.

**Recommended vehicles:** VEH-BIN, VEH-COMP.

**Treatment:** Composting or anaerobic digestion/biogas, depending on local capacity.

### FR-ORG-PACKAGED — Packaged food waste

**Rule:** Use only a dedicated packaged-food-waste service with depackaging capability. Capture packaging type and estimated non-food share.

### FR-ORG-UCO — Used cooking oil

**Rule:** Store separately from solid food waste in sealed compatible containers. Do not pour into drains.

**Recommended equipment:** Sealed drums or dedicated oil tank.

**Recommended vehicles:** VEH-TANK or VEH-HAZ when applicable.

**Traceability fields:** Source type, volume, oil condition, container ID, contamination, collection date, receiver, recovery certificate.

## 6.7 Garden waste

### FR-GAR-GREEN — Garden waste

**Accept:** Grass, leaves, plants, brush, branches, shrubs, and tree cuttings.

**Exclude:** Treated/construction wood, plastics, pots, metal, mixed household waste, and contaminated soil unless accepted separately.

**Recommended equipment:** Open container, bulk bag for small volumes, designated green-waste area.

**Recommended vehicles:** VEH-LIFT, VEH-HOOK, VEH-CRANE.

**Treatment:** Composting, chipping, and biological processing.

## 6.8 Wood

### FR-WOD-CLEAN — Clean untreated wood

**Accept:** Untreated pallets, crates, timber, framing, beams, and clean construction wood.

**Exclude:** Paint/varnish/impregnation, hazardous coatings, large non-wood attachments, and mixed construction materials.

**Recommended equipment:** Open container, covered storage if material quality requires protection.

**Recommended vehicles:** VEH-LIFT, VEH-HOOK.

### FR-WOD-MIXED — Mixed wood

**Accept:** Construction/demolition wood that can include surface paint, varnish, nails, screws, pallets, and some engineered wood where the receiver accepts it.

**Exclude:** Impregnated wood, major metal components, gypsum, cement, wallpaper/asphalt-board residues, and prohibited engineered boards as defined locally.

**Recommended equipment:** Open container, compactor where suitable.

**Recommended vehicles:** VEH-LIFT, VEH-HOOK.

### FR-HAZ-WOOD-IMP — Impregnated wood

**Rule:** Hazardous waste. Keep CCA-, copper-, and creosote-treated wood separate where required. Do not burn. Declare and use an authorized route.

**Recommended equipment:** Clearly labeled covered container or approved hazardous-waste storage.

**Recommended vehicle:** VEH-HAZ or approved dedicated transport configuration.

## 6.9 Construction and mineral waste

### FR-MIN-CONC-CLEAN and FR-MIN-CONC-REINF — Concrete

**Core rule:** Separate reinforced concrete from non-reinforced concrete when receiver pricing or treatment requires it. Screen demolition material for coatings, sealants, PCB, asbestos, and other contamination.

**Recommended equipment:** Heavy-duty open lift container; use smaller containers for dense material.

**Recommended vehicles:** VEH-LIFT; VEH-HOOK for larger operations within weight limits.

### FR-MIN-BRICK — Brick and roof tile

**Accept:** Clean brick, masonry, and roof tiles.

**Exclude:** Mixed wood, gypsum, insulation, plastics, hazardous coatings, and significant contamination.

**Recommended equipment:** Heavy-duty open container.

**Recommended vehicles:** VEH-LIFT, VEH-HOOK with payload control.

### FR-MIN-SOIL-CLEAN — Clean soil, stone, sand and gravel

**Rule:** Only use clean-mass route after local confirmation. Soil from developed sites may require characterization before it can be treated as clean.

**Recommended equipment:** EQ-CNT-OPEN-5 or other weight-controlled open container.

**Vehicle:** VEH-LIFT or VEH-HOOK, subject to legal road weight.

### FR-MIN-SOIL-CONTAM — Contaminated soil

**Rule:** Requires characterization/classification, approved receiver, documentation, and controlled transport. Class 4–5 contaminated masses are hazardous waste.

**Recommended equipment:** Covered, leak-managed container where required.

**Vehicle:** VEH-HAZ or approved carrier configuration.

### FR-MIN-GYPSUM — Gypsum

**Critical rule:** Keep dry and separate from residual waste, wood, minerals, insulation, and food waste.

**Recommended equipment:** Covered or closed dedicated container.

**Recommended vehicle:** VEH-LIFT.

### FR-MIN-MINWOOL — Mineral wool/insulation

**Accept:** Mineral wool, glass wool, and rock wool.

**Exclude:** EPS/XPS, cellular rubber, PE foam, and mixed waste.

**Recommended equipment:** Container or sacks/bulk bags.

**Recommended vehicles:** VEH-LIFT, VEH-HOOK, VEH-CRANE, VEH-FORKBOX.

**Treatment:** Often controlled landfill unless a local reuse/recycling path exists.

### FR-MIN-EPS — EPS/XPS insulation

**Rule:** Do not combine with mineral wool. Identify packaging EPS vs construction insulation and contamination condition; use the local specialized route.

## 6.10 Electrical and electronic waste

### FR-EE-MIXED — Mixed EE waste

**Definition:** Products that have used or conducted electricity, including battery-powered devices.

**Rules**

- Do not place in residual waste or scrap-metal containers.
- Store in marked, approved cages or secure covered areas.
- Protect from theft, damage, and weather.
- Secure devices containing personal/commercial data.

**Recommended equipment:** EQ-CAGE-EE, lockable storage, dedicated cages/containers.

**Recommended vehicles:** VEH-FORKBOX, VEH-CRANE, dedicated EE logistics as configured.

### FR-EE-LARGE — Large appliances

**Rule:** Keep appliances separate from ordinary scrap metal; route to EE system.

### FR-EE-COLD — Cooling appliances

**Rule:** Specialist EE fraction due to refrigerants and components; keep intact and dry.

### FR-EE-LAMPS — Lamps and fluorescent tubes

**Rule:** Protect from breakage. Treat as regulated/hazardous EE stream; never place in glass, residual, or metal waste.

## 6.11 Hazardous waste

### Common operating controls for all FR-HAZ-* fractions

- Preserve original labels and packaging where safe.
- Do not mix incompatible chemicals.
- Keep containers closed, upright, protected from weather, and secured against unauthorized access.
- Record quantity, packaging, hazard labels, declared content, generator, and declaration/consignment data.
- Use approved collection and receiving routes.

### Hazard-specific rules

| Fraction | Main rule | Typical equipment | Vehicle |
|---|---|---|---|
| FR-HAZ-OIL | Keep oils segregated and sealed | EQ-HAZ-DRUM-200 / EQ-HAZ-IBC-1000 | VEH-HAZ / VEH-TANK |
| FR-HAZ-OILFILTER | Prevent leakage; separate from residual waste | Sealed drum/container | VEH-HAZ |
| FR-HAZ-PAINT | Preserve container/label; do not mix | Original container + secure cabinet | VEH-HAZ |
| FR-HAZ-SOLVENT | Compatibility and vapor/fire risk controls | Approved sealed package | VEH-HAZ |
| FR-HAZ-AEROSOL | Pressurised; do not pierce or compact | Approved collection container | VEH-HAZ |
| FR-HAZ-GAS | Pressurised; protect valve; no compaction | Cylinder rack / approved handling | VEH-HAZ |
| FR-HAZ-BATTERY | Segregate types; protect lithium terminals | Approved battery box | VEH-HAZ |
| FR-HAZ-EXTING | Pressurised; dedicated route | Secure collection area | VEH-HAZ |
| FR-HAZ-ASB | Use approved dust-tight bagging; specialist handling | EQ-BAG-ASB-UN | VEH-HAZ |
| FR-HAZ-PCBWIN | Specialist hazardous building waste | Protected pallet/rack | VEH-HAZ |
| FR-HAZ-CPWIN | Specialist hazardous building waste | Protected pallet/rack | VEH-HAZ |

## 6.12 Risk and healthcare waste

### FR-RSK-INFECT — Infectious waste

**Rule:** Use approved sealed UN containers. Do not use ordinary bags, bins, cardboard boxes, compactors, or residual-waste containers.

**Equipment:** EQ-RSK-YELLOW-30, EQ-RSK-YELLOW-50.

**Vehicle:** VEH-RISK.

**Treatment:** Controlled specialist incineration or equivalent permitted route.

### FR-RSK-SHARPS — Sharps

**Rule:** Place directly into puncture-resistant sharps containers. Close and place inside an approved larger risk-waste container if required by the collection protocol.

**Equipment:** EQ-RSK-SHARP-2 plus approved outer container.

**Vehicle:** VEH-RISK.

### FR-RSK-PHARM and FR-RSK-CYTO

**Rule:** Keep separately identified and use the operator’s approved packaging and documentation. Do not mix with infectious waste unless the local specialist procedure explicitly permits it.

## 6.13 Tires and other rubber

### FR-RUB-TIRES — Tires

**Accept:** Passenger-car, truck, tractor, trailer, motorcycle, and pneumatic industrial tires, with or without rims where locally accepted.

**Rules**

- Keep tires free of oil, chemicals, soil, stones, and unrelated waste.
- Rims should be identified for separate metal recovery.
- Do not assume other rubber products use the tire-return route.

**Recommended equipment:** Containers, pallets, cages.

**Recommended vehicles:** VEH-LIFT, VEH-HOOK, VEH-FORKBOX.

**Treatment:** Reuse, retreading, material recycling, or energy recovery; landfill is prohibited for discarded tires in Norway.

## 6.14 Textiles, furniture, and bulky materials

### FR-TEX-REUSE / FR-TEX-RECYCLE

**Rule:** Assess condition before disposal. Keep reusable textiles dry and clean. Direct wet, moldy, heavily contaminated, or hazardous-contaminated textiles to a receiver-approved alternative stream.

### FR-BULK-FURN — Furniture and fixtures

**Rule:** Capture reuse potential before disposal. Separate electrical components, batteries, refrigerants, hazardous materials, and removable recyclable components.

**Recommended equipment:** Open container, bulk bag for dismantled components, pallet/cage for reusable items.

**Recommended vehicles:** VEH-LIFT, VEH-HOOK, VEH-CRANE, VEH-FORKBOX.

## 6.15 Aquaculture and fisheries waste

### General controls

Record material composition, metal attachments, copper impregnation/coatings, biofouling/cleaning status, dimensions, weight, whether cut/dismantled, and pickup requirements.

| Fraction | Definition / rule | Recommended equipment | Vehicle |
|---|---|---|---|
| FR-AQU-CAGES | Cage-system components | Container/pallet | VEH-HOOK / VEH-CRANE |
| FR-AQU-ROPE | Ropes and hawsers | Bulk bag/container | VEH-CRANE / VEH-HOOK |
| FR-AQU-FEEDHOSE | PP/PE feed hoses; order should include estimated metres, correct customer name, and facility address | Container/loose controlled load | VEH-CRANE / VEH-HOOK |
| FR-AQU-NET-CU | Copper-impregnated net; controlled specialist route | Container/bag as instructed | Specialist configuration |
| FR-AQU-NET-NCU | Non-copper net; specialist recycling potential | Container/bag as instructed | VEH-CRANE / VEH-HOOK |
| FR-AQU-LICESKIRT | Lice-skirt material | Container/bag as instructed | VEH-CRANE / VEH-HOOK |

---

# 7. Matching logic

## 7.1 The matching chain

WASTR must make recommendations using this exact logical chain:

```text
Waste item/load
  -> hazard and regulatory classification
  -> canonical fraction
  -> quality and preparation state
  -> permitted equipment candidates
  -> fill, volume, density, and gross-weight check
  -> compatible vehicle candidates
  -> site-access and safety constraints
  -> receiver acceptance and downstream route
  -> cost/service-level optimization
  -> final recommended service
```

## 7.2 Fraction-to-equipment matrix

| Fraction group | Primary equipment | Alternative equipment | Key restriction |
|---|---|---|---|
| Food waste | Lidded bin/caddy | Dedicated compactor | Bags/liners and frequency must follow local program |
| Packaged food waste | Dedicated sealed bin/container | Specialist tank/processing system | Receiver must have depackaging capability |
| Used cooking oil | Sealed drum or oil tank | IBC when approved | No drain disposal; liquid compatibility required |
| Paper/cardboard | Covered bin/container, baler | Cage/compactor | Must remain dry |
| Plastic film | 240 L bag stand, baler | Covered container | Keep free of paper/strapping/wood |
| Rigid plastic packaging | Bin/cage/container | Bulk bag | Must be empty/clean and non-hazardous |
| Glass/metal packaging | Sturdy bin/container | Return-point equipment | Not ceramics/window glass/hazardous packaging |
| Metal scrap | Open container/cage/pallet | Hook-lift container | Exclude EE, gas cylinders, hazardous items |
| Clean/mixed wood | Open container | Compactor where suitable | Impregnated wood excluded |
| Impregnated wood | Labeled dedicated hazardous container | Covered storage | Hazardous-waste route only |
| Gypsum | Covered/closed container | Dedicated dry bulk bag | Must stay dry and separate |
| Mineral wool | Container or bulk bags | Covered storage | Exclude EPS/XPS and mixed debris |
| Concrete/soil/brick | Heavy-duty open container | Small container for dense loads | Gross weight is limiting constraint |
| EE waste | Lockable cage/secure area | Pallet/cage | Protect from weather and theft |
| Hazardous liquids | UN drum/IBC | Secure cabinet | Compatibility and declaration required |
| Asbestos | UN dust-tight bag | Specialist sealed package | Trained/specialist route only |
| Infectious waste | UN sealed yellow container | Sharps box inside outer container | No ordinary bins/bags |
| Tires | Container/cage/pallet | Stack under controlled conditions | Keep clean; rims identified |
| Furniture | Open container/pallet | Crane pickup | Assess reuse and EE/hazard components |
| Aquaculture equipment | Container/bulk bag/pallet | Controlled loose load | Record coating, contamination, and dimensions |

## 7.3 Equipment-to-vehicle matrix

| Equipment | Primary vehicle | Secondary vehicle | Notes |
|---|---|---|---|
| 140–1,000 L wheeled bin | VEH-BIN | VEH-COMP | Lift mechanism must match bin standard |
| 240 L bag stand | VEH-BIN | VEH-FORKBOX | Collection process varies by operator |
| 4.5–10 m3 combi container | VEH-LIFT | VEH-COMP | Verify local lifting interface |
| 5–20 m3 lift container | VEH-LIFT | VEH-CRANE for difficult siting | Vehicle access/placement is critical |
| 22–35 m3 hook container | VEH-HOOK | VEH-CRANE for placement only | Respect gross weight/legal payload |
| Bulk bag | VEH-CRANE | VEH-FORKBOX | Must have safe lifting loops and pickup access |
| Pallet/cage | VEH-FORKBOX | VEH-CRANE | Use load securing and pallet compatibility |
| Stationary compactor | VEH-LIFT or VEH-HOOK | — | Depends on detachable-container design |
| Baled material | VEH-FORKBOX | VEH-CRANE | Forklift loading and bale integrity required |
| Drum/IBC hazardous waste | VEH-HAZ | VEH-TANK for liquids | Certified dangerous-goods procedure may apply |
| Risk-waste container | VEH-RISK | — | Dedicated controlled collection |
| Used cooking oil tank | VEH-TANK | VEH-HAZ | Confirm pump/connection requirements |

## 7.4 Weight and density rules

### Core formula

```text
estimated_gross_weight_kg = estimated_volume_m3 * estimated_bulk_density_kg_per_m3
```

### Container feasibility rule

```text
estimated_gross_weight_kg <= equipment.max_total_weight_kg
```

### Safety buffer rule

For an automated recommendation, do not plan to the absolute limit. Use:

```text
recommended_max_load_kg = equipment.max_total_weight_kg * safety_factor
```

Default `safety_factor`:

- 0.80 for uncertain density or mixed construction waste.
- 0.85 for ordinary heavy mineral loads with site-verified material.
- 0.90 for stable, well-characterized recyclable material.
- Local operator configuration may override these defaults.

### Example: dense concrete

A 10 m3 container is not automatically suitable for 10 m3 of concrete. WASTR must calculate expected density, apply the equipment’s maximum total weight, and recommend a smaller fill level or container if the estimated gross weight exceeds limits.

## 7.5 Access feasibility rules

A pickup is feasible only when all required fields have a passing value:

| Constraint | Required validation |
|---|---|
| Road width | Compatible with vehicle width and maneuvering allowance |
| Turning space | Adequate for vehicle length and turning radius |
| Height clearance | No conflict with overhead wires, trees, roofs, bridges, or gates |
| Ground bearing | Suitable for vehicle outrigger/load requirements, especially crane truck |
| Slope | Within vehicle/container handling limit |
| Placement distance | Crane reach or loading method can reach equipment |
| Gate/access control | Driver can access during scheduled time window |
| Pedestrian/public safety | Loading zone can be secured safely |
| Road/bridge limits | Vehicle gross weight and axle limits are allowed |

## 7.6 Mandatory rejection rules

The recommendation engine must reject or route for manual review when:

- Waste is unknown or described only as “mixed” without pictures/details.
- Hazard indicators are present but classification is incomplete.
- A load may contain asbestos, PCB windows, contaminated soil, chemicals, batteries, gas cylinders, refrigerants, or infectious waste.
- Estimated load weight exceeds equipment or vehicle limits.
- Equipment is incompatible with the vehicle’s lifting mechanism.
- Site access is insufficient or unverified for the selected vehicle.
- The selected receiver does not accept the fraction/condition.
- Required declaration/documentation is missing.

---

# 8. Routing and recommendation engine

## 8.1 Recommendation inputs

Minimum required inputs:

```yaml
waste_input:
  item_description: string
  photos: [url]
  source_type: household | office | retail | restaurant | construction | industrial | healthcare | aquaculture | other
  location:
    country: string
    municipality: string
    latitude: number
    longitude: number
  estimated_volume_m3: number
  estimated_weight_kg: number | null
  material_composition: [string]
  packaging_or_product: packaging | product | mixed | unknown
  hazardous_indicators: [string]
  electrical_components: boolean | unknown
  condition:
    clean: boolean | unknown
    dry: boolean | unknown
    contaminated: boolean | unknown
    contamination_notes: string
  site_access:
    road_width_m: number | null
    height_clearance_m: number | null
    crane_reach_m: number | null
    ground_bearing_verified: boolean | null
    access_notes: string
  collection_urgency: same_day | scheduled | recurring
```

## 8.2 Deterministic decision flow

```pseudo
function recommendService(input, localRules, equipmentCatalog, vehicleCatalog):
  safety = classifySafety(input)
  if safety.requires_manual_review:
      return manualReview("Hazard/regulatory uncertainty")

  fraction = classifyFraction(input, localRules)
  if fraction is null:
      return manualReview("Fraction not identified")

  quality = evaluateQuality(input, fraction)
  if quality.rejected:
      return rerouteOrManualReview(quality.reason)

  receiverOptions = findAcceptingReceivers(fraction, quality, input.location)
  if receiverOptions is empty:
      return manualReview("No verified receiver")

  equipmentOptions = findAllowedEquipment(fraction, quality, localRules)
  equipmentOptions = filterByCapacityAndWeight(equipmentOptions, input)
  equipmentOptions = filterBySiteStorageConstraints(equipmentOptions, input.site_access)
  if equipmentOptions is empty:
      return manualReview("No safe equipment match")

  vehicleOptions = findCompatibleVehicles(equipmentOptions, vehicleCatalog)
  vehicleOptions = filterByAccess(vehicleOptions, input.site_access)
  vehicleOptions = filterByWasteTransportClass(vehicleOptions, fraction)
  if vehicleOptions is empty:
      return manualReview("No feasible vehicle match")

  services = combine(fraction, quality, receiverOptions, equipmentOptions, vehicleOptions)
  return rankBySafetyThenComplianceThenReuseThenCostThenDistance(services)
```

## 8.3 Ranking priorities

Rank feasible recommendations in this order:

1. Safety and legal compliance.
2. Receiver acceptance certainty.
3. Waste-hierarchy outcome: reuse > recycling > biological treatment > energy recovery > disposal.
4. Contamination-risk reduction.
5. Equipment and vehicle availability.
6. Operational feasibility and service reliability.
7. Cost and route distance.
8. Carbon/emissions optimization where reliable route data is available.

## 8.4 Output contract

Every generated recommendation must include:

```yaml
recommendation:
  status: approved | conditional | manual_review | rejected
  fraction_id: string
  confidence: high | medium | low
  required_preparation: [string]
  prohibited_materials: [string]
  recommended_equipment:
    equipment_id: string
    quantity: number
    fill_limit_m3: number | null
    fill_limit_kg: number | null
  recommended_vehicle:
    vehicle_id: string
    pickup_method: empty | swap | crane_lift | forklift_load | pump | specialist_collection
  receiver_id: string | null
  treatment_route: reuse | recycle | biological | energy_recovery | controlled_treatment | landfill
  required_documents: [string]
  access_requirements: [string]
  warnings: [string]
  manual_review_reason: string | null
```

---

# 9. Data model

## 9.1 Master entities

| Entity | Purpose | Primary key |
|---|---|---|
| WasteCategory | Top-level classification | `category_id` |
| WasteFraction | Canonical operational stream | `fraction_id` |
| Material | Physical material/substance | `material_id` |
| ItemExample | User-recognizable example | `item_example_id` |
| AcceptanceRule | Location/receiver-specific rule | `acceptance_rule_id` |
| EquipmentType | Equipment master data | `equipment_id` |
| VehicleType | Vehicle master data | `vehicle_id` |
| Receiver | Facility/operator | `receiver_id` |
| ServiceArea | Geographic operating area | `service_area_id` |
| CollectionOrder | Customer pickup job | `collection_order_id` |
| ContainerAsset | Individually tracked equipment | `asset_id` |
| MovementEvent | Custody/transport event | `movement_event_id` |
| WeightTicket | Measured weight record | `weight_ticket_id` |
| TreatmentEvent | Downstream treatment evidence | `treatment_event_id` |
| ComplianceDocument | Declaration, permit, certificate | `document_id` |

## 9.2 WasteFraction schema

```yaml
WasteFraction:
  fraction_id: string
  category_id: string
  display_name_en: string
  display_name_no: string
  synonyms_en: [string]
  synonyms_no: [string]
  handling_class: ordinary | recyclable | hazardous | ee_regulated | healthcare_risk | specialist
  waste_hierarchy_default: reuse | recycle | biological | energy_recovery | controlled_treatment | landfill
  description_short: string
  description_long: string
  accepted_examples: [string]
  prohibited_examples: [string]
  preparation_rules: [string]
  contamination_rules: [string]
  equipment_candidates: [equipment_id]
  vehicle_candidates: [vehicle_id]
  requires_declaration: boolean
  requires_secure_storage: boolean
  requires_weather_protection: boolean
  requires_specialist_carrier: boolean
  default_density_kg_m3: number | null
  density_range_kg_m3:
    min: number | null
    max: number | null
  effective_from: date
  effective_to: date | null
  status: active | deprecated | draft
```

## 9.3 EquipmentType schema

```yaml
EquipmentType:
  equipment_id: string
  display_name_en: string
  display_name_no: string
  equipment_class: bin | bag_stand | bulk_bag | cage | pallet | container | compactor | baler | hazardous_package | risk_package
  volume_l: number | null
  volume_m3: number | null
  length_m: number | null
  width_m: number | null
  height_m: number | null
  self_weight_kg: number | null
  max_total_weight_kg: number | null
  max_payload_kg: number | null
  closed: boolean
  lockable: boolean
  weather_protected: boolean
  un_approved: boolean
  compatible_vehicle_ids: [vehicle_id]
  allowed_fraction_ids: [fraction_id]
  prohibited_fraction_ids: [fraction_id]
  operating_constraints: [string]
  status: active | deprecated | draft
```

## 9.4 VehicleType schema

```yaml
VehicleType:
  vehicle_id: string
  display_name_en: string
  display_name_no: string
  lift_method: bin_lift | lift | hook_lift | crane | forklift | pump | specialist
  compatible_equipment_ids: [equipment_id]
  min_container_volume_m3: number | null
  max_container_volume_m3: number | null
  max_payload_kg: number | null
  waste_classes_allowed: [ordinary, recyclable, hazardous, ee_regulated, healthcare_risk, specialist]
  access_requirements:
    min_road_width_m: number | null
    min_height_clearance_m: number | null
    turning_radius_m: number | null
    max_slope_percent: number | null
  special_requirements: [string]
  status: active | deprecated | draft
```

## 9.5 Location-specific acceptance rule schema

```yaml
AcceptanceRule:
  acceptance_rule_id: string
  fraction_id: string
  receiver_id: string
  service_area_id: string
  accepted: boolean
  accepted_examples: [string]
  prohibited_examples: [string]
  max_contamination_percent: number | null
  max_moisture_percent: number | null
  packaging_required: [string]
  equipment_allowed: [equipment_id]
  vehicle_allowed: [vehicle_id]
  pricing_basis: per_pickup | per_container | per_kg | per_tonne | per_m3 | contract | mixed
  treatment_route: string
  documentation_required: [string]
  valid_from: date
  valid_to: date | null
  validated_by: string
  validation_source_url: string | null
  validation_document_id: string | null
  validation_date: date
  status: active | superseded | draft
```

## 9.6 Traceability event schema

```yaml
MovementEvent:
  movement_event_id: string
  collection_order_id: string
  timestamp: datetime
  event_type: generated | packed | container_sealed | pickup | transferred | weighed | inspected | rejected | treated | certificate_issued
  actor_type: generator | driver | facility_operator | system | auditor
  actor_id: string
  location:
    latitude: number | null
    longitude: number | null
    address: string | null
  fraction_id: string
  container_asset_id: string | null
  estimated_weight_kg: number | null
  measured_weight_kg: number | null
  contamination_status: accepted | conditional | downgraded | rejected | unknown
  evidence_urls: [string]
  notes: string | null
```

---

# 10. API and content schema

## 10.1 Public content page model

Every WASTR fraction content page should be generated from structured data and contain:

```yaml
public_fraction_page:
  fraction_id: string
  title: string
  subtitle: string
  what_it_is: string
  accepted_items: [string]
  not_accepted_items: [string]
  how_to_prepare: [string]
  safety_notice: string | null
  recommended_equipment: [equipment_id]
  collection_options: [string]
  what_happens_next: string
  local_rule_disclaimer: string
  last_validated: date
  service_area_id: string
```

## 10.2 Content-generation constraints

Generated content must:

- Use the local `AcceptanceRule` when available.
- State uncertainty instead of presenting generic guidance as a local guarantee.
- Show prohibited-item warnings prominently for hazardous, EE, risk, and construction waste.
- Avoid claiming a recycling outcome unless a verified local downstream route is recorded.
- Avoid publishing legal/compliance claims without source and validation date.

## 10.3 Example API response

```json
{
  "fraction_id": "FR-MIN-GYPSUM",
  "status": "approved",
  "display_name": "Gypsum",
  "instructions": [
    "Keep gypsum clean, dry, and separate from other construction waste.",
    "Use a covered dedicated container.",
    "Do not place gypsum in residual waste."
  ],
  "equipment": {
    "equipment_id": "EQ-CNT-COMBI-8-C",
    "quantity": 1,
    "fill_limit_kg": 2800
  },
  "vehicle": {
    "vehicle_id": "VEH-LIFT",
    "pickup_method": "swap"
  },
  "requirements": {
    "weather_protection": true,
    "manual_review": false
  },
  "treatment_route": "recycle",
  "last_validated": "2026-09-17"
}
```

---

# 11. Validation and traceability

## 11.1 Minimum traceability chain

```text
Generator
  -> item/fraction classification
  -> packaging/container assignment
  -> collection order
  -> pickup and carrier custody
  -> weighbridge / receiving inspection
  -> transfer or treatment
  -> treatment/recovery evidence
  -> customer reporting
```

## 11.2 Mandatory record fields by risk class

| Waste class | Mandatory fields |
|---|---|
| Ordinary recyclable | Fraction, source, quantity/weight, collection date, receiver, treatment route |
| Construction/mineral | Fraction, project/site, volume/weight, contamination screening, container, receiver |
| EE waste | Fraction, cage/container ID, secure-storage status, pickup, receiver |
| Hazardous waste | Generator, site, fraction, packaging, quantity, hazard details, declaration ID, carrier, receiver, evidence |
| Healthcare/risk waste | Generator, package ID, risk fraction, seal status, pickup, specialist carrier, receiver/treatment evidence |
| Used cooking oil | Generator/site, oil volume, container ID, contamination, pickup, recovery route/certificate |

## 11.3 Contamination workflow

```pseudo
if inspection.contamination == none:
  accept_as_planned()
elif contamination is removable and receiver permits:
  mark_conditional_acceptance()
  add_corrective_action()
elif contamination changes fraction or treatment:
  reroute()
  update_price_and_traceability()
else:
  reject_load()
  create_nonconformance_event()
  notify_generator()
```

## 11.4 Evidence standards

Recommended evidence per collection:

- Before-collection photographs for high-risk/bulky loads.
- Container, bag, pallet, or cage ID.
- Driver confirmation and timestamp.
- GPS coordinates where legally and commercially appropriate.
- Weighbridge ticket.
- Receiving inspection result.
- Waste declaration/consignment data for regulated waste.
- Treatment or recovery certificate when available.

---

# 12. Product UX rules

## 12.1 Customer classification flow

Ask the user simple questions in this order:

1. “What is the item or material?”
2. “Does it contain electricity, a battery, chemicals, oil, paint, gas, or a hazard symbol?”
3. “Is it packaging or the product itself?”
4. “Is it clean and dry?”
5. “How much do you have?”
6. “Can a truck access the pickup point?”
7. “Upload photos for confirmation.”

## 12.2 High-risk UI behavior

For asbestos, hazardous chemicals, gas cylinders, batteries, risk waste, contaminated soil, PCB/chlorinated-paraffin windows, or unknown construction materials:

- Do not show instant unqualified disposal confirmation.
- Display a safety warning.
- Request photos and details.
- Require manual/operator review or a verified specialist pathway.
- Prevent selection of general residual container as a default.

## 12.3 Equipment recommendation UX

Display recommendations in this order:

1. Fraction and safety classification.
2. Preparation steps.
3. Equipment size and quantity.
4. Vehicle/pickup method.
5. Access requirements.
6. Estimated price basis and assumptions.
7. Treatment/recovery outcome.
8. Evidence/document requirements.

## 12.4 Explainability requirement

Every recommendation must be explainable in plain language, for example:

> “We recommend a covered 8 m3 container and a lift truck because gypsum must remain dry, this volume fits your estimated load, and your site access supports lift-truck collection.”

---

# 13. Localisation and versioning

## 13.1 Local rule overlays

Use this file as the canonical baseline, then apply overlays:

```text
Global WASTR taxonomy
  -> Country overlay
    -> State/region overlay
      -> Municipality/service-area overlay
        -> Receiver/operator acceptance rule
          -> Customer contract rule
```

Never overwrite global fraction IDs to implement local variation. Add or update an `AcceptanceRule` linked to the appropriate service area and receiver.

## 13.2 GitHub repository recommendation

Suggested structure:

```text
/docs
  /waste-operations
    wastr-waste-operations-single-source-of-truth.md
    CHANGELOG.md
/data
  waste-fractions.json
  equipment-types.json
  vehicle-types.json
  acceptance-rules/
    norway/
      oslo.json
      trondheim.json
      rio-de-janeiro.json
/schemas
  waste-fraction.schema.json
  equipment-type.schema.json
  acceptance-rule.schema.json
  collection-order.schema.json
```

## 13.3 Versioning rules

- Use semantic versioning: `MAJOR.MINOR.PATCH`.
- **MAJOR:** taxonomy or data-model breaking change.
- **MINOR:** new fraction, equipment type, vehicle type, or non-breaking structured fields.
- **PATCH:** corrections, wording changes, new examples, and validation updates.
- Record every change in `CHANGELOG.md`.
- Never silently edit an acceptance rule in production; end-date the old rule and create a new version.

## 13.4 Review cadence

- High-risk/hazardous rules: at least quarterly and whenever regulation/receiver requirements change.
- Equipment/vehicle data: at least quarterly and whenever fleet/equipment changes.
- Local receiver rules: validate at onboarding and at least every six months.
- Public content: refresh after any acceptance-rule update.

---

# 14. Glossary

| English | Norwegian | Meaning |
|---|---|---|
| Bulk bag | Storsekk | Flexible high-capacity bag |
| Cage | Bur | Metal storage/transport cage |
| Compactor | Komprimator | Equipment that compresses waste |
| Container | Container | Large waste skip/container |
| Contaminated soil | Forurenset masse | Soil requiring assessment/control due to pollutants |
| Food waste | Matavfall | Biodegradable food scraps/material |
| Hazardous waste | Farlig avfall | Waste with environmental/health hazard properties |
| Hook-lift truck | Krokbil | Truck for hook-lift containers |
| Lift truck | Liftbil | Truck for lift containers |
| Mixed waste | Blandet avfall | Unsorted waste accepted only under defined conditions |
| Paper/cardboard/carton | Papp, papir og kartong | Fiber-based recyclable materials |
| Residual waste | Restavfall | Remaining waste after source sorting |
| Risk waste | Risikoavfall | Healthcare waste requiring special handling |
| Source sorting | Kildesortering | Separate waste at generation point |
| Waste fraction | Avfallsfraksjon | Operationally defined waste stream |
| Wheeled bin | Beholder / dunk | Mobile bin, usually 140–1,000 L |

---

# 15. Source and validation notes

## 15.1 Primary source basis

This baseline synthesizes public information from Retura Norway’s waste-sorting directory and collection-equipment pages, plus related Retura equipment/fraction guidance. The source material emphasizes clear labeling, source sorting from generation through disposal, equipment sized to need, and category-specific handling.

## 15.2 Known limits

- Retura is a national brand with local operating companies; exact equipment availability, pickup methods, acceptance criteria, dimensions, fees, and downstream treatment routes can vary.
- Waste classifications and regulations must be verified in the jurisdiction where WASTR operates.
- This document includes Norwegian operational terminology because its initial reference base is Norwegian; it should be localized before use in Brazil or other markets.
- Numerical dimensions and weight limits represent reference values from the initial source base and must be confirmed against the deployed equipment supplier/fleet configuration.

## 15.3 Deployment checklist

Before enabling an operational recommendation in a new location:

- [ ] Create the service area.
- [ ] Register verified receivers and carrier partners.
- [ ] Add receiver-specific acceptance rules for every enabled fraction.
- [ ] Validate equipment and vehicle compatibility.
- [ ] Configure local price basis and surcharge rules.
- [ ] Configure hazardous/risk-waste escalation process.
- [ ] Test access constraints with field operations.
- [ ] Configure traceability and document retention.
- [ ] Obtain legal/compliance review where required.
- [ ] Publish customer-facing content only after validation.

---

## End of document
