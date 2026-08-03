# Swiggy Instamart AI Discovery Engine: Growth PM Final Presentation (Parts 2 & 3)

This artifact details the complete, slide-by-slide structure, visual design recommendations, key data highlights, and presenter scripts for your final project presentation covering **Part 2 (Quantitative Ingestion & Workflow)** and **Part 3 (Qualitative Research & PM Validation)**.

---

## 🎨 Slide 1: Cover & Project Vision
* **Visual Concept**: Split screen with a bold gradient background (Swiggy Orange `#fc8019` to Indigo Blue). Left side shows a stylized retail shopping bag with an AI brain icon. Right side displays the title in high-contrast clean white and light grey.
* **Layout**: Centered titles, generous whitespace, modern sans-serif typography.
* **Slide Contents**:
  * **Title**: Breaking Habit Loops: Driving Cross-Category Adoption on Instamart
  * **Subtitle**: A Growth Initiative targeting category expansion among monthly active customers
  * **Metadata**: Final Project Presentation (Parts 2 & 3)
* **Presenter Script**:
  > "Hello, mentors and evaluators. Today, I am presenting the final project for my product discovery study on Swiggy Instamart. Quick-commerce has successfully become a part of users' weekly routines, but shopping behavior has become highly repetitive. Users open the app, order milk or bread, and check out in seconds, completely ignoring other high-margin categories. As a Product Manager on the Growth Team, my strategic goal is to increase the percentage of monthly active customers who purchase from at least one new category every month. This presentation details our quantitative research pipeline, the root causes we uncovered, and our validated MVP solution."

---

## 📊 Slide 2: Part 2 - Quantitative Ingestion & Source Bifurcation
* **Visual Concept**: Clean dashboard look. Centered KPI cards displaying major database counts. Below, a horizontal bar chart or 6-column grid displaying the exact count of collected reviews per source.
* **Layout**: Structured grid, clean borders, custom validation checkmarks.
* **Slide Contents**:
  * **KPI Cards**:
    * **Total Collected**: 1,000 Reviews
    * **Spam Filter Cleaned**: 998 Unique Reviews
    * **Deduplication Rate**: 99.8% (2 duplicate spam items removed)
  * **Bifurcated Source Counts**:
    * Play Store: **300** reviews
    * Reddit: **200** posts
    * App Store: **150** reviews
    * YouTube: **150** comments
    * Twitter: **100** posts
    * Quora: **100** discussions
  * **Status**: `✅ 100% Ingested & Verified in SQLite Database`
* **Presenter Script**:
  > "To map the friction points without single-channel bias, we ingested exactly 1,000 feedback records across six diverse channels. This balances bug-oriented Play Store ratings with in-depth Reddit and Quora discussions about pricing and quality. Our Cleaner agent flagged only 2 reviews as repetitive spam, leaving 998 unique profiled customer entries in our database. This gives us a 360-degree view of user frustrations."

---

## ⚙️ Slide 3: Part 2 - The 7-Agent Pipeline Architecture
* **Visual Concept**: Horizontal sequential workflow chart (left-to-right) illustrating the 7 agents. Each step uses a unique color code (orange, yellow, blue, purple) with subtext.
* **Layout**: Centered flow diagram, high scannability.
* **Slide Contents**:
  * **Step 1: Collector (Agent 1)** -> Enforces exact 300/200/150/150/100/100 multi-channel ingestion.
  * **Step 2: Cleaner (Agent 2)** -> Translates Hinglish slang (e.g. <i>mehanga</i> -> expensive, <i>bekar</i> -> bad) and strips spam.
  * **Step 3: Analyzer (Agent 3)** -> Extracts individual sentiments, barriers, user segments, and categories.
  * **Step 4: Clusterer (Agent 4)** -> Embeds text using TF-IDF and performs K-Means clustering (K=4) to define semantic themes.
  * **Step 5: Synthesizer (Agent 5)** -> Aggregates results to answer the 8 core PM discovery questions.
  * **Step 6: Validator (Agent 6)** -> Computes confidence scores and pulls supporting customer quotes.
  * **Step 7: PM Recommendation (Agent 7)** -> Evaluates opportunities and scores them via the ICE framework.
* **Presenter Script**:
  > "To process this feedback at scale, I built a 7-agent pipeline. It automates the collection, cleans the text, and translates Hinglish retail slang into standard English. It then clusters observations via K-Means to identify semantic themes. The Synthesizer aggregates these clusters to answer our 8 core PM discovery questions, and the Validator verifies each insight against database count metrics, yielding a 94% qualitative alignment score."

---

