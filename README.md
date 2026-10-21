# 🛡️ PhishGuard — Educational Phishing URL Analyzer

A beginner-friendly cybersecurity dashboard built with **Python** and **Streamlit**.  
It checks a URL's *text* for common phishing warning signs and returns a **Low / Medium / High** risk estimate.

> ⚠️ **This is an educational estimate only.**  
> PhishGuard does **not** visit or fetch the URL.  
> It cannot guarantee a URL is safe or malicious.

---

## Features

| Check | What it looks for |
|---|---|
| Raw IP address | `http://192.168.1.1/…` instead of a domain name |
| URL shortener | `bit.ly`, `tinyurl.com`, `t.co`, and more |
| Long URL | More than 75 characters |
| Excessive subdomains | More than 3 dots in the domain |
| `@` symbol | Hides the real destination |
| Missing HTTPS | Unencrypted connection |
| Phishing keywords | `login`, `verify`, `banking`, `password`, etc. |

---

## How to Run

### 1 — Install Python
Download from <https://python.org> (3.9 or newer recommended).

### 2 — Install Streamlit
```bash
pip install streamlit
```
Or use the requirements file:
```bash
pip install -r requirements.txt
```

### 3 — Start the app
```bash
streamlit run app.py
```

Your browser will open automatically at **http://localhost:8501**.

---

## Project Structure

```
PhishGuard/
├── app.py            ← All application code (single file)
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## Disclaimer

PhishGuard is intended **for educational purposes only**.  
Always use professional security tools (e.g., [VirusTotal](https://www.virustotal.com)) for real threat detection.
