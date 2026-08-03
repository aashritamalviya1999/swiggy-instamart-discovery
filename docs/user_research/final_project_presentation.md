# Swiggy Instamart Category Exploration: Growth PM Slide Deck (Visual-Rich Edition)

This artifact details the slide-by-slide layout, visual assets, and content of the final presentation deck compiled for your portfolio submission. It has been updated to replace all raw developer code blocks with **high-fidelity visual diagrams and UI mockups** to ensure maximum readability and professional PM styling.

---

## 🎨 Slide 1: Cover & Strategic Outline
*   **Title**: Category Discovery on Instamart: A Gap and an Opportunity
*   **Subtitle**: A Growth Initiative targeting category expansion among monthly active customers
*   **Layout**: Balanced Cover Frame.
*   **Content Details**:
    *   *Core Issue*: Instamart repeat buyers are anchored to grocery histories, bypassing category exploration.
    *   *Platform Comparison Table*: Compares Instamart (Post-Checkout Add-on), Zepto (Pass widgets), Blinkit (Specialties), and BigBasket (BB Daily Subscription).
    *   *Scale of Opportunity*: ~35M MACs, 75% repeat habits, projected **18% AOV lift** (~₹180M ARR lift pilot).

---

## 💾 Slide 2: Database Ingestion & Storage Architecture
*   **Title**: Database & Ingestion Engine (What Work Was Performed)
*   **Layout**: Dual Column (Left: Functional details | Right: Relational Database Schema Diagram)
*   **Left Column (Storage & Ingestion Details)**:
    *   *Relational DB*: Built structured SQLite tables (`reviews.db`) to store text, sentiments, and ICE priorities.
    *   *Ingestion Scrapers*: Python scripts scrape iTunes XML, Play Store reviews, Reddit communities, and Quora discussions.
    *   *Hinglish normalizer*: Standardizes spelling and translates regional retail slang (e.g. *mehanga* -> expensive) before analysis.
