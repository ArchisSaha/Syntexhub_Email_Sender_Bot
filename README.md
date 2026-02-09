\# 📧 Syntexhub Email Sender Bot



\*\*Project for SYNTECXHUB Internship Program\*\* | \*Week 3 Project Submission\*



\## 🎯 Project Overview

A Python-based automated email sender with CSV recipient management, attachment support, and retry logic.



\## ✨ Features

\- ✅ Automated Email Sending via SMTP

\- ✅ CSV Recipient Management

\- ✅ Personalized Messages with placeholders

\- ✅ Attachment Support

\- ✅ Retry Logic \& Detailed Logging

\- ✅ Secure Gmail Authentication



\## 📁 Files Included

\- `email\_sender\_bot.py` - Main Python script

\- `recipients.csv` - Sample recipient list

\- `requirements.txt` - Dependencies

\- `README.md` - This documentation

\- `LICENSE` - MIT License



\## 🚀 Quick Start



\### Installation

```bash

git clone https://github.com/YOUR\_USERNAME/Syntexhub\_Email\_Sender\_Bot.git

cd Syntexhub\_Email\_Sender\_Bot



Run the Bot

python email\_sender\_bot.py



CSV Format

email,name,company

john@example.com,John Doe,TechCorp

jane@example.com,Jane Smith,DataSystems



Sample Usage



==================================================

SYNTECXHUB - EMAIL SENDER BOT

==================================================

Enter your email: your.email@gmail.com

Enter app password: \*\*\*\*\*\*\*\*\*\*\*\*

Enter CSV path: recipients.csv

Enter subject: Hello {name}!

Enter body: Dear {name}, this is from {company}...



📊 Features Implemented



1. SMTP Integration - Uses smtplib with TLS
2. CSV Reading - Reads recipients from CSV files
3. Personalization - Uses {name}, {company} placeholders
4. Attachments - Supports multiple file types
5. Error Handling - Retry logic with exponential backoff
6. Logging - Comprehensive file and console logging



🔧 Technologies Used



* Python 3
* smtplib \& email libraries
* CSV module for data handling
* logging for error tracking



🤝 Contributing



This project is developed as a part of the SYNTECXHUB Internship Program.