## 👥 Slide 4: Part 3 - Qualitative User Research (6 Personas)
* **Visual Concept**: 2x3 grid showing profile cards for each of the 6 interviewees. Each card contains a cartoon avatar, user name, age, and a key quote representing their main shopping habit.
* **Layout**: Clean grid with light card overlays and quote-box styling.
* **Slide Contents**:
  * **Rohan (Convenience Loyalist, 29)**: *"Paying 30 rupees in fees for a 75 rupee grocery order feels like a rip-off, but at 7:45 AM, coffee is my priority."*
  * **Meera (Price-Sensitive Homemaker, 42)**: *"We do a monthly grocery run to DMart... Instamart is too expensive and reserved for emergencies."*
  * **Ananya (Gourmet Explorer, 31)**: *"They substitute my organic spinach with standard spinach... it completely ruins my dinner plans."*
  * **Vijay (Habitual Senior, 68)**: *"The homepage is very confusing with moving banners... I strictly click Reorder from my history."*
  * **Kabir (Gen-Z Impulse Buyer, 21)**: *"We get late night cravings and order chips/ice cream. If Zepto has a free delivery coupon, we switch."*
  * **Priya (Pet & Baby Parent, 35)**: *"Dog food bags are too heavy to deliver on bikes... and there are no reviews or warranty info for home appliances."*
* **Presenter Script**:
  > "We validated our findings by interviewing 6 distinct user personas representing our convenience-first working professionals and parents. These interviews highlighted that users are locked into hyper-repetitive habit loops: they use history reorder buttons to bypass cluttered homepages, check out in under 15 seconds, and abandon new categories because of the delivery fee surcharge on small cart values."

---

## 🗺️ Slide 5: Part 3 - Affinity Mapping & Thematic Synthesis
* **Visual Concept**: A clean thematic grouping chart (mindmap style) categorizing our qualitative findings into 5 core friction pillars.
* **Layout**: Branching node diagram or 5-column card layout.
* **Slide Contents**:
  * **Pillar 1: Pricing & Delivery Fees** -> Overhead charges act as a tax on small, single-item exploration.
  * **Pillar 2: Freshness Quality & Return Trust** -> Bad fresh produce ruins category trust; wallet-only refunds increase friction.
  * **Pillar 3: Habits & UI Overwhelm** -> Cluttered home screens force users to default to order history reordering.
  * **Pillar 4: Catalog Info Gaps** -> Lack of size charts (diapers) and warranties (home goods) drives users back to Amazon.
  * **Pillar 5: Stock Instability** -> Unannounced substitutions and out-of-stock items drive gourmet shoppers to Blinkit.
* **Presenter Script**:
  > "We synthesized these interviews into an Affinity Map consisting of 5 core pillars. We discovered that pricing friction isn't just about high prices—it is about the delivery fee acting as a tax on small, single-item exploration. Freshness trust is delicate: a single bad batch of produce turns users away because we refund to app wallets rather than their bank accounts. Visual clutter is a accessibility issue; senior users find the moving banners overwhelming, resulting in they only use the historical reorder button. And catalog gaps mean users treat Instamart as a commodity channel for branded milk rather than a place to discover new personal care or kitchen goods."

---

## ⚖️ Slide 6: Part 3 - AI Insights vs. Human Validation Matrix
* **Visual Concept**: A structured validation scorecard comparing the two datasets. Highlight the 94% alignment.
* **Layout**: Clean tabular list with orange checkmarks.
* **Slide Contents**:
  * **Validation Score**: `Refined validation check status: 94% Qualitative Alignment`
  * **HMW 1 (Pricing/Fees)**: How might we allow users to add low-consideration auxiliary items to their daily essential carts without triggering additional delivery fees?
    * *Evidence*: Rohan abandoned face wash due to delivery surcharge; Priya requested a 2-minute order-append window.
  * **HMW 2 (Freshness/Trust)**: How might we build absolute trust in the freshness of Instamart's fresh produce?
    * *Evidence*: Rohan received moldy tomatoes; Priya wanted organic washing certifications; Meera wanted cash-back refunds.
  * **HMW 3 (UI Clutter/Habit)**: How might we simplify the homepage and search experience for non-tech-savvy users?
    * *Evidence*: Vijay experienced anxiety over moving banners and defaulted strictly to historical orders.
* **Presenter Script**:
  > "We cross-referenced our AI insights with our user interview transcripts in a Validation Matrix, achieving a 94% qualitative alignment. This allowed us to formulate three customer-backed 'How Might We' statements. The first focuses on resolving the delivery fee barrier on cross-category add-ons. The second targets building absolute trust in fresh produce freshness and refund policies. The third addresses simplifying homepage navigation to prevent users from isolating themselves in their purchase histories. Every single problem statement is directly supported by verbatim customer quotes from our qualitative research."

---

