
Overview:
The TOI Vulnerability Management process aligns with existing enterprise VM workflows to ensure consistent detection, ownership, and remediation of vulnerabilities.

Process Flow:

Scanning

Tool1 and Tool2 scan infrastructure.
Scan results made available via APIs.
Data Ingestion

Scripts fetch scan data.
Data is pushed to Kafka topics.
Data Consumption

Splunk and Platform Tool consume Kafka data for analysis and dashboards.
Ownership Mapping

Scan results are enriched using ITAM data to identify asset owners.
Notification

VM Operations team sends email notifications to respective asset owners for remediation.
