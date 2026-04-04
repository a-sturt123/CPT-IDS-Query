# Project Proposal

## 1. Project Identification
- Project Title: CPT IDS Query
- Course: Process Automation and Shell Script
- Term: Spring 2026
- Student Name(s): Ayden Sturtevant, Darian Mongiovi
- Primary Contact: Discord
- Proposed Start Date: Pending Project Approval
- Proposed End Date: TBD

---

## 2. Project Selection & Motivation
The motivation for this project revolves around bringing the concepts we've learned with automation, APIs, and database management together for a user application.
We are proposing a Discord bot that will help users interact with a database of network traffic, providing insight for CPT/security students to become familiar with network traffic logs.

As computer tech students we feel this is a great project for showcasing what we've learned while potentially providing a unique service for future students.

Professionally this is a project that will show our team's ability to remain agile and manage complex programming tasks.

---

## 3. Problem Statement

As of right now, students within the CPT program currently have no way to view or analyze the traffic within the CPT environment. While tools like Wireshark
or IDS systems can capture this data, they are not ideal for user friendliness or everyday use.

Additionally, students have no way of understanding network usage patterns such as peak traffic times, which can impact performance when they are trying to
complete a lab or use a platform like Cengage. Without this type of information, it makes it hard for students to work around high traffic periods which can potentially lead to slower performance and a less efficient workflow. This also limits opportunities for cybersecurity students to perform basic SOC-style analysis on real or structured network data.


---

## 4. Proposed Solution Overview
We are proposing a virtual environment where and instance of wire shark can run, and databases are populated with specific traffic relevant to intrusion detection.
Tools such as Tshark and PostgreSQL will collect traffic data and populate an SQL database accordingly. Rules will have to be made to filter large ammounts of data, and queries will have to be desinged to give users a veriaty of options to pull data.

Include:
- We intend to build and data collection pipeline, and a discord bot that allows students to pull data as needed.
- Network traffic data collection, Data cleaning, Database Population.

---

## 5. Technical Stack & Tools

- Operating System(s): CPT Internal Linux Machine
- Programming Language(s): Python, SQL
- Frameworks / Libraries: pandas, requests, scapy (or something similar), SQLAlchemy, Discord.py
- Databases / Storage: PostgreSQL (primary). SQLite (for testing)
- Infrastructure (VMs, containers, etc.): CPT Internal VM environment
- Tools (Git, CI, monitoring, APIs, etc.): Git, VS Code, Discord API

---

## 6. Prerequisite Knowledge & Skills

I have experience with Python, SQL, SQLAlchemy, Discord bots, Linux, and Git from prior coursework and personal projects. My Network Security, Cybersecurity, and Server Administration classes have also given me a solid background for the network side of this project. The main thing I need to pick up is Scapy, which I plan to tackle early on. -Ayden

Networking is my main focus as a student. I have insights into network traffic and what to look for when it comes to malicious traffic, and intrusion detection. I also have a lot of practice using python and sql as a student. -Darian

---

## 7. Project Scope & Deliverables

Minimum Viable Product (MVP):
- Collect or use network traffic data from the CPT environment
- Clean and structure the data using Python
- Store the data in a database
- Discord bot that allows users to query traffic data

Required Deliverables:
- Python scripts for data collection and processing
- Working Discord bot with query commands
- Database schema and population logic
- Basic documentation for setup and usage

Optional Stretch Goals:
- Visualization of traffic patterns (graphs or charts)
- More advanced query filters (time ranges, protocols)
- Near real time data updates

---

## 8. Milestones & Timeline

- Phase 1: Deploy Tshark and begin collecting/cleaning data.
- Phase 2: Design SQL database and population scripts
- Phase 3: Test Discord bot and basic queries.
- Phase 4: Deploy bot with full scope of query options.

---

## 9. Risks, Constraints & Dependencies

Technical Risks:
- Limited access to real network traffic data
- Difficulty capturing or filtering traffic accurately

Time Constraints:
- Limited timeframe to design, build, and test the system

Dependencies:
- Access to CPT internal network or sample traffic data
- Database credentials and permissions
- Discord bot token and server access

Mitigation Strategies:
- Use sample or logged data if live capture is restricted
- Start with simple queries and expand if time allows

---

## 10. Security, Ethics & Safety Considerations
Address any relevant concerns, such as:
- Authentication: We need scope of available data.
- Data sensitivity: We need to ensure that traffic data in no way compromises security.
- Network exposure: We are proposing a network scanner for inbound traffic, to ensure only public data is used.
- Automation: Ensure automation isnt compromised (SQL injection considerations)
- Ethical considerations: Privacy


---

## 11. Team Structure (If Applicable)

- Roles are very equal, we both hold responsibility for working on code and making suggestions on overall structure

- Currently we are using discord to communicate about initial structures. A github repository will be set up to handle code revisions

- Simple voting to resolve any ambiguity issues. Goals are very cleared and structured. We will stick to a set of packages and tools to avoid technical conflicts

- The project can be parsed out into different functions needed so members can focus on strong suits weather it be sql, python, or web apis

---

## 12. Documentation & Knowledge Transfer Plan
Explain how this project will be documented.  Please note that this should include documentation in the UVDesk knowledgebase at the very least.  Programming projects should include readme.md files. 

Include:
- README or user documentation
- Deployment or maintenance guides
- How another student or administrator could continue the project

---

## 13. Faculty/cpt.internal Resources Requested

- Access to CPT internal VM environment
- PostgreSQL database credentials
- Discord bot token and server access
- Permission to access or use network traffic data (if required)

---

## 14. Acknowledgement of Expectations
By submitting this proposal, I acknowledge that:
- This is a self-directed technical project
- I am responsible for research and troubleshooting
- Evaluation will consider process, documentation, and professionalism

**Signature (Name & Date):**

Student 1:  __Ayden Sturtevant__________________________ Date: _____4-1-26__________
Student 2:  ____________________________ Date: _______________
Student 3:  ____________________________ Date: _______________
Student 4:  ____________________________ Date: _______________

Instructor: ____________________________ Date: _______________
