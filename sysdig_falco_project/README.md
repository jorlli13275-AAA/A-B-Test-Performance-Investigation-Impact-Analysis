# Cloud Security A/B Test — Investigation Impact Analysis

## 1. Project Overview

This project analyzes an A/B test conducted on a cloud security platform using Falco alert data from Kubernetes environments.

The objective is to evaluate whether introducing a **runtime context panel** improves how users interact with and respond to security alerts.

---

## 2. Business Problem

Security teams receive a high volume of alerts, but not all alerts are effectively investigated or resolved.

Key questions:

- Does additional context increase engagement with alerts?
- Does it help users investigate alerts faster?
- Does it improve resolution outcomes?

---

## 3. Hypothesis

Users exposed to a runtime context panel will:

- Investigate more alerts  
- Investigate alerts faster  
- Resolve more alerts  

compared to users using the traditional alert interface.

---

## 4. Dataset

- Falco Kubernetes alert logs  
- Simulated product analytics data:
  - alert views  
  - investigations  
  - remediations  

Data was processed using **BigQuery (SQL)** and visualized in **Tableau**.

---

## 5. Experiment Design

- **Control Group**: Traditional alert view  
- **Treatment Group**: Alert view with runtime context panel  

---

## 6. Metrics

### Primary
- **Investigation Rate** → % of alerts investigated  

### Secondary
- **Avg Time to Investigate (minutes)**  
- **Remediation Rate** → % of investigated alerts resolved  
- **Total Alerts Investigated** → engagement volume  

---

## 7. Results

### Investigation Rate

- Control: **56%**
- Treatment: **75%**

👉 Significant increase in engagement (+19 pp)

---

### Avg Time to Investigate

- Control: **59.3 min**
- Treatment: **60.2 min**

👉 No improvement in investigation speed

---

### Remediation Rate

- Control: **32.45%**
- Treatment: **38.58%**

👉 Slight improvement, but not strong enough to indicate meaningful impact

---

### Total Alerts Investigated

- Control: **384**
- Treatment: **548**

👉 Higher engagement in treatment group

---

## 8. Key Insights

- The runtime context panel significantly increases **user engagement**
- Users investigate more alerts when additional context is available
- However:
  - It does **not reduce investigation time**
  - It does **not strongly improve resolution outcomes**

👉 The feature improves **interaction**, but not **efficiency or effectiveness**

---

## 9. Recommendation

The runtime context panel should be **kept**, as it drives higher engagement.

However, further improvements should focus on:

- Reducing investigation time  
- Improving decision-making during investigations  
- Enhancing remediation workflows  

---

## 10. Dashboard

The Tableau dashboard includes:

- KPI summary (rate, time, remediation, volume)
- A/B comparison charts
- Top alert rules by volume (Falco alerts)

---

## 11. Tech Stack

- **SQL (BigQuery)** — data analysis  
- **Tableau** — visualization & storytelling  

---

## 12. Key Takeaway

> More context increases engagement,  
> but engagement alone does not guarantee better outcomes.

This highlights the importance of measuring both:
- behavioral metrics (interaction)
- outcome metrics (impact)
