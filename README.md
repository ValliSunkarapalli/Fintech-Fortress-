🛡️ Advanced Framework for Spoofing Detection and Recovery

Multi Layered Anomaly Detection and Adaptive Learning in FinTech

🏆 Distinguished Project – Texas A&M University-Corpus Christi

📌 Overview

This FinTech cybersecurity project addresses a major threat in financial systems — spoofing attacks — by introducing a multi-layered detection and recovery framework. It combines traditional rule-based detection, machine learning models, and adaptive learning with behavioral biometrics to identify and mitigate attacks in real time.

🎯 Key Highlights

Rule Based Detection for fast anomaly identification

Machine Learning Models:

Support Vector Machine (SVM)

Isolation Forest

Random Forest

Behavioral Biometrics using Keystroke Dynamics

Few Shot & Zero Shot Learning for detecting unknown threats

Automated Recovery Logic to mitigate active spoofing attacks

🧰 Tech Stack

Languages: Python

Libraries: Scikit-learn, Pandas, NumPy, Matplotlib

Network Analysis: Scapy, PyShark

Database: SQLite

Containerization: Docker

Dataset: UNSW-NB15

🗂️ Project Structure

├── data/                    # Dataset files (processed & raw)
├── models/                  # ML model training & saved models
├── keystroke/               # Keystroke dynamics module
├── src/                     # Core detection & recovery logic
├── recovery/                # Adaptive threat mitigation logic
├── Dockerfile               # Container setup
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation

🔄 How It Works

Data Collection: Use Scapy and PyShark for network traffic capture

Preprocessing: Clean and transform using Pandas & NumPy

Detection Layer: Apply ML models for anomaly detection

Behavioral Layer: Validate users with keystroke biometrics

Adaptive Layer: React to new threats using few/zero shot learning

Recovery: Initiate automatic defense actions

