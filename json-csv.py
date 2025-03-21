
TOI Vulnerability Management (VM) Process
The TOI Vulnerability Management (VM) process aligns with the existing enterprise vulnerability management workflows. This ensures consistency, integration with established tools, and operational efficiency across the infrastructure.

1. Scanning Infrastructure
The VM process begins with two existing vulnerability scanning tools (Tool1 and Tool2) that perform automated scans on cloud and on-premise infrastructure. These tools assess the systems for known vulnerabilities on a scheduled basis or on demand.

2. Data Ingestion and Processing
Once scans are completed:

The tools expose scan results via APIs.
Custom scripts are used to retrieve these scan results and publish them to Kafka topics for further processing.
3. Consumption by Analysis Platforms
The scan data from Kafka topics is consumed by:

Splunk: For visualization, alerting, and dashboarding.
Platform Tool: Used for deeper analysis, enrichment, and automation.
4. Ownership Mapping
To determine asset ownership:

The scan data is mapped against IT Asset Management (ITAM) data.
This correlation provides accurate ownership information for each asset with vulnerabilities.
5. Notification and Remediation
With asset ownership established:

The VM Operations team triggers automated email notifications to the respective asset owners.
These notifications include details about detected vulnerabilities and required remediation actions.