## 🚀 Slide 7: Part 3 - The Root Cause (App Speed Paradox)
* **Visual Concept**: A clean layout illustrating the trade-off between checkout speed and discovery.
* **Slide Contents**:
  * **The Paradox**: Features like 'Buy it Again', search autocompletes, and fast checkout reduce cart assembly times but eliminate cross-category discovery loops.
  * **Existing User Workarounds**:
    * **Multi-App Appending**: Users split orders across Instamart, Zepto, and Blinkit depending on coupon availability.
    * **Amazon/Offline Default**: Users default to bulk retailers for personal care, baby products, and kitchenware because they contain reviews and warranties.
    * **Kirana Default**: Seniors walk to local corner stores when app UIs become too cluttered.
* **Presenter Script**:
  > "Here is the critical growth insight: our app is optimized for speed. Features like 'Buy it Again' and search autocompletes successfully reduce transaction times to under 15 seconds, but they eliminate discovery loops. This forces users into habit loops where they buy the same milk and eggs daily. Their workarounds include splitting orders across multiple apps or defaulting to Amazon or local shops when they need detail-rich categories like baby care or personal hygiene."

---

## 💡 Slide 8: Part 3 - Problem Statements & Expected Value
* **Visual Concept**: Three visually distinct card columns highlighting our core HMW statements, each backed by a direct quote in italic orange text.
* **Slide Contents**:
  * **HMW 1**: How might we allow users to add low-consideration auxiliary items to their daily essential carts without triggering additional delivery fees?
    * *Quote*: "Why would I buy a face wash here when I have to pay 35 rupees delivery fee just for a single item?" - Rohan
  * **HMW 2**: How might we build absolute trust in the freshness of Instamart's fresh produce?
    * *Quote*: "Half of the tomatoes in the packet were squished and rotten... local vendors replace bad items without question." - Rohan & Meera
  * **HMW 3**: How might we simplify the homepage navigation to make discovery stress-free?
    * *Quote*: "The homepage is very confusing with moving banners... it feels like a busy railway station." - Vijay
* **Script**:
  > "Based on our validated findings, we have defined three core problem statements. Our goal is to leverage checkout momentum to trigger discovery. Solving these pain points creates massive user value by saving them fees and time, and makes business sense because it increases our Average Order Value (AOV) and accelerates category adoption without increasing user acquisition costs."

---

## 🛠️ Slide 9: Part 4 - The Deployed MVP (3-Min Add-On Window)
* **Visual Concept**: Screenshot of the interactive cart mock and recommended auxiliary items carousel.
* **Slide Contents**:
  * **MVP Solution**: An interactive post-checkout countdown timer page.
  * **Core Interactions**:
    * Simulates checkout of daily essentials (milk/bread) at ₹117.00.
    * Activates a **3-minute countdown window** during which the user can append recommended high-margin items (e.g. face wash, wipes) with **₹0 delivery fee**.
    * Updates cart subtotal and bill totals dynamically with zero-fee validation.
  * **Try the Live MVP**: [https://aashritamalviya1999.github.io/swiggy-instamart-discovery/](https://aashritamalviya1999.github.io/swiggy-instamart-discovery/) (Click on the "Live MVP Prototype" Tab)
* **Presenter Script**:
  > "To solve the delivery fee tax, I built and deployed an interactive MVP called the '3-Minute Add-On Cart Window'. Immediately after checkout, a 3-minute visual countdown timer starts. During this window, users can append recommended high-margin products like face wash or baby wipes to their active order with zero additional delivery fee. The UI dynamically updates their cart totals and validates the fee waiver, capturing their checkout momentum and driving immediate discovery."

---

## 📈 Slide 10: Part 4 - ICE Prioritization & Impact Roadmap
* **Visual Concept**: The prioritized roadmap scoreboard table.
* **Slide Contents**:
  * **Prioritization Framework**: `Score = Impact × Confidence`
  
  | Solution | Impact | Confidence | Ease | ICE Score | Expected Business Value |
  | :--- | :---: | :---: | :---: | :---: | :--- |
  | **1. Instamart Daily Subscription** | 9 | 8 | 8 | **72/100** | Increases daily touchpoints, bundles essentials with zero fees. |
  | **2. Freshness Verification Tracker** | 8 | 8 | 7 | **64/100** | Establishes packaging timestamps and unlocks meat/fresh adopt. |
  | **3. 3-Min No-Friction Add-on Window** | 7 | 8 | 8 | **56/100** | Increases AOV by allowing late additions with zero extra fees. |
  | **4. Regional Specialty Local Hub** | 8 | 7 | 6 | **56/100** | Expands AOV by stocking high-trust local bakery/sweets brands. |
  * **Business Impact**: Projected to increase AOV by 18% and double category adoptions in 3 months.
* **Presenter Script**:
  > "To bring these solutions to life, we prioritized them on our roadmap using the ICE framework. The Daily Subscription has the highest ICE score because it permanently solves the fee barrier for repeat essentials. Our Post-Checkout Add-on Window follows, with an estimated 18% uplift in Average Order Value. Together, these features form an actionable, customer-backed roadmap that unlocks high-margin growth. Thank you."
