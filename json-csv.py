Slide 1: TOI Vulnerability Management - Overview
Objective:
To align TOI VM with existing vulnerability management processes for efficient risk identification and notification.

Key Components:

Scanning Tools
Data Ingestion (Kafka)
Analysis Platforms (Splunk, Platform Tool)
Ownership Mapping (ITAM)
Notifications to Asset Owners
Slide 2: Step 1 – Vulnerability Scanning
Tools Involved: Tool1 & Tool2

Perform regular scans across infrastructure.
Identify vulnerabilities on cloud and on-prem environments.
Output:

Raw scan results made available through APIs.
Slide 3: Step 2 – Data Ingestion via Kafka
Scripts:

Retrieve scan results via API.
Publish data into Kafka topics.
Why Kafka?

Reliable, scalable, and asynchronous data streaming.
Slide 4: Step 3 – Data Consumption & Analysis
Consumers of Kafka Topics:

Splunk: For dashboards, alerts, and search queries.
Platform Tool: For deeper correlation and reporting.
Goal:

Centralize and normalize scan data.
Slide 5: Step 4 – Ownership Mapping via ITAM
Action:

Scan data is enriched by mapping to ITAM (IT Asset Management).
Purpose:

Identify the correct asset owners responsible for remediation.
Slide 6: Step 5 – Notifications & Remediation
VM Operations Team:

Sends automated email notifications to respective owners.
Emails include vulnerability details and remediation guidance.
Outcome:

Timely awareness and action by responsible teams.
