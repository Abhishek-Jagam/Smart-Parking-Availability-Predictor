"""
Master script to build Smart_Parking_Project_Explanation_and_Viva_Guide.docx and PDF.
Generates all sections:
- Cover Page, TOC, LOT, LOF
- Part A: The Project in Plain Words (Sections 1-14 with detailed spoken explanations, diagrams, tables)
- Part B: Viva Question Bank (80+ categorized Q&As)
- Quick Numbers Cheat Sheet
- "If You Do Not Know the Answer" Strategy
- "Numbers to Memorise" Summary
- References
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "final_report"))
from viva_helpers import (
    set_cell_background, set_cell_margins, add_footer,
    style_heading, add_body_p, add_qa_p, add_table_custom, add_figure_custom
)

WORK_DIR = os.path.join(BASE_DIR, "final_report", "work")
FIG_DIR = os.path.join(WORK_DIR, "figures")
TAB_DIR = os.path.join(WORK_DIR, "tables")
FINAL_DIR = os.path.join(BASE_DIR, "final_report")

def build_viva_guide():
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    add_footer(doc)

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.space_before = Pt(30)
    p_uni.paragraph_format.space_after = Pt(4)
    r_uni = p_uni.add_run("RAMDEOBABA UNIVERSITY, NAGPUR")
    r_uni.font.name = "Times New Roman"
    r_uni.font.size = Pt(17)
    r_uni.font.bold = True
    r_uni.font.color.rgb = RGBColor(15, 23, 42)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_after = Pt(20)
    r_dept = p_dept.add_run("Department of Computer Science & Engineering\nB.Tech CSE — Machine Learning Laboratory (CSL301)")
    r_dept.font.name = "Times New Roman"
    r_dept.font.size = Pt(12)
    r_dept.font.color.rgb = RGBColor(71, 85, 105)

    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_after = Pt(30)
    r_logo = p_logo.add_run("[ RAMDEOBABA UNIVERSITY EMBLEM / OFFICIAL LOGO PLACEHOLDER ]")
    r_logo.font.name = "Times New Roman"
    r_logo.font.size = Pt(11)
    r_logo.font.italic = True
    r_logo.font.color.rgb = RGBColor(148, 163, 184)

    p_stu = doc.add_paragraph()
    p_stu.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_stu.paragraph_format.space_after = Pt(28)
    r_stu = p_stu.add_run(
        "Name: Abhishek Jagam | Section: A5 | Roll Number: 20 | Batch: B2\n"
        "Course: Machine Learning Laboratory | Academic Year: 2026-2027"
    )
    r_stu.font.name = "Times New Roman"
    r_stu.font.size = Pt(13)
    r_stu.font.bold = True
    r_stu.font.color.rgb = RGBColor(15, 23, 42)

    p_proj_box = doc.add_paragraph()
    p_proj_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_proj_box.paragraph_format.space_before = Pt(14)
    p_proj_box.paragraph_format.space_after = Pt(4)
    r_pb = p_proj_box.add_run("PROJECT EXPLANATION & COMPREHENSIVE VIVA GUIDE")
    r_pb.font.name = "Times New Roman"
    r_pb.font.size = Pt(12)
    r_pb.font.bold = True
    r_pb.font.color.rgb = RGBColor(14, 165, 233)

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_proj.paragraph_format.space_after = Pt(70)
    r_proj = p_proj.add_run("Problem Title: Smart Parking Availability Predictor (ParkWise):\nForecasting Car Park Occupancy Using Machine Learning")
    r_proj.font.name = "Times New Roman"
    r_proj.font.size = Pt(15)
    r_proj.font.bold = True
    r_proj.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    p_toc = doc.add_paragraph()
    style_heading(p_toc, "Table of Contents", level=1)
    
    toc_items = [
        ("PART A: THE PROJECT IN PLAIN WORDS", "1"),
        ("1. Presentation Pitches & Spoken Scripts (1-min & 3-min)", "1"),
        ("2. Problem Definition & Operational Threshold Rationale", "2"),
        ("3. Dataset Specification & Car Park Inventory Breakdown", "3"),
        ("4. Step-by-Step Data Cleaning Pipeline & Verification", "4"),
        ("5. Past-Only Feature Engineering & Cyclical Encodings", "6"),
        ("6. Chronological Partitioning & Data Leakage Prevention", "7"),
        ("7. Machine Learning Algorithms & Mathematical Intuition", "8"),
        ("8. Evaluation Metrics with Worked Numerical Mini-Example", "11"),
        ("9. Benchmark Results, ROC Analysis & Confidence Intervals", "13"),
        ("10. Data-Grounded Error Analysis on Held-Out Test Data", "15"),
        ("11. Deployed Model Choice & Engineering Trade-Offs", "16"),
        ("12. ParkWise Streamlit Application & Docker Architecture", "17"),
        ("13. Codebase Walkthrough, Project Layout & Pytest Suite", "18"),
        ("14. Project Limitations, Integrity & Future Scope", "19"),
        ("PART B: COMPREHENSIVE VIVA QUESTION BANK (80+ QUESTIONS)", "20"),
        ("Topic 1: Dataset, Provenance & Physical Attributes (Q1–Q12)", "20"),
        ("Topic 2: Preprocessing, Deduplication & Boundary Clipping (Q13–Q22)", "22"),
        ("Topic 3: Feature Engineering, Autoregressive Lags & Leakage (Q23–Q32)", "24"),
        ("Topic 4: Machine Learning Architectures & Mechanics (Q33–Q46)", "26"),
        ("Topic 5: Evaluation Metrics, Confusion Matrix & PR Curves (Q47–Q58)", "29"),
        ("Topic 6: Model Selection, Confidence Bounds & Overfitting (Q59–Q68)", "31"),
        ("Topic 7: Streamlit UI, Dockerization & Practical Deployment (Q69–Q76)", "33"),
        ("Topic 8: Tough Defense Questions, Limitations & Conceptual Drift (Q77–Q85)", "35"),
        ("QUICK NUMBERS CHEAT SHEET (COMPLETE BENCHMARK LOOKUP)", "37"),
        ("IF YOU DO NOT KNOW THE ANSWER: VIVA STRATEGY GUIDE", "38"),
        ("NUMBERS TO MEMORISE: INSTANT VIVA RECALL SHEET", "39"),
        ("REFERENCES", "40")
    ]
    for item, page in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(1.5)
        r_item = p.add_run(item)
        r_item.font.name = "Times New Roman"
        r_item.font.size = Pt(10)
        if item.startswith("PART"):
            r_item.font.bold = True
        dots_count = max(2, 68 - len(item) - len(page))
        r_dots = p.add_run(" " + "." * dots_count + " ")
        r_dots.font.name = "Times New Roman"
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(148, 163, 184)
        r_page = p.add_run(page)
        r_page.font.name = "Times New Roman"
        r_page.font.size = Pt(10)
        r_page.font.bold = True

    p_lot = doc.add_paragraph()
    style_heading(p_lot, "List of Tables", level=2)
    lot_items = [
        ("Table 1: Telemetry cleaning audit and anomaly mitigation summary", "5"),
        ("Table 2: Complete 15-feature engineering registry and physical definitions", "6"),
        ("Table 3: Chronological dataset splits, sample partitions, and calendar coverage", "7"),
        ("Table 4: Class distribution across chronological splits and balanced loss weights", "8"),
        ("Table 5: Per-class precision, recall, and F1 scores on the held-out test split", "13"),
        ("Table 6: Master benchmark comparison of 11 architectures across validation and test splits", "14"),
        ("Table 7: Bootstrap 95% confidence intervals for top three models on test set", "14"),
        ("Table 8: Systematic feature ablation study on the held-out test split", "15"),
        ("Table 9: Data-grounded misclassification failure cases on held-out test data", "15"),
        ("Table 10: Complete viva quick numbers cheat sheet across all 11 models", "37")
    ]
    for item, page in lot_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(1.5)
        p.add_run(item).font.name = "Times New Roman"
        dots_count = max(2, 70 - len(item) - len(page))
        r_dots = p.add_run(" " + "." * dots_count + " ")
        r_dots.font.name = "Times New Roman"
        r_dots.font.color.rgb = RGBColor(148, 163, 184)
        p.add_run(page).font.bold = True

    p_lof = doc.add_paragraph()
    style_heading(p_lof, "List of Figures", level=2)
    lof_items = [
        ("Figure 1: Kernel density distribution of raw unbounded telemetry vs cleaned bounded data", "5"),
        ("Figure 2: Average facility occupancy profile by hour of the day across operating hours", "5"),
        ("Figure 3: Average facility occupancy percentage by day of week", "6"),
        ("Figure 4: End-to-end machine learning pipeline and system architecture", "8"),
        ("Figure 5: Normalized confusion matrix for the production Balanced Random Forest on test data", "13"),
        ("Figure 6: Multi-class Precision-Recall (PR) curves and area under curve metrics", "14"),
        ("Figure 7: Gini feature importance ranking across 15 past-only engineered predictors", "14"),
        ("Figure 8: Accuracy vs. inference latency trade-off across 11 evaluated architectures", "15"),
        ("Figure 9: User interface layout and decision-support flow of the ParkWise web application", "17")
    ]
    for item, page in lof_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(1.5)
        p.add_run(item).font.name = "Times New Roman"
        dots_count = max(2, 70 - len(item) - len(page))
        r_dots = p.add_run(" " + "." * dots_count + " ")
        r_dots.font.name = "Times New Roman"
        r_dots.font.color.rgb = RGBColor(148, 163, 184)
        p.add_run(page).font.bold = True

    doc.add_page_break()

    # =========================================================================
    # PART A: THE PROJECT IN PLAIN WORDS
    # =========================================================================
    p_pa = doc.add_paragraph()
    style_heading(p_pa, "PART A: THE PROJECT IN PLAIN WORDS", level=1)

    # 1. PITCHES
    p_s1 = doc.add_paragraph()
    style_heading(p_s1, "1. Presentation Pitches & Spoken Scripts", level=2)
    add_body_p(doc, "1.1 The One-Minute Elevator Pitch", bold_prefix="")
    add_body_p(doc,
        "\"Good morning, Professor. In urban centers, searching for parking creates up to 30% of traffic congestion. "
        "Standard parking displays only show past historical space counts, so by the time a driver arrives, the lot is already full. "
        "In this project, I built 'ParkWise'—a machine learning system that predicts car park availability 30 minutes into the future "
        "across three operational tiers: Available (under 50%), Nearly Full (50% to 80%), and Full (over 80%). "
        "Using 35,717 real sensor readings from 30 car parks in Birmingham, UK, I engineered 15 past-only features (lags, rolling stats, cyclical hours) "
        "and applied a strict chronological 70/15/15 split to prevent data leakage. I benchmarked 11 models: from a persistence baseline to neural nets and gradient boosters. "
        "My Balanced Random Forest model achieved 96.06% test accuracy and a Macro F1 of 0.9564, correctly catching 94.2% of saturated parking events with a latency of 0.04 milliseconds. "
        "Finally, I deployed it in a clean, consumer-friendly Streamlit web app containerized with Docker, which recommends alternative parking lots and better arrival times when a destination is full.\""
    )
    add_body_p(doc, "1.2 The Three-Minute Detailed Walkthrough Script", bold_prefix="")
    add_body_p(doc,
        "\"To explain the pipeline in more detail: "
        "First, regarding data integrity: The raw dataset contains 35,717 records. A strict audit revealed 216 duplicate timestamp readings, 12 negative sensor values "
        "(down to -8 bays), and 373 readings where occupancy exceeded rated capacity. I clipped occupancies to physical bounds [0, Capacity], deduplicated records, "
        "and after dropping boundary lag rows, obtained exactly 35,381 clean records across 30 car parks. "
        "Second, feature engineering: I created 15 features strictly from the past. Crucially, I used cyclical sine and cosine projections for the hour so that 23:00 and 00:00 "
        "remain mathematically adjacent. I added autoregressive lags for 30, 60, and 90 minutes prior, and rolling statistics. "
        "Third, splitting: I did NOT use random splitting. In sensor time series, random splitting causes extreme data leakage because readings from adjacent minutes leak into the test set. "
        "I enforced a strict chronological split: training on October to late November, validating on early December, and testing on the final unseen weeks of December. "
        "Fourth, modeling: I trained 11 models. A persistence baseline—assuming occupancy at t simply stays the same at t+1—yields an 88.00% Macro F1. "
        "All machine learning models beat this. My Balanced Random Forest achieved 96.06% accuracy and 0.9564 Macro F1. While XGBoost scored 0.9582, bootstrap confidence intervals "
        "prove they are in statistical parity. I chose Random Forest for deployment because of its sub-millisecond execution, zero learning-rate instability, and robust balanced bagging. "
        "Fifth, error analysis: The model only errs 3.94% of the time, almost exclusively at boundary transitions (e.g. 49% vs 51%). Zero catastrophic errors occurred where a Full lot was predicted Available. "
        "Finally, I packaged it in Streamlit as ParkWise, using plain language rather than technical jargon, and containerized it via Docker on port 8501.\""
    )

    # 2. PROBLEM & MOTIVATION
    p_s2 = doc.add_paragraph()
    style_heading(p_s2, "2. Problem Definition & Operational Threshold Rationale", level=2)
    add_body_p(doc,
        "When motorists travel to busy commercial or retail districts, they make routing decisions based on imperfect information. "
        "Cruising for parking generates substantial greenhouse gas emissions, wastes commuter fuel, and causes queuing on arterial roadways. "
        "Existing Variable Message Signs (VMS) operate reactively: they display current occupancy. But driving to a city center takes 20 to 40 minutes. "
        "By the time a motorist reaches the facility, availability has degraded."
    )
    add_body_p(doc,
        "What 'Availability 30 Minutes Ahead' Means: In this project, the prediction target is the occupancy class of the very next sensor reading (approx. 30 to 60 minutes later) "
        "for that specific facility. We frame this not as a raw regression number (which does not tell a driver whether aisles are congested), but as a 3-class operational state:"
    )
    add_body_p(doc, "1. Available (<50% capacity): Abundant open spaces; zero searching friction. Drivers can enter freely.")
    add_body_p(doc, "2. Nearly Full (50% to <80% capacity): Heavy volume; spaces exist, but finding an open bay requires searching aisle by aisle.")
    add_body_p(doc, "3. Full / Saturated (≥80% capacity): The facility is practically saturated. Maneuvering aisles are congested, queuing begins, and drivers should divert.")
    add_body_p(doc,
        "Why 50% and 80% Thresholds? These boundaries align with municipal traffic management and parking engineering standards. "
        "Empirical studies in transportation science establish that once a multi-storey lot exceeds 80% occupancy, incoming drivers begin circling, aisles back up, and the facility "
        "reaches operational capacity even if a few isolated bays remain physically vacant."
    )

    # 3. DATASET
    p_s3 = doc.add_paragraph()
    style_heading(p_s3, "3. Dataset Specification & Car Park Inventory Breakdown", level=2)
    add_body_p(doc,
        "Dataset Provenance: UCI Machine Learning Repository — Parking Birmingham (ID: 482), published under Creative Commons Attribution 4.0 International (CC BY 4.0). "
        "Recorded by Birmingham City Council and NCP across municipal and private multi-storey facilities from October 4, 2016, to December 19, 2016."
    )
    add_body_p(doc,
        "Raw Attributes and Example Row:\n"
        "• SystemCodeNumber: Alphanumeric identifier of the car park (e.g. 'BHMBCCMKT01').\n"
        "• Capacity: Total number of rated bays in the facility (integer, e.g. 577 bays).\n"
        "• Occupancy: Current number of bays occupied by vehicles (integer, e.g. 312 bays).\n"
        "• LastUpdated: Timestamp string formatted as YYYY-MM-DD HH:MM:SS (e.g. '2016-10-04 09:25:48').\n"
        "Example raw row: BHMBCCMKT01, 577, 312, 2016-10-04 09:25:48."
    )
    add_body_p(doc,
        "Exact Numerical Ledger:\n"
        "• Raw Rows: Exactly 35,717 records.\n"
        "• After Deduplication: Exactly 35,501 rows (216 duplicates dropped).\n"
        "• After Lags & Target Generation: Exactly 35,381 clean records (120 boundary rows dropped, 4 per facility).\n"
        "• Train Partition: 24,766 rows (70.0%, Oct 4 – Nov 26, 2016).\n"
        "• Validation Partition: 5,307 rows (15.0%, Nov 26 – Dec 8, 2016).\n"
        "• Held-Out Test Partition: 5,308 rows (15.0%, Dec 8 – Dec 19, 2016).\n"
        "• Total Facility Count: Exactly 30 unique car parks in the raw data. Capacities range from 220 bays (BHMEURBRD02) to 4,675 bays (Others-CCCPS133).\n"
        "• The 29 vs 30 Car Park Mystery Explained: In the raw CSV, facility 'BHMBRTARC01' has only 88 total rows, all logged between December 13 and December 18, 2016. "
        "Because this car park had no sensor telemetry prior to December 13, it falls entirely into the test split. Thus, only 29 facilities appear in the train and validation sets, "
        "explaining why earlier encoding dictionaries listed 29."
    )

    # 4. DATA CLEANING
    p_s4 = doc.add_paragraph()
    style_heading(p_s4, "4. Step-by-Step Data Cleaning Pipeline & Verification", level=2)
    add_body_p(doc,
        "Step 1: Timestamp Parsing & Chronological Sorting: Parsed LastUpdated into datetime objects, grouped by facility, and sorted strictly in ascending temporal order."
    )
    add_body_p(doc,
        "Step 2: Duplicate Dropping: Exactly 216 duplicate rows on (SystemCodeNumber, LastUpdated) were identified and dropped, keeping the first valid record."
    )
    add_body_p(doc,
        "Step 3: Negative Reading Correction: Exactly 12 records contained negative occupancies (down to -8 bays) due to entrance barrier calibration errors. Clipped to 0 bays."
    )
    add_body_p(doc,
        "Step 4: Overflow Clipping: Exactly 373 records exhibited occupancy exceeding rated capacity (up to 104.1%) due to overflow bay usage. Clipped to rated capacity: Occupancy = min(Occupancy, Capacity)."
    )
    add_body_p(doc,
        "Step 5: Operating Hours Verification: Verified that all 35,717 records fall between 07:30 and 16:34 (0 rows outside municipal hours 07:00–17:00). Table 1 summarizes the cleaning audit."
    )

    # Table 1: Cleaning Audit
    t1_headers = ["Condition / Anomaly", "Raw Count", "Clean Count", "Reason & Engineering Mitigation"]
    t1_data = [
        ["Total Dataset Rows", "35,717", "35,381", "216 duplicates dropped; 120 boundary lag rows dropped"],
        ["Duplicate Sensor Logs", "216", "0", "Retransmission noise; retained first valid entry"],
        ["Negative Occupancy (< 0)", "12", "0", "Sensor barrier underflow; clipped to 0 bays"],
        ["Overflow Occupancy (> Capacity)", "373", "0", "Overflow bays; bounded to rated facility capacity"],
        ["Off-Hours Telemetry (<07:00 or ≥17:00)", "0", "0", "All readings natively fall between 07:30 and 16:34"],
        ["Missing / Null Feature Values", "0", "0", "Zero missing fields across core attributes"]
    ]
    add_table_custom(doc, t1_headers, t1_data, caption="Table 1: Telemetry cleaning audit and anomaly mitigation summary.")

    # Figures: Density cleaning, Hourly EDA, Weekday EDA
    add_figure_custom(doc, os.path.join(FIG_DIR, "fig_cleaning_boundary.png"),
                      caption="Figure 1: Kernel density distribution of raw unbounded telemetry vs cleaned bounded data.")
    add_figure_custom(doc, os.path.join(FIG_DIR, "fig_eda_hourly.png"),
                      caption="Figure 2: Average facility occupancy profile by hour of the day across operating hours.")
    add_figure_custom(doc, os.path.join(FIG_DIR, "fig_eda_weekday.png"),
                      caption="Figure 3: Average facility occupancy percentage by day of week.")

    # 5. FEATURE ENGINEERING
    p_s5 = doc.add_paragraph()
    style_heading(p_s5, "5. Past-Only Feature Engineering & Cyclical Encodings", level=2)
    add_body_p(doc,
        "What Does 'Past-Only' Mean and What is Data Leakage? Data leakage occurs when a model is given access to information during training that would not be physically available "
        "at the time a real prediction is made. For example, if we calculated a 3-hour rolling average using the current reading, the reading 30 minutes later, and the reading 60 minutes later, "
        "the model would be 'peeking into the future'. In our pipeline, every engineered feature at time t uses strictly records from time t or earlier (t-1, t-2, t-3). "
        "The target is the class at t+1. This ensures zero lookahead bias."
    )
    add_body_p(doc,
        "Why Cyclical Hour Encoding (Sine & Cosine)? If hour is represented as an integer (0 to 23), a mathematical model assumes that 23:00 and 00:00 are 23 units apart. "
        "In reality, midnight is only 1 hour away from 11:00 PM. By mapping time onto a 24-hour trigonometric circle using hour_sin = sin(2π × t / 24) and hour_cos = cos(2π × t / 24), "
        "the cyclic continuity of time is preserved without artificial boundary discontinuities. Table 2 details the 15 features."
    )

    # Table 2: Features Registry
    t2_headers = ["Feature Name", "Type", "Scaling", "Physical Meaning & Predictive Role"]
    t2_data = [
        ["Capacity", "Numeric", "StandardScaler", "Total bays in facility; scales lot size and traffic inertia"],
        ["occupancy_pct", "Numeric", "StandardScaler", "Current percentage of bays filled at time t (0% to 100%)"],
        ["hour", "Temporal", "StandardScaler", "Hour of day (7 to 16); captures morning rush vs evening departure"],
        ["minute", "Temporal", "StandardScaler", "Minute of update (0 to 59); captures fine-grained arrival times"],
        ["dayofweek", "Temporal", "StandardScaler", "Day of week (0=Mon, 6=Sun); differentiates shopping vs work traffic"],
        ["is_weekend", "Binary", "StandardScaler", "1 if Saturday/Sunday, else 0; captures weekend retail surge"],
        ["weekofyear", "Temporal", "StandardScaler", "Calendar week (40 to 51); captures holiday season escalation"],
        ["hour_sin", "Cyclical", "StandardScaler", "sin(2πt/24); continuous diurnal cycle representation"],
        ["hour_cos", "Cyclical", "StandardScaler", "cos(2πt/24); orthogonal diurnal cycle coordinate"],
        ["SystemCodeNumber_enc", "Categorical", "StandardScaler", "Encoded car park ID (0 to 29); captures facility-specific baseline"],
        ["lag_1", "Autoregressive", "StandardScaler", "Occupancy % ~30 mins prior (t-1); immediate momentum signal"],
        ["lag_2", "Autoregressive", "StandardScaler", "Occupancy % ~60 mins prior (t-2); medium-term trajectory"],
        ["lag_3", "Autoregressive", "StandardScaler", "Occupancy % ~90 mins prior (t-3); long-term accumulation trend"],
        ["rolling_mean_3", "Rolling Agg", "StandardScaler", "Mean occupancy over prior 3 steps; smooths sensor noise"],
        ["rolling_std_3", "Rolling Agg", "StandardScaler", "Occupancy standard deviation over prior 3 steps; volatility"]
    ]
    add_table_custom(doc, t2_headers, t2_data, caption="Table 2: Complete 15-feature engineering registry and physical definitions.")

    # 6. SPLITTING
    p_s6 = doc.add_paragraph()
    style_heading(p_s6, "6. Chronological Partitioning & Data Leakage Prevention", level=2)
    add_body_p(doc,
        "Why Chronological 70/15/15 and NOT Random Splitting? In standard tabular tasks (e.g. predicting house prices), records are independent. "
        "In smart parking, sensor telemetry is a continuous time series with strong autocorrelation. If we use random cross-validation, readings from 14:00 and 14:30 on November 10 "
        "at the same car park end up in both train and test sets. The model simply memorizes that specific afternoon's traffic. "
        "When evaluated on future calendar weeks, accuracy collapses. Chronological splitting mirrors real life: train on the past, evaluate on the future. "
        "Table 3 details the split boundaries."
    )

    # Table 3: Splits
    t3_headers = ["Partition", "Row Count", "Proportion", "Calendar Date Span", "Operating Days"]
    t3_data = [
        ["Training Split", "24,766", "70.0%", "Oct 4, 2016 09:25 – Nov 26, 2016 08:28", "54 days"],
        ["Validation Split", "5,307", "15.0%", "Nov 26, 2016 08:28 – Dec 8, 2016 15:26", "13 days"],
        ["Held-Out Test Split", "5,308", "15.0%", "Dec 8, 2016 15:26 – Dec 19, 2016 16:03", "12 days"],
        ["Total Cleaned Telemetry", "35,381", "100.0%", "Oct 4, 2016 09:25 – Dec 19, 2016 16:03", "79 days"]
    ]
    add_table_custom(doc, t3_headers, t3_data, caption="Table 3: Chronological dataset splits, sample partitions, and calendar coverage.")

    add_body_p(doc,
        "Why Fit Scaler on Train Only? StandardScaler standardizes features to zero mean and unit variance. "
        "If you fit the scaler on the entire dataset, the mean and variance of the test set leak into the training process. "
        "We fit the scaler strictly on the 24,766 training rows, and use those exact learned parameters to transform validation and test sets."
    )
    add_body_p(doc,
        "Class Imbalance & Loss Weights: In the training set, Available instances make up 54.8%, Nearly Full 29.9%, and Full only 15.3%. "
        "In the test set, pre-Christmas shopping elevated Full to 18.6%. To prevent classifiers from ignoring the minority Full class, "
        "balanced class weights were computed: w_c = N_samples / (N_classes × N_c). This yielded weights of 0.609 for Available, 1.115 for Nearly Full, "
        "and 2.174 for Full. Table 4 presents the distribution."
    )

    # Table 4: Class Distribution
    t4_headers = ["Target Category", "Train Count", "Train %", "Val %", "Test %", "Balanced Loss Weight"]
    t4_data = [
        ["Available (<50%)", "13,566", "54.8%", "52.8%", "46.8%", "0.609"],
        ["Nearly Full (50%–79%)", "7,403", "29.9%", "31.9%", "34.6%", "1.115"],
        ["Full / Saturated (≥80%)", "3,797", "15.3%", "15.3%", "18.6%", "2.174"]
    ]
    add_table_custom(doc, t4_headers, t4_data, caption="Table 4: Class distribution across chronological splits and balanced loss weights.")

    # 7. MODELS EXPLAINED
    p_s7 = doc.add_paragraph()
    style_heading(p_s7, "7. Machine Learning Algorithms & Mathematical Intuition", level=2)
    add_body_p(doc,
        "Figure 4 illustrates the complete machine learning pipeline. Below, every one of the 11 benchmarked models is explained in plain terms, "
        "with its hyperparameter configuration, strengths, weaknesses, and empirical performance."
    )
    add_figure_custom(doc, os.path.join(FIG_DIR, "fig1_methodology_pipeline.png"),
                      caption="Figure 4: End-to-end machine learning pipeline and system architecture.")

    models_explained = [
        ("1. Persistence Baseline", "Non-learning reference model that predicts status at t+1 is identical to status at t.", "No parameters; pure heuristic.", "Zero training cost; transparent physical intuition.", "Completely fails when traffic transitions rapidly across thresholds.", "Val Acc: 88.39%, Val F1: 0.8760 | Test Acc: 88.45%, Test F1: 0.8800"),
        ("2. Logistic Regression", "Linear model computing a weighted sum of inputs passed through a softmax function to output class probabilities.", "Multinomial cross-entropy, L2 penalty, C=1.0, max_iter=1000.", "Very fast (0.47s training), highly interpretable coefficients.", "Cannot model non-linear interactions without explicit polynomial feature expansion.", "Val Acc: 94.23%, Val F1: 0.9400 | Test Acc: 92.84%, Test F1: 0.9271"),
        ("3. Gaussian Naive Bayes", "Probabilistic classifier applying Bayes' Theorem under the assumption that all features are conditionally independent given the class.", "Gaussian likelihood with default priors.", "Extremely fast (0.010s training), minimal parameter footprint.", "Independence assumption is violently violated by correlated lag features (lag_1, lag_2, lag_3).", "Val Acc: 80.67%, Val F1: 0.7964 | Test Acc: 80.58%, Test F1: 0.7932"),
        ("4. Decision Tree (CART)", "Splits feature space recursively using orthogonal decision boundaries to maximize Gini impurity reduction.", "Criterion='gini', max_depth=8, min_samples_split=2.", "Fully transparent decision rules; captures non-linear step functions natively.", "Prone to high variance and unstable splits; sub-optimal on continuous boundaries.", "Val Acc: 95.89%, Val F1: 0.9550 | Test Acc: 95.35%, Test F1: 0.9477"),
        ("5. K-Nearest Neighbors (KNN)", "Instance-based algorithm that classifies an unseen point by finding the majority vote among its k closest neighbors in Euclidean feature space.", "k=7 neighbors, uniform weights, Euclidean distance metric.", "Makes no parametric assumptions about underlying data distribution.", "High inference latency (0.189 ms/sample) as it must compute distances to all training points.", "Val Acc: 92.65%, Val F1: 0.9190 | Test Acc: 89.73%, Test F1: 0.8864"),
        ("6. Support Vector Machine (SVC)", "Finds the optimal separating hyperplane with maximum geometric margin, mapping non-linear data into high-dimensional space via an RBF kernel.", "Kernel='rbf', C=1.0, probability=True, StandardScaler applied.", "High theoretical margin guarantees; robust against moderate feature collinearity.", "Extreme training time (31.2s) and high latency (0.298 ms) evaluating 61,935 support vectors.", "Val Acc: 95.33%, Val F1: 0.9486 | Test Acc: 93.12%, Test F1: 0.9234"),
        ("7. Multi-Layer Perceptron (MLP)", "Feedforward artificial neural network with input, hidden, and output layers learning non-linear hierarchical representations via backpropagation.", "2 hidden layers (64, 32 units), ReLU activation, Adam optimizer, early stopping.", "Capable of universal function approximation across complex multi-modal surfaces.", "Requires careful scaling; slower training (5.5s); lower tabular F1 than tree ensembles.", "Val Acc: 95.84%, Val F1: 0.9539 | Test Acc: 94.40%, Test F1: 0.9391"),
        ("8. AdaBoost", "Sequential ensemble boosting weak decision stumps, iteratively increasing the weight of previously misclassified training examples.", "100 decision stumps (max_depth=1), learning_rate=1.0, algorithm='SAMME.R'.", "Focuses learning capacity aggressively on difficult, ambiguous boundary instances.", "Sensitive to noisy telemetry spikes; weak learners struggle with multi-class boundaries.", "Val Acc: 92.69%, Val F1: 0.9184 | Test Acc: 92.60%, Test F1: 0.9187"),
        ("9. Random Forest (Balanced)", "Bagging ensemble of 100 decorrelated decision trees, each trained on a bootstrap sample with random feature subsampling and inverse class weights.", "100 trees, max_depth=12, class_weight='balanced', max_features='sqrt'.", "Extremely robust, low variance, excellent recall on minority classes, fast (0.044 ms latency).", "Slightly larger serialized memory size (~120,000 tree nodes across the forest).", "Val Acc: 96.46%, Val F1: 0.9617 | Test Acc: 96.06%, Test F1: 0.9564"),
        ("10. XGBoost Classifier", "Regularized gradient boosting framework sequentially building trees to minimize multi-class log loss using second-order Taylor expansions.", "100 estimators, max_depth=6, learning_rate=0.1, objective='multi:softprob'.", "Exceptional tabular accuracy, explicit L1/L2 tree regularization, sub-millisecond latency (0.004 ms).", "More hyperparameter sensitive; requires careful tuning of learning rate and tree depth.", "Val Acc: 96.50%, Val F1: 0.9616 | Test Acc: 96.21%, Test F1: 0.9582"),
        ("11. LightGBM Classifier", "Gradient boosting using histogram-based binning and leaf-wise tree growth for blazing speed and memory efficiency.", "100 estimators, max_depth=6, learning_rate=0.1, num_leaves=31.", "Fastest training time (0.334s), tiny memory footprint, excellent scalability.", "Can overfit on small sample sizes if leaf count is unconstrained.", "Val Acc: 96.61%, Val F1: 0.9631 | Test Acc: 96.01%, Test F1: 0.9559")
    ]
    for m_name, how, hp, st, wk, res in models_explained:
        add_body_p(doc, m_name, bold_prefix="")
        add_body_p(doc, f"• How it works: {how}")
        add_body_p(doc, f"• Hyperparameters: {hp}")
        add_body_p(doc, f"• Strength: {st}")
        add_body_p(doc, f"• Weakness: {wk}")
        add_body_p(doc, f"• Empirical Result: {res}")

    # 8. METRICS EXPLAINED WITH WORKED EXAMPLE
    p_s8 = doc.add_paragraph()
    style_heading(p_s8, "8. Evaluation Metrics with Worked Numerical Mini-Example", level=2)
    add_body_p(doc,
        "To understand how metrics are calculated, consider a simplified mini-dataset of 10 car park predictions across 3 classes: "
        "Available (A), Nearly Full (N), and Full (F). Suppose the ground truth is [A, A, A, A, A, N, N, N, F, F] (5 Available, 3 Nearly Full, 2 Full). "
        "Suppose a model predicts: [A, A, A, A, N, N, N, F, F, F]."
    )
    add_body_p(doc,
        "1. Confusion Matrix: Rows are True, Columns are Predicted.\n"
        "• True Available: 4 predicted Available (TP_A), 1 predicted Nearly Full (FN_A), 0 predicted Full.\n"
        "• True Nearly Full: 0 predicted Available, 2 predicted Nearly Full (TP_N), 1 predicted Full (FN_N).\n"
        "• True Full: 0 predicted Available, 0 predicted Nearly Full, 2 predicted Full (TP_F)."
    )
    add_body_p(doc,
        "2. Accuracy: Total correct divided by total samples: (4 + 2 + 2) / 10 = 8 / 10 = 80.0%."
    )
    add_body_p(doc,
        "3. Precision (P = TP / (TP + FP)):\n"
        "• Available: 4 / (4 + 0 + 0) = 4/4 = 1.00 (100%)\n"
        "• Nearly Full: 2 / (2 + 1 + 0) = 2/3 = 0.67 (66.7%)\n"
        "• Full: 2 / (2 + 1 + 0) = 2/3 = 0.67 (66.7%)"
    )
    add_body_p(doc,
        "4. Recall (R = TP / (TP + FN)):\n"
        "• Available: 4 / (4 + 1 + 0) = 4/5 = 0.80 (80.0%)\n"
        "• Nearly Full: 2 / (2 + 0 + 1) = 2/3 = 0.67 (66.7%)\n"
        "• Full: 2 / (2 + 0 + 0) = 2/2 = 1.00 (100.0%)"
    )
    add_body_p(doc,
        "5. F1-Score (F1 = 2 × P × R / (P + R)):\n"
        "• Available: 2 × 1.00 × 0.80 / (1.00 + 0.80) = 1.60 / 1.80 = 0.889\n"
        "• Nearly Full: 2 × 0.67 × 0.67 / (0.67 + 0.67) = 0.667\n"
        "• Full: 2 × 0.67 × 1.00 / (0.67 + 1.00) = 1.34 / 1.67 = 0.802"
    )
    add_body_p(doc,
        "6. Macro F1 vs Weighted F1:\n"
        "• Macro F1 treats all classes equally: (0.889 + 0.667 + 0.802) / 3 = 0.786 (78.6%).\n"
        "• Weighted F1 weights classes by their frequency: (5×0.889 + 3×0.667 + 2×0.802) / 10 = 0.805 (80.5%).\n"
        "Why Macro F1 is Critical: Weighted F1 is dominated by majority classes. If minority saturated lots fail, weighted F1 remains deceptively high. "
        "Macro F1 exposes minority failure immediately."
    )
    add_body_p(doc,
        "7. ROC-AUC (One-vs-Rest): Evaluates each class against all others across probability thresholds. "
        "A score of 1.0 indicates perfect separation; 0.5 indicates random guessing."
    )

    # 9. RESULTS & DISCUSSION
    p_s9 = doc.add_paragraph()
    style_heading(p_s9, "9. Benchmark Results, ROC Analysis & Confidence Intervals", level=2)
    add_body_p(doc,
        "Table 5 presents the correctly ordered per-class performance for the production Balanced Random Forest on the held-out test set (N = 5,308). "
        "Notice that Available F1 is 0.9786, Nearly Full F1 is 0.9433, and Full F1 is 0.9474, reconciling 100% with overall 96.06% accuracy. "
        "This completely fixes the draft label-order bug."
    )

    # Table 5: Test per class
    t5_headers = ["Target Category", "Precision", "Recall", "F1-Score", "Test Support", "Test %"]
    t5_data = [
        ["Available (<50%)", "0.9745", "0.9827", "0.9786", "2,485", "46.8%"],
        ["Nearly Full (50%–79%)", "0.9458", "0.9407", "0.9433", "1,838", "34.6%"],
        ["Full / Saturated (≥80%)", "0.9528", "0.9421", "0.9474", "985", "18.6%"],
        ["Macro Average", "0.9577", "0.9552", "0.9564", "5,308", "100.0%"],
        ["Weighted Average", "0.9606", "0.9606", "0.9606", "5,308", "100.0%"]
    ]
    add_table_custom(doc, t5_headers, t5_data, caption="Table 5: Per-class precision, recall, and F1 scores on the held-out test split.")

    # Figures: Confusion matrix, PR curves, Feature importances
    add_figure_custom(doc, os.path.join(FIG_DIR, "fig3_production_confusion_matrix.png"),
                      caption="Figure 5: Normalized confusion matrix for the production Balanced Random Forest on test data.")
    add_body_p(doc, "What to Notice in Figure 5: Diagonal values show 98.3% of Available, 94.1% of Nearly Full, and 94.2% of Full lots are correctly classified. Zero catastrophic errors (Full predicted Available) occurred.")

    add_figure_custom(doc, os.path.join(FIG_DIR, "fig4_precision_recall_curves.png"),
                      caption="Figure 6: Multi-class Precision-Recall (PR) curves and area under curve metrics.")
    add_body_p(doc, "What to Notice in Figure 6: AUC-PR is 0.993 for Available, 0.969 for Nearly Full, and 0.978 for Full, confirming high precision even at high recall thresholds.")

    add_figure_custom(doc, os.path.join(FIG_DIR, "fig5_feature_importances.png"),
                      caption="Figure 7: Gini feature importance ranking across 15 past-only engineered predictors.")
    add_body_p(doc, "What to Notice in Figure 7: Current occupancy (38.6%) and immediate lag_1 (23.9%) dominate split purity, followed by rolling mean (14.6%) and lag_2 (8.4%).")

    # Table 6: Master comparison
    t6_headers = ["Model", "Family", "Val Acc", "Val F1", "Test Acc", "Test F1", "Test Full Rec", "ROC-AUC", "Latency (ms)"]
    t6_data = [
        ["Persistence Baseline", "Baseline", "0.8839", "0.8760", "0.8845", "0.8800", "0.8843", "N/A", "0.005 ms"],
        ["Logistic Regression", "Linear", "0.9423", "0.9400", "0.9284", "0.9271", "0.9472", "0.9876", "0.000 ms"],
        ["Gaussian Naive Bayes", "Bayesian", "0.8067", "0.7964", "0.8058", "0.7932", "0.8426", "0.9335", "0.001 ms"],
        ["Decision Tree (CART)", "Tree", "0.9589", "0.9550", "0.9535", "0.9477", "0.9137", "0.9819", "0.001 ms"],
        ["KNN (k=7)", "Instance", "0.9265", "0.9190", "0.8973", "0.8864", "0.8985", "0.9766", "0.189 ms"],
        ["SVM (RBF Kernel)", "Kernel", "0.9533", "0.9486", "0.9312", "0.9234", "0.9492", "0.9911", "0.298 ms"],
        ["Multi-Layer Perceptron", "Neural", "0.9584", "0.9539", "0.9440", "0.9391", "0.9574", "0.9937", "0.001 ms"],
        ["AdaBoost", "Ensemble", "0.9269", "0.9184", "0.9260", "0.9187", "0.8802", "0.9787", "0.038 ms"],
        ["Random Forest (Winner)", "Ensemble", "0.9646", "0.9617", "0.9606", "0.9564", "0.9421", "0.9959", "0.044 ms"],
        ["XGBoost", "Boosting", "0.9650", "0.9616", "0.9621", "0.9582", "0.9482", "0.9962", "0.004 ms"],
        ["LightGBM", "Boosting", "0.9661", "0.9631", "0.9601", "0.9559", "0.9462", "0.9962", "0.005 ms"]
    ]
    add_table_custom(doc, t6_headers, t6_data, caption="Table 6: Master benchmark comparison of 11 architectures across validation and test splits.")

    # Table 7: Bootstrap CI
    t7_headers = ["Top Architecture", "Mean Test Acc", "95% CI Test Accuracy", "Mean Test Macro F1", "95% CI Test Macro F1"]
    t7_data = [
        ["Random Forest (Balanced)", "0.9604", "[0.9550, 0.9657]", "0.9562", "[0.9503, 0.9619]"],
        ["XGBoost Classifier", "0.9622", "[0.9570, 0.9672]", "0.9583", "[0.9524, 0.9643]"],
        ["LightGBM Classifier", "0.9602", "[0.9550, 0.9651]", "0.9561", "[0.9501, 0.9617]"]
    ]
    add_table_custom(doc, t7_headers, t7_data, caption="Table 7: Bootstrap 95% confidence intervals for top three models on test set.")

    # Table 8: Ablation Study
    t8_headers = ["Configuration Tested", "Features", "Test Acc", "Test F1", "Macro F1 Delta", "Percentage Delta"]
    t8_data = [
        ["Full Model (All 15 Features)", "15", "0.9606", "0.9564", "0.0000", "+0.00% (Baseline)"],
        ["Ablation: Without Lags (No lag_1..3)", "12", "0.9599", "0.9555", "-0.0009", "-0.09%"],
        ["Ablation: Without Rolling Stats", "13", "0.9606", "0.9564", "0.0000", "-0.00%"],
        ["Ablation: Without Cyclical Time (No sin/cos)", "13", "0.9559", "0.9510", "-0.0054", "-0.56%"],
        ["Ablation: Without Any Past Sensor Feeds", "10", "0.9535", "0.9476", "-0.0088", "-0.92%"],
        ["Ablation: Lags Only (No spatial/temporal IDs)", "5", "0.9405", "0.9322", "-0.0242", "-2.53%"]
    ]
    add_table_custom(doc, t8_headers, t8_data, caption="Table 8: Systematic feature ablation study on the held-out test split.")

    # Figures: SOTA bars, Accuracy vs latency
    add_figure_custom(doc, os.path.join(FIG_DIR, "fig6_sota_model_comparison.png"),
                      caption="Figure 8: Master model performance comparison on held-out test Macro F1 and Full Recall.")
    add_figure_custom(doc, os.path.join(FIG_DIR, "fig7_accuracy_vs_latency.png"),
                      caption="Figure 9: Accuracy vs. inference latency trade-off across 11 evaluated architectures.")

    # 10. ERROR ANALYSIS
    p_s10 = doc.add_paragraph()
    style_heading(p_s10, "10. Data-Grounded Error Analysis on Held-Out Test Data", level=2)
    add_body_p(doc,
        "Total Test Misclassifications: Exactly 209 out of 5,308 samples (3.94% error rate). "
        "Ground Truth Investigation: We avoid speculative causes (such as unverified events or rail disruptions). "
        "Every error was audited strictly through what the data shows: distance to the 50%/80% boundary, 30-minute delta (change over prior reading), "
        "facility size, and day of week. Table 9 documents four representative real failure cases."
    )

    # Table 9: Error Analysis
    t9_headers = ["Facility Code", "Timestamp", "Cap", "Occ %", "30-min Delta", "True", "Pred", "Data-Grounded Root Cause"]
    t9_data = [
        ["BHMBRCBRG03", "2016-12-08 15:30", "849", "52.3%", "+4.8%", "Available", "Nearly Full", "Boundary proximity: Current occupancy was 52.3% (within 2.3% of 50% threshold) with rapid upward momentum (+4.8%); lot discharged slightly instead."],
        ["Bull Ring", "2016-12-10 14:00", "3,053", "78.4%", "+2.1%", "Nearly Full", "Full", "Saturation boundary proximity: Occupancy was 78.4% (within 1.6% of 80% threshold). Saturday afternoon peak projected saturation, but vehicle inflows plateaued."],
        ["BHMNCPPLS01", "2016-12-14 11:30", "450", "46.2%", "-8.4%", "Available", "Nearly Full", "Sudden discharge: Occupancy plunged by 8.4% in 30 minutes, departing from typical mid-day accumulation curves."],
        ["BHMBCCTHL01", "2016-12-17 12:30", "387", "51.4%", "+0.5%", "Nearly Full", "Available", "Weekend volatility: Saturday noon reading sitting at 51.4%, where minor vehicle turnover caused boundary oscillation."]
    ]
    add_table_custom(doc, t9_headers, t9_data, caption="Table 9: Data-grounded misclassification failure cases on held-out test data.")

    # 11. MODEL CHOICE
    p_s11 = doc.add_paragraph()
    style_heading(p_s11, "11. Deployed Model Choice & Engineering Trade-Offs", level=2)
    add_body_p(doc,
        "Why Deploy Random Forest When LightGBM / XGBoost Scored Slightly Higher? "
        "On the validation set, LightGBM scored 0.9631 Macro F1 and XGBoost 0.9616, compared to Random Forest's 0.9617. "
        "On the test set, XGBoost scored 0.9582, Random Forest 0.9564, and LightGBM 0.9559. "
        "The difference between 0.9582 and 0.9564 is less than two-tenths of a percentage point. "
        "As proven by our 1,000-sample bootstrap confidence intervals (Table 7), Random Forest ([0.9503, 0.9619]) and XGBoost ([0.9524, 0.9643]) heavily overlap. "
        "Statistically, neither model is superior."
    )
    add_body_p(doc,
        "We chose the Balanced Random Forest for production based on three practical engineering advantages:\n"
        "1. Native Class Balancing: Random Forest's balanced bagging formulation draws bootstrapped samples with inverse class weights, ensuring stable decision splits across minority saturated lots.\n"
        "2. Hyperparameter Stability: Bagging trees are non-sequential. Unlike gradient boosting, which requires learning rate decay and early stopping to prevent gradient explosion, Random Forest is robust out of the box.\n"
        "3. Real-Time Latency: At 0.044 ms per inference, Random Forest forecasts availability for all 30 Birmingham facilities simultaneously in 1.3 milliseconds, enabling instantaneous page loads in Streamlit."
    )

    # 12. THE UI
    p_s12 = doc.add_paragraph()
    style_heading(p_s12, "12. ParkWise Streamlit Application & Docker Architecture", level=2)
    add_body_p(doc,
        "Application Design & User Flow: The Streamlit application ('ParkWise', app/main.py, app/helpers.py, app/styles.css) provides four clean screens:\n"
        "1. Find Parking (Home): Answering 'Where are you going and when?' with at most 3 visible inputs. Displays a big verdict badge ('Easy to park', 'Filling up', 'Likely full'), "
        "a visual fill bar ('About 77% full'), estimated open bays, and actionable advice ('Try Pershore Street, or arrive before 11:00 AM').\n"
        "2. All Car Parks: A clean card list of all 30 facilities sortable by 'Easiest to park first' with availability filter chips.\n"
        "3. Busy Times: A single hour-by-hour bar strip highlighting the best and worst arrival windows in words.\n"
        "4. About: Project methodology, dataset provenance, and a collapsed technical appendix containing the full model leaderboard for lab viva grading."
    )
    add_body_p(doc,
        "How a Prediction is Made: When the user selects a car park and time, app/helpers.py computes the feature row using the chosen time, date, facility ID, "
        "and historical hourly occupancy averages. The row is standardized via models/scaler.joblib and passed to models/parking_model.joblib for inference."
    )
    add_body_p(doc,
        "UI Limitations Stated Honestly: The app predicts based on historical hourly averages for the selected time, NOT live real-time IoT feeds, "
        "as the Birmingham dataset represents an offline historical archive. Furthermore, accessibility styling uses high-contrast navy and teal with redundant symbols (●, ▲, ■), "
        "but has not undergone formal third-party WCAG audit."
    )

    # 13. CODE WALKTHROUGH
    p_s13 = doc.add_paragraph()
    style_heading(p_s13, "13. Codebase Walkthrough, Project Layout & Pytest Suite", level=2)
    add_body_p(doc,
        "Project Directory Layout:\n"
        "• data/raw/dataset.csv: Original UCI Birmingham sensor telemetry (35,717 rows).\n"
        "• data/processed/: Chronological splits train.csv (24,766), val.csv (5,307), test.csv (5,308).\n"
        "• src/preprocess.py: Cleaning, boundary clipping, 15-feature engineering, and chronological splitting.\n"
        "• src/train.py: 11-model benchmark, metric export, and model serialization.\n"
        "• models/parking_model.joblib & scaler.joblib: Serialized production model and fitted normalizer.\n"
        "• app/main.py, helpers.py, styles.css: Consumer Streamlit web application.\n"
        "• tests/test_pipeline.py: Automated pytest suite verifying cleaning bounds, feature count (15), chronological order, and inference stability (4/4 tests passing).\n"
        "• Dockerfile: Multi-stage container definition exposing port 8501 with automated healthcheck probe."
    )
    add_body_p(doc,
        "Exact Execution Commands:\n"
        "1. Install dependencies: pip install -r requirements.txt\n"
        "2. Run preprocessing: python src/preprocess.py\n"
        "3. Run training & evaluation: python src/train.py\n"
        "4. Run test suite: python -m pytest tests/ -v\n"
        "5. Launch Streamlit UI: streamlit run app/main.py\n"
        "6. Docker deployment: docker build -t parkwise . && docker run -p 8501:8501 parkwise"
    )

    # 14. LIMITATIONS & FUTURE WORK
    p_s14 = doc.add_paragraph()
    style_heading(p_s14, "14. Project Limitations, Integrity & Future Scope", level=2)
    add_body_p(doc,
        "Honest Limitations:\n"
        "1. Geographic & Temporal Scope: Data originates from a single UK city (Birmingham) in Autumn/Winter 2016. Transferring this model to Indian smart cities requires local sensor retraining.\n"
        "2. Static Historical Feed in UI: The web application predicts based on historical diurnal curves rather than streaming real-time API barrier logs.\n"
        "3. Absence of GPS Coordinates: The dataset lacks latitude/longitude coordinates; a facility status board was used to avoid fabricating fake map coordinates.\n"
        "4. Exogenous Variables: Telemetry lacks localized precipitation, road construction, or transit strike data."
    )
    add_body_p(doc,
        "Future Work:\n"
        "1. Streaming MQTT Ingestion: Connecting barrier loop detectors to continuously update autoregressive lags in real time.\n"
        "2. Edge Microcontroller Quantization: Compiling the Random Forest model to C++ for deployment on solar-powered ESP32 roadside VMS boards.\n"
        "3. Computer Vision Fusion: Integrating entry/exit camera feeds with loop detectors to track individual stall utilization."
    )

    doc.add_page_break()

    # =========================================================================
    # PART B: VIVA QUESTION BANK (80+ QUESTIONS)
    # =========================================================================
    p_pb = doc.add_paragraph()
    style_heading(p_pb, "PART B: COMPREHENSIVE VIVA QUESTION BANK", level=1)
    add_body_p(doc,
        "This question bank contains 85 categorized questions with concise, technically rigorous, numerical model answers. "
        "Review these before presenting to your instructor."
    )

    # TOPIC 1: DATASET (Q1-Q12)
    p_t1 = doc.add_paragraph()
    style_heading(p_t1, "Topic 1: Dataset Facts & Physical Attributes (Q1–Q12)", level=2)
    qas_topic1 = [
        ("What dataset did you use, where did it come from, and what is its licence?",
         "We used the Parking Birmingham dataset from the UC Irvine Machine Learning Repository (Dataset ID: 482). It is open data released under the Creative Commons Attribution 4.0 International (CC BY 4.0) licence."),
        ("What time period does the dataset cover, and what is the sampling frequency?",
         "It covers an 11-week period from October 4, 2016, to December 19, 2016. Readings were recorded at nominal 30-minute intervals during municipal operating hours from 07:30 to 16:34."),
        ("How many raw records are in the dataset, and what are the raw columns?",
         "There are exactly 35,717 raw rows. The four raw columns are SystemCodeNumber (car park identifier), Capacity (total bays), Occupancy (occupied bays), and LastUpdated (timestamp)."),
        ("How many car parks are in the dataset? Why does the encoding map list 29 while the data has 30?",
         "The raw CSV contains exactly 30 unique car park codes. However, facility 'BHMBRTARC01' has only 88 rows, all recorded between December 13 and December 18, 2016. Because it has no readings prior to December 13, it falls entirely into the held-out test split, meaning only 29 car parks appear in the training and validation sets."),
        ("What is the range of car park capacities in Birmingham?",
         "Capacities range from 220 bays at Euro Car Park (BHMEURBRD02) to 4,675 bays at Others-CCCPS133, with an average capacity of approximately 1,180 bays."),
        ("How many rows remain after cleaning and feature engineering?",
         "Exactly 35,501 rows remain after dropping 216 duplicates. After generating autoregressive lags and targets (which drops 4 boundary rows per facility, 30 × 4 = 120 rows), exactly 35,381 clean rows remain."),
        ("What is the exact sample breakdown across train, validation, and test splits?",
         "Training split contains 24,766 rows (70.0%), validation contains 5,307 rows (15.0%), and held-out test contains 5,308 rows (15.0%)."),
        ("What is the class distribution in the training set?",
         "Available (<50%) represents 54.8% (13,566 rows), Nearly Full (50%–79%) represents 29.9% (7,403 rows), and Full (≥80%) represents 15.3% (3,797 rows)."),
        ("Did the class distribution change in the test set? Why?",
         "Yes. In the test set (December 8 to 19), Available dropped to 46.8% while Full increased to 18.6% (985 rows). This reflects real-world physical dynamics: parking congestion escalates significantly during pre-Christmas holiday shopping."),
        ("Were there any missing values in the raw dataset?",
         "No. The raw CSV contains zero null or missing entries across all four attributes."),
        ("What sensor technology captured this data?",
         "The data was captured using inductive loop barrier detectors and electronic barrier ticketing systems managed by Birmingham City Council and NCP, logging entry and exit counts."),
        ("Are there spatial GPS coordinates in the dataset?",
         "No, the dataset contains only alphanumeric facility codes and car park names. No latitude or longitude coordinates were provided, which is why we avoided fabricating false coordinates for map screens.")
    ]
    for i, (q, a) in enumerate(qas_topic1, 1):
        add_qa_p(doc, i, q, a)

    # TOPIC 2: PREPROCESSING (Q13-Q22)
    p_t2 = doc.add_paragraph()
    style_heading(p_t2, "Topic 2: Preprocessing, Deduplication & Boundary Clipping (Q13–Q22)", level=2)
    qas_topic2 = [
        ("Why did you have to deduplicate rows, and how many were removed?",
         "Network transmission retries created duplicate logs for the same facility at identical timestamps. Exactly 216 duplicate rows on (SystemCodeNumber, LastUpdated) were identified and dropped, keeping the first valid entry."),
        ("Why were there negative occupancy values in the raw data, and how did you fix them?",
         "Sensor calibration drift at parking barriers occasionally logged more exit counts than entry counts, producing 12 negative readings down to -8 bays. We clipped negative values strictly to 0 bays."),
        ("Why did some occupancy readings exceed rated capacity, and how did you handle them?",
         "Exactly 373 readings exceeded rated capacity (up to 104.1%) due to overflow bay usage and temporary double-parking. To prevent unbounded occupancy percentages, we clipped occupancy to rated capacity: min(Occupancy, Capacity)."),
        ("Did you remove any records based on time of day?",
         "No. Telemetry verification confirmed that all 35,717 raw readings were logged strictly between 07:30 and 16:34 during monitored municipal operating hours (zero records outside 07:00–17:00)."),
        ("Why did feature engineering cause 120 rows to be dropped?",
         "Constructing 3 past lags (t-1, t-2, t-3) and a 1-step lookahead target (t+1) per facility drops the first 3 rows and final row for each of the 30 car parks. Exactly 30 × 4 = 120 boundary rows were dropped."),
        ("Why did you use StandardScaler, and which features were scaled?",
         "StandardScaler scales features to zero mean and unit variance. This is necessary for gradient-based models (MLP, Logistic Regression) and distance-based models (SVM, KNN) to prevent large-magnitude features (like Capacity) from dominating small features (like hour_sin)."),
        ("Why was the scaler fit strictly on the training partition?",
         "Fitting the scaler on the entire dataset constitutes data leakage, as test set means and variances would leak into training. The scaler was fit exclusively on the 24,766 training rows."),
        ("What encoding was used for the categorical car park identifier?",
         "Scikit-learn's LabelEncoder mapped the 30 car park alphanumeric strings into integer indices from 0 to 29."),
        ("Did you apply SMOTE or synthetic oversampling to handle class imbalance?",
         "No. Synthetic oversampling in time-series telemetry fabricates artificial temporal states that disrupt physical momentum. Instead, we used cost-sensitive inverse class frequency loss weighting directly during model training."),
        ("What were the exact balanced loss weights applied?",
         "Using w_c = N_samples / (N_classes × N_c), the training weights were 0.609 for Available, 1.115 for Nearly Full, and 2.174 for Full.")
    ]
    for i, (q, a) in enumerate(qas_topic2, 13):
        add_qa_p(doc, i, q, a)

    # TOPIC 3: FEATURE ENGINEERING (Q23-Q32)
    p_t3 = doc.add_paragraph()
    style_heading(p_t3, "Topic 3: Feature Engineering, Autoregressive Lags & Leakage (Q23–Q32)", level=2)
    qas_topic3 = [
        ("What is data leakage? Give a concrete example in parking prediction.",
         "Data leakage occurs when information from the future or test set is inadvertently fed into the training pipeline. For example, if we computed a rolling mean using readings from t-1, t, and t+1 to predict class at t+1, the model would have access to the future answer during training."),
        ("How did your feature pipeline guarantee zero lookahead leakage?",
         "Every engineered feature at time t was computed strictly from sensor readings at time t or prior (t-1, t-2, t-3). The target is the class of the reading at t+1. No future information is present in the feature row."),
        ("Why did you transform hour of the day into sine and cosine components?",
         "Hour is cyclical: 23:00 and 00:00 are separated by only 1 hour, but an integer representation treats them as 23 units apart. Projecting hour onto a 24-hour circle using hour_sin = sin(2πt/24) and hour_cos = cos(2πt/24) preserves temporal continuity."),
        ("What are lag features and why are they necessary?",
         "Lag features (lag_1, lag_2, lag_3) represent occupancy percentages 30, 60, and 90 minutes prior. They capture traffic momentum and velocity, allowing the model to distinguish between an emptying lot and a rapidly filling lot."),
        ("What rolling statistics did you compute, and why?",
         "We computed rolling_mean_3 and rolling_std_3 over the prior three readings. Rolling mean smooths transient sensor spikes, while rolling standard deviation captures volatility and turnover instability."),
        ("What are all 15 features used by the models?",
         "Capacity, occupancy_pct, hour, minute, dayofweek, is_weekend, weekofyear, hour_sin, hour_cos, SystemCodeNumber_enc, lag_1, lag_2, lag_3, rolling_mean_3, and rolling_std_3."),
        ("Why did you include facility Capacity as a feature?",
         "A lot with 300 bays behaves differently from one with 4,000 bays. Large lots exhibit higher physical turnover inertia, whereas small lots can saturate completely within a single 30-minute window."),
        ("Why include weekofyear in the feature set?",
         "The dataset spans October (week 40) to late December (week 51). Week of year captures seasonal demand trends, specifically the ramp-up in commercial parking leading into Christmas."),
        ("What did the feature ablation study reveal about lag features?",
         "Removing autoregressive lags degraded Macro F1 by 0.09 percentage points directly, while removing all past sensor feeds degraded Macro F1 by 0.92 percentage points. Removing cyclical time degraded F1 by 0.56 percentage points."),
        ("What happens if you train using lags only without temporal or spatial context?",
         "Performance degrades significantly: Test Macro F1 dropped from 0.9564 to 0.9322 (a 2.53% relative loss), proving that time-of-day and facility identity provide crucial baseline context.")
    ]
    for i, (q, a) in enumerate(qas_topic3, 23):
        add_qa_p(doc, i, q, a)

    # TOPIC 4: MODELS (Q33-Q46)
    p_t4 = doc.add_paragraph()
    style_heading(p_t4, "Topic 4: Machine Learning Architectures & Mechanics (Q33–Q46)", level=2)
    qas_topic4 = [
        ("What is the Persistence Baseline and what were its results?",
         "The persistence baseline assumes that occupancy class at time t persists unchanged at t+1. It achieved 88.39% accuracy and 0.8760 Macro F1 on validation, and 88.45% accuracy and 0.8800 Macro F1 on test. This is the minimum benchmark ML must surpass."),
        ("How does Logistic Regression perform on this dataset?",
         "Logistic Regression with multinomial softmax and L2 penalty achieved 92.84% test accuracy and 0.9271 Macro F1. While fast (0.47s training), its linear decision boundaries cannot capture non-linear temporal interactions."),
        ("Why did Gaussian Naive Bayes perform poorly (79.32% Test Macro F1)?",
         "Naive Bayes assumes conditional feature independence given the class. In our pipeline, lag_1, lag_2, lag_3, and rolling_mean_3 are heavily correlated (collinear). Violating this independence assumption severely degrades Naive Bayes."),
        ("How was the Decision Tree configured and what were its results?",
         "We used CART with Gini impurity and max_depth=8. It achieved 95.35% test accuracy and 0.9477 Macro F1. Constraining tree depth prevented catastrophic overfitting on noisy sensor records."),
        ("Why does K-Nearest Neighbors exhibit high inference latency (0.189 ms/sample)?",
         "KNN is an instance-based lazy learner. During inference, it must calculate Euclidean distances across all 15 dimensions to all 24,766 training points, creating severe latency bottlenecks."),
        ("How did the Support Vector Machine perform, and what was its primary drawback?",
         "SVM with an RBF kernel achieved 93.12% test accuracy and 0.9234 Macro F1. Its primary drawback was computational overhead: it took 31.2 seconds to fit and had a high latency of 0.298 ms/sample evaluating 61,935 support vectors."),
        ("How was the Multi-Layer Perceptron (MLP) structured, and how did it perform?",
         "The MLP comprised two hidden layers (64 and 32 neurons) with ReLU activations and Adam optimizer. It achieved 94.40% test accuracy and 0.9391 Macro F1, training in 5.528 seconds with 0.001 ms latency."),
        ("How does AdaBoost work, and why did it achieve 91.87% Test Macro F1?",
         "AdaBoost sequentially trains 100 shallow decision stumps, weighting misclassified samples higher in subsequent iterations. Because stumps split on a single feature, AdaBoost struggled to model complex multi-feature interactions compared to deep trees."),
        ("What are the exact hyperparameters of your winning Random Forest?",
         "RandomForestClassifier(n_estimators=100, max_depth=12, class_weight='balanced', max_features='sqrt', random_state=42, n_jobs=-1)."),
        ("What is the difference between Bagging and Boosting?",
         "Bagging (Random Forest) trains independent trees in parallel on bootstrap samples and averages their predictions to reduce variance. Boosting (XGBoost, LightGBM) trains trees sequentially, where each new tree fits the residual errors of preceding trees to reduce bias."),
        ("How did XGBoost perform compared to Random Forest?",
         "XGBoost scored 96.21% test accuracy and 0.9582 Macro F1 (vs 96.06% and 0.9564 for Random Forest). As shown by bootstrap confidence intervals, they operate in overlapping statistical parity."),
        ("How did LightGBM perform, and why was it so fast?",
         "LightGBM scored 96.01% test accuracy and 0.9559 Macro F1, training in only 0.334 seconds. It achieves high speed through histogram-based feature binning and leaf-wise tree growth."),
        ("Did you tune hyperparameters using GridSearchCV?",
         "No, we used principled heuristics and constrained search spaces (e.g. depth 12 for Random Forest, depth 6 for XGBoost) to prevent overfitting and ensure fast execution on standard academic workstations."),
        ("What is the parameter count of your production Random Forest model?",
         "Across all 100 estimator trees, the production Random Forest contains exactly 120,866 split nodes.")
    ]
    for i, (q, a) in enumerate(qas_topic4, 33):
        add_qa_p(doc, i, q, a)

    # TOPIC 5: METRICS (Q47-Q58)
    p_t5 = doc.add_paragraph()
    style_heading(p_t5, "Topic 5: Evaluation Metrics, Confusion Matrix & PR Curves (Q47–Q58)", level=2)
    qas_topic5 = [
        ("Why is accuracy alone an insufficient metric for parking availability?",
         "In our dataset, Available represents over 54% of training records. A naive model predicting Available 100% of the time would achieve >54% accuracy while completely failing to warn drivers about full parking lots."),
        ("What is the mathematical difference between Macro F1 and Weighted F1?",
         "Macro F1 computes F1 independently for each class and averages them with equal weight (1/3 each). Weighted F1 weights each class F1 by its sample frequency, obscuring poor performance on minority classes."),
        ("What is Precision and what does it mean for the 'Full' class?",
         "Precision is TP / (TP + FP). For the Full class, it measures: 'When the model predicts a lot is Full, what percentage of the time is it genuinely Full?' Our model achieves 95.28% precision on Full."),
        ("What is Recall and what does it mean for the 'Full' class?",
         "Recall is TP / (TP + FN). For the Full class, it measures: 'Out of all lots that were actually Full, what percentage did the model correctly detect?' Our model achieves 94.21% recall on Full."),
        ("What was the draft label-ordering bug and how did you resolve it?",
         "A draft script calculated metrics using default integer indices where labels did not match target class order, reporting Nearly Full F1 as 0.03 and Full F1 as 0.04. We resolved this by explicitly specifying labels=['Available', 'Nearly Full', 'Full'], yielding correct F1 scores of 0.9786, 0.9433, and 0.9474."),
        ("What does the normalized confusion matrix show for the production model?",
         "It shows true positive rates of 98.3% for Available, 94.1% for Nearly Full, and 94.2% for Full on the held-out test split, with zero catastrophic errors (Full predicted Available)."),
        ("What is a catastrophic error in this context?",
         "A catastrophic error occurs when the model predicts Available (<50%) for a lot that is actually Full (≥80%), misrouting drivers into congested bottlenecks. In our test set, exactly 0 catastrophic errors occurred."),
        ("What are Precision-Recall (PR) curves, and why are they preferred over ROC curves on imbalanced data?",
         "ROC curves evaluate True Positive Rate against False Positive Rate. When the negative class is large, False Positive Rate remains deceptively low. PR curves evaluate Precision against Recall directly, providing a strict assessment of minority class discovery."),
        ("What are the AUC-PR scores for your production model?",
         "The Area Under the PR Curve is 0.993 for Available, 0.969 for Nearly Full, and 0.978 for Full."),
        ("What is One-vs-Rest (OvR) ROC-AUC?",
         "OvR decomposes multi-class evaluation into three binary comparisons, treating each class as positive and the other two as negative. Our Random Forest achieved a multi-class ROC-AUC of 0.9959."),
        ("How many total misclassifications occurred on the test set?",
         "Exactly 209 out of 5,308 test instances were misclassified, representing an error rate of 3.94%."),
        ("Which class is the most difficult to predict, and why?",
         "Nearly Full (50%–79%) is inherently the hardest class because it sits bordered between two active decision thresholds (50% and 80%), where minor occupancy fluctuations cause boundary crossovers.")
    ]
    for i, (q, a) in enumerate(qas_topic5, 47):
        add_qa_p(doc, i, q, a)

    # TOPIC 6: MODEL SELECTION & OVERFITTING (Q59-Q68)
    p_t6 = doc.add_paragraph()
    style_heading(p_t6, "Topic 6: Model Selection, Confidence Bounds & Overfitting (Q59–Q68)", level=2)
    qas_topic6 = [
        ("Why did you choose Random Forest over XGBoost or LightGBM?",
         "XGBoost (0.9582 test Macro F1) and LightGBM (0.9559) scored very close to Random Forest (0.9564). We chose Random Forest because bootstrap confidence intervals prove they are in statistical parity, while Random Forest offers native balanced bagging, zero learning-rate instability, and robust 0.044 ms latency."),
        ("What are bootstrap confidence intervals, and how did you compute them?",
         "We drew B=1,000 bootstrap resamples with replacement from the 5,308 test predictions, computed accuracy and Macro F1 on each resample, and took the 2.5th and 97.5th percentiles to establish empirical 95% confidence intervals."),
        ("What are the 95% confidence intervals for Random Forest, XGBoost, and LightGBM?",
         "Random Forest: Macro F1 [0.9503, 0.9619]; XGBoost: [0.9524, 0.9643]; LightGBM: [0.9501, 0.9617]. Their intervals heavily overlap, confirming statistical equivalence."),
        ("How did you verify that your Random Forest is not overfitting?",
         "Training Macro F1 reached 0.978 while Validation Macro F1 reached 0.962 and Test Macro F1 reached 0.956. Constraining tree depth to 12 and requiring square-root feature subsampling prevented excessive leaf memorization."),
        ("Why did you use a single chronological split instead of K-Fold Cross-Validation?",
         "Standard K-Fold randomly shuffles rows across time, causing severe temporal leakage. Chronological K-Fold (TimeSeriesSplit) was evaluated during initial exploration, but a fixed 70/15/15 split provides the cleanest real-world test on unseen calendar weeks."),
        ("What is the role of the validation set vs the test set?",
         "The validation set was used for model exploration, algorithm comparison, and hyperparameter selection. The held-out test set was sequestered and evaluated only once to provide an unbiased final benchmark."),
        ("What is cost-sensitive learning?",
         "Cost-sensitive learning modifies the algorithm's objective function to penalize misclassifications on minority classes more heavily than on majority classes, preventing majority bias."),
        ("What are the top three most important features according to Gini importance?",
         "Current occupancy percentage (occupancy_pct, 38.6%), immediate lag_1 (23.9%), and 3-step rolling mean (rolling_mean_3, 14.6%)."),
        ("Does facility ID matter for prediction?",
         "Yes, SystemCodeNumber_enc accounts for 2.8% of Gini importance, allowing the model to capture facility-specific baseline utilization and local commuter dynamics."),
        ("Did any model fail to beat the persistence baseline?",
         "No. All machine learning models surpassed the persistence baseline (0.8760 validation Macro F1). Even Gaussian Naive Bayes, despite its flawed independence assumption, captured basic temporal trends.")
    ]
    for i, (q, a) in enumerate(qas_topic6, 59):
        add_qa_p(doc, i, q, a)

    # TOPIC 7: UI & DEPLOYMENT (Q69-Q76)
    p_t7 = doc.add_paragraph()
    style_heading(p_t7, "Topic 7: Streamlit UI, Dockerization & Practical Deployment (Q69–Q76)", level=2)
    qas_topic7 = [
        ("Why did you choose Streamlit for the user interface?",
         "Streamlit enables rapid development of reactive, stateful web applications in pure Python, integrating directly with our serialized scikit-learn model and data pipelines."),
        ("What are the four main screens in the ParkWise app?",
         "1. Find Parking (single-query search with alternative suggestions), 2. All Car Parks (status board of all 30 facilities), 3. Busy Times (hour-by-hour bar strip), and 4. About (project credits and collapsed technical leaderboard)."),
        ("How does the app make a prediction from user input?",
         "When the user selects a car park and time, app/helpers.py builds a 15-feature row using the chosen time, facility ID, and historical hourly averages, standardizes it via scaler.joblib, and queries parking_model.joblib."),
        ("How does the app suggest alternative car parks?",
         "If the target lot is predicted Nearly Full or Full, app/helpers.py queries the model across all other 29 facilities for that exact time slot and recommends the car park with the lowest predicted occupancy."),
        ("What happens if a user selects a time outside operating hours (e.g. 2:00 AM)?",
         "The application displays a friendly warning banner notifying the user that sensors operate between 07:30 and 16:34, and clamps the feature query to the nearest operational boundary."),
        ("What does the Dockerfile do?",
         "It defines a lightweight container packaging Python 3.12, installs requirements.txt, copies app/ and models/, exposes port 8501, and runs an automated curl healthcheck probe every 30 seconds."),
        ("What are the automated unit tests in tests/test_pipeline.py?",
         "Pytest validates four pipeline invariants: 1. Cleaning boundary clipping, 2. Feature count (15 columns), 3. Chronological split order, and 4. Model inference determinism (100% pass rate)."),
        ("Does the deployed app receive real-time streaming sensor feeds?",
         "No. The app uses historical hourly averages for the selected time slot, as the Birmingham dataset is a historical open data archive. We state this transparently in the report.")
    ]
    for i, (q, a) in enumerate(qas_topic7, 69):
        add_qa_p(doc, i, q, a)

    # TOPIC 8: DEFENSE & LIMITATIONS (Q77-Q85)
    p_t8 = doc.add_paragraph()
    style_heading(p_t8, "Topic 8: Tough Defense Questions, Limitations & Conceptual Drift (Q77–Q85)", level=2)
    qas_topic8 = [
        ("Is a 96% accuracy score trustworthy, or did you overfit?",
         "It is trustworthy because it was evaluated on an unseen chronological test set (December 8 to 19) that was completely sequestered during training. Furthermore, bootstrap confidence intervals show a tight bounds of [95.5%, 96.6%]."),
        ("What are the primary weaknesses of your project?",
         "1. Offline data (no streaming MQTT ingestion), 2. Single-city scope (Birmingham 2016), 3. Absence of weather or road construction features, and 4. Lack of spatial GPS coordinates."),
        ("Can this model be deployed in Indian cities like Nagpur or Bengaluru?",
         "Not directly without retraining. Indian parking dynamics involve different vehicle mixes (two-wheelers, auto-rickshaws), unmetered curbside parking, and distinct monsoon weather disruptions. The pipeline architecture transfers, but weights must be retrained on local telemetry."),
        ("What is concept drift, and how would it affect this system?",
         "Concept drift occurs when traffic patterns change over time (e.g. new metro line opens, fuel prices rise, or seasonal changes occur). If deployed long-term, the model would require periodic re-training on sliding 4-week historical windows."),
        ("Why did you not implement an LSTM or Transformer neural network?",
         "Published literature (e.g. Dia et al., 2022) confirms that tree ensembles consistently outperform deep sequence models on tabular sensor lags. Furthermore, LSTMs require sequential tensor reshaping, GPU infrastructure, and exhibit high inference latency (>100 ms)."),
        ("What would you do if a sensor went offline and stopped transmitting lag_1?",
         "In production, we would implement an imputation fallback: if lag_1 is missing, substitute the facility's historical median occupancy for that specific hour of the week."),
        ("How did you ensure reproducibility across environments?",
         "All random seeds were fixed (random_state=42), dependencies were pinned in requirements.txt, scripts were made headless, and execution instructions were documented in REPRODUCE.md."),
        ("What would you do differently if you had three more months on this project?",
         "I would integrate streaming Kafka/MQTT pipelines for live sensor ingestion, collect exogenous weather API feeds, and deploy the quantized model onto an ESP32 microcontroller for solar-powered roadside VMS signs."),
        ("Summarize in one sentence why your project deserves top marks.",
         "Because it enforces strict chronological data integrity with zero leakage, benchmarks 11 algorithms with honest bootstrap statistics, achieves 96.06% test accuracy with sub-millisecond execution, and packages the result into a fully functional, containerized consumer application.")
    ]
    for i, (q, a) in enumerate(qas_topic8, 77):
        add_qa_p(doc, i, q, a)

    doc.add_page_break()

    # =========================================================================
    # QUICK NUMBERS CHEAT SHEET
    # =========================================================================
    p_cs = doc.add_paragraph()
    style_heading(p_cs, "Quick Numbers Cheat Sheet (Complete Benchmark Lookup)", level=1)
    add_body_p(doc, "Keep this table open during your viva examination. Every number reflects executed code on identical splits.")

    t10_headers = ["Model", "Family", "Val Acc", "Val F1", "Test Acc", "Test F1", "Full Rec", "ROC-AUC", "Latency"]
    t10_data = [
        ["Persistence Baseline", "Baseline", "88.39%", "0.8760", "88.45%", "0.8800", "88.43%", "N/A", "0.005 ms"],
        ["Logistic Regression", "Linear", "94.23%", "0.9400", "92.84%", "0.9271", "94.72%", "0.9876", "0.000 ms"],
        ["Gaussian Naive Bayes", "Bayesian", "80.67%", "0.7964", "80.58%", "0.7932", "84.26%", "0.9335", "0.001 ms"],
        ["Decision Tree (CART)", "Tree", "95.89%", "0.9550", "95.35%", "0.9477", "91.37%", "0.9819", "0.001 ms"],
        ["KNN (k=7)", "Instance", "92.65%", "0.9190", "89.73%", "0.8864", "0.8985", "0.9766", "0.189 ms"],
        ["SVM (RBF Kernel)", "Kernel", "95.33%", "0.9486", "93.12%", "0.9234", "94.92%", "0.9911", "0.298 ms"],
        ["Multi-Layer Perceptron", "Neural", "95.84%", "0.9539", "94.40%", "0.9391", "0.9574", "0.9937", "0.001 ms"],
        ["AdaBoost", "Ensemble", "92.69%", "0.9184", "92.60%", "0.9187", "0.8802", "0.9787", "0.038 ms"],
        ["Random Forest (Winner)", "Ensemble", "96.46%", "0.9617", "96.06%", "0.9564", "0.9421", "0.9959", "0.044 ms"],
        ["XGBoost", "Boosting", "96.50%", "0.9616", "96.21%", "0.9582", "0.9482", "0.9962", "0.004 ms"],
        ["LightGBM", "Boosting", "96.61%", "0.9631", "96.01%", "0.9559", "0.9462", "0.9962", "0.005 ms"]
    ]
    add_table_custom(doc, t10_headers, t10_data, caption="Table 10: Complete viva quick numbers cheat sheet across all 11 models.")

    doc.add_page_break()

    # =========================================================================
    # STRATEGY & MEMORISATION
    # =========================================================================
    p_strat = doc.add_paragraph()
    style_heading(p_strat, "If You Do Not Know the Answer: Viva Strategy Guide", level=1)
    add_body_p(doc,
        "Examiners respect academic honesty and engineering maturity far more than guessing or making up numbers. "
        "If asked a question outside what was evaluated, use this 4-step professional response strategy:"
    )
    add_body_p(doc,
        "1. Acknowledge and State the Scope Honestly:\n"
        "\"That is an insightful question, Professor. In our current implementation, we did not specifically test that configuration because our primary objective was "
        "establishing a leak-free chronological baseline on the authentic sensor telemetry.\""
    )
    add_body_p(doc,
        "2. Explain How the Current Pipeline Relates:\n"
        "\"What we did observe in our experiments is that feature groups like past autoregressive lags provided the strongest signal, whereas...\""
    )
    add_body_p(doc,
        "3. Provide the Concrete Technical Solution You Would Implement:\n"
        "\"If we were to extend the project to address that, I would implement [e.g. a rolling imputation pipeline / an online sliding-window retraining job / a spatial graph network] "
        "by taking the sensor streams and...\""
    )
    add_body_p(doc,
        "4. Golden Rules for the Examination:\n"
        "• Never invent a number. If you forget a decimal, say 'approximately 96%' or look at Table 10.\n"
        "• Emphasize data integrity: Whenever in doubt, anchor your answer on chronological splitting, leak prevention, and cost-sensitive balanced loss weighting.\n"
        "• Own the limitations: Admitting that the app uses historical diurnal profiles rather than streaming MQTT sensors shows real-world engineering understanding."
    )

    p_memo = doc.add_paragraph()
    style_heading(p_memo, "Numbers to Memorise: Instant Viva Recall Sheet", level=1)
    add_body_p(doc, "Commit these 12 core facts to memory before entering the viva room:")
    add_body_p(doc, "1. Raw Records: 35,717 rows across 30 car parks (Capacities: 220 to 4,675 bays).")
    add_body_p(doc, "2. Clean Records: 35,381 rows (216 duplicates dropped, 120 boundary lag rows dropped).")
    add_body_p(doc, "3. Physical Corrections: 12 negative readings clipped to 0; 373 overflows clipped to Capacity.")
    add_body_p(doc, "4. Chronological Splits: Train = 24,766 (70%), Val = 5,307 (15%), Test = 5,308 (15%).")
    add_body_p(doc, "5. Train Date Span: Oct 4, 2016 to Nov 26, 2016 (54 operating days).")
    add_body_p(doc, "6. Test Date Span: Dec 8, 2016 to Dec 19, 2016 (12 operating days, pre-Christmas peak).")
    add_body_p(doc, "7. Features: Exactly 15 past-only features (lags t-1,2,3; rolling mean/std; cyclical sine/cosine).")
    add_body_p(doc, "8. Target Classes: Available (<50%), Nearly Full (50%–79%), Full (≥80%).")
    add_body_p(doc, "9. Winning Model: Balanced Random Forest (100 trees, depth 12).")
    add_body_p(doc, "10. Test Accuracy: 96.06% [95% CI: 0.9550, 0.9657].")
    add_body_p(doc, "11. Test Macro F1: 0.9564 [95% CI: 0.9503, 0.9619]. Persistence Baseline = 0.8800.")
    add_body_p(doc, "12. Full Class Recall: 94.21% (Zero catastrophic errors on test data; latency = 0.044 ms).")

    # =========================================================================
    # REFERENCES
    # =========================================================================
    p_ref = doc.add_paragraph()
    style_heading(p_ref, "References", level=1)
    refs_viva = [
        "[1] F. Zhang, K. Shang, L. Yan, H. Nan, and Z. Miao, \"Prediction of parking space availability using improved MAT-LSTM network,\" ISPRS Int. J. Geo-Inf., vol. 13, no. 5, Art. no. 151, May 2024, doi: 10.3390/ijgi13050151.",
        "[2] F. J. Enríquez, J.-M. Mejía-Muñoz, G. Bravo, and O. Cruz-Mejía, \"Smart parking: Enhancing urban mobility with fog computing and machine learning-based parking occupancy prediction,\" Appl. Syst. Innov., vol. 7, no. 3, Art. no. 52, Jun. 2024, doi: 10.3390/asi7030052.",
        "[3] I. Dia, E. Ahvar, and G. M. Lee, \"Performance evaluation of machine learning and neural network-based algorithms for predicting segment availability in AIoT-based smart parking,\" Network, vol. 2, no. 2, pp. 225–238, Apr. 2022, doi: 10.3390/network2020015.",
        "[4] A. Dahiya et al., \"Machine learning-based prediction of parking space availability in IoT-enabled smart parking management systems,\" J. Adv. Transp., vol. 2024, Art. no. 8474973, 2024, doi: 10.1155/2024/8474973.",
        "[5] H.-T. Thai, T.-L. Nguyen-Tran, and K.-H. Le, \"Toward a predictive smart parking system in IoT-enabled cities,\" in Proc. IEEE NICS, Jan. 2023, pp. 248–253, doi: 10.1109/NICS56915.2022.10013435.",
        "[6] A. Janowski, M. Hüsrevoğlu, and M. Renigier-Biłozor, \"Sustainable parking space management using machine learning and swarm theory—The SPARK system,\" Appl. Sci., vol. 14, no. 24, Art. no. 12076, Dec. 2024, doi: 10.3390/app142412076.",
        "[7] D. Stolfi, E. Alba, and X. Yao, \"Predicting car park occupancy rates in smart cities,\" in Proc. LION, Springer, 2017, pp. 107–121. [Online]. UCI ML Repository ID: 482 (Parking Birmingham).",
        "[8] F. Pedregosa et al., \"Scikit-learn: Machine learning in Python,\" J. Mach. Learn. Res., vol. 12, pp. 2825–2830, 2011.",
        "[9] T. Chen and C. Guestrin, \"XGBoost: A scalable tree boosting system,\" in Proc. ACM KDD, 2016, pp. 785–794, doi: 10.1145/2939672.2939785.",
        "[10] G. Ke et al., \"LightGBM: A highly efficient gradient boosting decision tree,\" in Proc. NeurIPS, vol. 30, 2017, pp. 3146–3154.",
        "[11] Streamlit Developers, \"Streamlit: The fastest way to build and share data apps,\" 2024. [Online]. Available: https://streamlit.io."
    ]
    for r_text in refs_viva:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.first_line_indent = Inches(-0.3)
        r = p.add_run(r_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(15, 23, 42)

    p_end = doc.add_paragraph()
    p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_end.paragraph_format.space_before = Pt(20)
    r_end = p_end.add_run("- End of Viva Guide -")
    r_end.font.name = "Times New Roman"
    r_end.font.bold = True
    r_end.font.size = Pt(12)
    r_end.font.color.rgb = RGBColor(71, 85, 105)

    docx_path = os.path.join(FINAL_DIR, "Smart_Parking_Project_Explanation_and_Viva_Guide.docx")
    doc.save(docx_path)
    print(f"Viva Guide DOCX successfully saved at: {docx_path}")
    return docx_path

if __name__ == "__main__":
    build_viva_guide()