*   **Right Column (Visual Asset)**:
    *   🖼️ **[database_schema_diagram.jpg](file:///C:/Users/sanja/.gemini/antigravity/scratch/swiggy_instamart_discovery/docs/user_research/database_schema_diagram.jpg)**: A visual diagram illustrating the schema relationship between `reviews` and `opportunities` tables.

---

## ⚙️ Slide 3: 7-Agent AI Pipeline Ingestion (The 1-Slider)
*   **Title**: 7-Agent Ingestion Pipeline & Text Vector Clustering (What Was Built)
*   **Layout**: Dual Column (Left: Pipeline & Clustering details | Right: Ingestion Flowchart)
*   **Left Column (Agent & ML Engine Details)**:
    *   *7-Agent Orchestrator*: Coordinates the cleaning, analyzing, and synthesizing steps in Python.
    *   *K-Means Text Clustering*: Vectorizes customer text via TF-IDF embeddings and runs K-Means (K=4) to auto-group feedback subthemes.
    *   *Validation Engine*: Heuristically verifies insights against SQLite data to compute confidence scores.
*   **Right Column (Visual Asset)**:
    *   🖼️ **[n8n_pipeline_workflow.jpg](file:///C:/Users/sanja/.gemini/antigravity/scratch/swiggy_instamart_discovery/docs/user_research/n8n_pipeline_workflow.jpg)**: A clean flowchart representing the automated n8n data processing sequence (Trigger -> Scrape -> Clean -> Cluster -> SQLite DB).

---

## 🔌 Slide 4: FastAPI Gateway & Analytics Layer
*   **Title**: FastAPI Backend REST endpoints & Streamlit dashboard (What Was Built)
*   **Layout**: Dual Column (Left: REST API & Streamlit configurations | Right: Storage Schema Diagram)
*   **Left Column (Interface & API Details)**:
    *   *FastAPI Gateway*: Coded REST endpoints (like `/api/opportunities` and `/api/insights`) returning JSON query results to decouple data from UI.
    *   *Backlog Synchronization*: Roadmapping metrics are calculated in Python and stored in SQLite dynamically.
    *   *Streamlit App*: Renders sentiment pie charts and opportunity prioritization sheets in Swiggy brand colors.
*   **Right Column (Visual Asset)**:
    *   🖼️ **[database_schema_diagram.jpg](file:///C:/Users/sanja/.gemini/antigravity/scratch/swiggy_instamart_discovery/docs/user_research/database_schema_diagram.jpg)**: Displays the database schema highlighting the opportunities prioritization storage.

---

## 📊 Slide 5: Research Validation Matrix
*   **Title**: Target Segment & Validated Pain Points through Primary Research
*   **Layout**: Full-Width Scorecard Table.
*   **Content Details**:
    *   Cross-references your **1,000 reviews AI insights** against transcripts of your **6 customer interviews**, validating findings:
        *   *Habits Loop*: 81% validation (VJ and Rohan reorder milk in 5s).
        *   *Delivery Fee*: 76% validation (Rohan abandons face wash due to fees).
        *   *Specifications*: 83% validation (Priya defaults to Amazon diapers due to missing size charts).
        *   *Verdict*: All core opportunities are **Strongly Validated**.

---

## 👥 Slide 6: The Discovery Loop Problem & HMWs
*   **Title**: The Discovery Loop Problem Statement & Strategic HMWs
*   **Layout**: Dual Column (Left: Root Cause & Workarounds | Right: Growth Opportunity & HMW)
*   **Left Column (Core Problem)**:
    *   *The Problem*: Professionals bypass the homepage catalog, reordering dairy in under 15s.
    *   *Existing Workarounds*: Split-shopping across competitor apps depending on coupons.
*   **Right Column (Strategic HMW & Value)**:
    *   *HMW*: **How might we allow users to append low-consideration auxiliary items to their daily essential carts without triggering additional delivery fees?**
    *   *Business Value*: Increases Average Order Value (AOV), drives margin expansion via high-margin categories, and drives cross-selling with zero CAC.

---

## 📱 Slide 7: Deployed MVP Prototype (3-Min Add-On Window)
*   **Title**: The MVP Solution: Deployed 3-Minute Post-Checkout Add-On Window
*   **Layout**: Dual Column (Left: MVP mechanics | Right: Mobile UI Mockup)
*   **Left Column (MVP Mechanics)**:
    *   *Checkout Simulator*: Placing order simulates active checkout payment completion.
    *   *Visual Countdown Timer*: Triggers an active 3-minute countdown banner immediately.
    *   *0 Delivery Fee Window*: Waives all delivery and handling surcharges on auxiliary items.
    *   *Live MVP Link*: [https://aashritamalviya1999.github.io/swiggy-instamart-discovery/](https://aashritamalviya1999.github.io/swiggy-instamart-discovery/) (Live MVP Prototype Tab)
*   **Right Column (Visual Asset)**:
    *   🖼️ **[mvp_checkout_mockup.jpg](file:///C:/Users/sanja/.gemini/antigravity/scratch/swiggy_instamart_discovery/docs/user_research/mvp_checkout_mockup.jpg)**: A premium dark-mode mobile UI mockup of the checkout screen displaying the countdown timer and recommended items.

---

## 🚀 Slide 8: MVP Operational GTM Rollout Strategy
*   **Title**: MVP Phased Operational Rollout Strategy
*   **Layout**: Dual Column (Left: Phased Roadmap | Right: Operational Safety Gates)
*   **Left Column (GTM Phases)**:
    *   *Phase 1: Shadow Mode (W1-2)*: Track add-on clicks in the background without UI display.
    *   *Phase 2: Operational Buffer Trial (W3-6)*: Pilot in 1 dark store. Set packer lockout rule.
    *   *Phase 3: Tiered City Expansion (W7-12)*: Expand to 10 dark stores.
*   **Right Column (Safety Gates)**:
    *   *Packing Status Gate*: Disable add-on window once packaging has commenced to prevent opening sealed boxes.
    *   *Weight Capacity Gate*: Exclude items >2kg to protect bike delivery capacity.
    *   *Single-Rider Hand-off*: Merge add-ons into one package; no secondary rider.

---

## 📈 Slide 9: GTM Success & Operational Guardrails
*   **Title**: Phased GTM Pilot & Guardrail Success Metrics
*   **Layout**: Dual Column (Left: Indicators | Right: Operational SLA Guardrails)
*   **Left Column (Success Indicators)**:
    *   *North Star*: Cross-Category Discovery Completion Rate. Target: 35% in 30 days.
    *   *Leading indicators*: Timer conversion rate (>25%), platform split churn delta (-5% to Zepto).
*   **Right Column (SLA Guardrails)**:
    *   *Rider Wait Time Delta*: Target: <+30s. If delta exceeds 45s, drop timer window to 2 minutes.
    *   *Packer Picking SLA Delta*: Target: <+15s. Measures picker time to add append item to bag.
    *   *Delivery SLA Breach Rate*: Target: 0% change.

---

## ⚠️ Slide 10: GTM Risk & Operations Matrix
*   **Title**: Go-To-Market Operations & Risk Mitigation Matrix
*   **Layout**: Full-Width Operations Table.
*   **Content Details**:
    *   *Risk 1: Rider delay due to late additions* -> Likelihood: Medium | Impact: High -> *Packer lockout gate*: Disable append options when picker terminal registers order packing has commenced.
    *   *Risk 2: User abuses free delivery for heavy items* -> Likelihood: Low | Impact: Medium -> *Catalog weight limit*: Limit opportunities catalog to items <2kg.
    *   *Risk 3: Add-on items are out of stock* -> Likelihood: High | Impact: Medium -> *Real-time sync*: Query live dark store inventory before displaying add-ons.
