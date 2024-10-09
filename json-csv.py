
Home Page Overview: The tool’s home page provides a comprehensive dashboard, offering users a quick summary of the total number of vulnerabilities and assets. Users can also view a prioritized list of vulnerabilities, helping them identify the most critical issues at a glance. This prioritization is based on severity, making it easier for users to focus on high-impact vulnerabilities immediately.

Immediate CVE Notification Handling: Users are able to review CVEs that require immediate attention, particularly new assets identified in the last 24 hours. The tool facilitates swift actions by allowing users to click a "Notify" button to ensure that the relevant teams are informed about these new vulnerabilities.

Automated Notification and Jira Integration: Upon clicking the "Notify" button, the tool automatically generates a Jira ticket and sends an email notification to the Information Technology Security Officer (ITSO). These notifications include detailed information about the CVE and associated assets, streamlining the communication and task management process.

Updating Remediation and Acknowledgments: The tool allows users to log any feedback from stakeholders, such as acknowledgments or remediation updates. For instance, if an image owner reports that a particular vulnerability has been remediated, the corresponding dates can be updated in the system. This feature also triggers notifications to workload owners who rely on these updates, prompting them to take any necessary actions based on the new information.

Handling False Positives: If a user determines that a CVE is a false positive, they can mark it as such within the tool. This ensures that future notifications regarding that CVE for the particular asset (tied to its unique eonid) will be suppressed, preventing unnecessary alerts and reducing noise for users.

Post-Remediation Asset Removal: Once users remediate the identified CVEs, the corresponding assets are removed from the Vulnerability Management and Reporting Console (VMARC) after a three-day period. This cleanup ensures that the tool reflects only the active vulnerabilities, providing a clearer and more up-to-date view of the organization's security posture.
