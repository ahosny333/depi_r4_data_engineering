# Generator Monitoring IoT Platform — Backend

A data engineering project that scrapes, cleans, and centralizes job postings from multiple platforms into a single, searchable dashboard.

## Project Structure

```
project/
│
├── app.py                            ← flask app
|
├── scraping scripts/                 ← python scripts for web scraping  
│   └── arabjob_web_scraping.py        
│   └── Bayt_and_Adzona_jobs.py               
│   └── forsna web scraping.py               
│   └── naukrigulf.py               
│   └── Tanqeeb.py               
│   └── wuzzuf.py                     ← Simulates ESP32 without hardware
│
├── templates/                        ← web pages
├── requirements.txt
└── jobs.csv                          ← table for all jobs  
```

---

## Quick Start

### 1. Clone the repo
```bash
git clone https://github.com
```

### 2. Install dependencies
```bash
cd project
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Start the backend
```bash
python app.py
```
