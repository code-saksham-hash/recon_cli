# DNS Recon Tool

A command-line DNS reconnaissance tool for enumerating subdomains, querying DNS records, and gathering network intelligence on a target domain.

---

## Features

- **ASN Lookup** — Resolves IP address, ASN, organization, country, city, and reverse DNS
- **DNS Records** — Queries A, MX, TXT, NS, and CNAME records
- **Subdomain Enumeration** — Passive discovery via crt.sh certificate transparency logs, with automatic retry
- **Brute Force Subdomains** — Active enumeration using a 60+ entry wordlist of common subdomain prefixes
- **Rich Terminal Output** — Color-coded, structured output powered by the Rich library

---

## Requirements

- Python 3.8+
- Internet access (for crt.sh and ipapi.co lookups)

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/code-saksham-hash/recon_cli.git
cd recon_cli
pip install -r requirements.txt
```

---

## Usage

```bash
python recon.py -d <target-domain>
```

**Example:**

```bash
python recon.py -d example.com
```

---

## Docker

Pull directly from Docker Hub:

```bash
docker pull saksham409/recon-tool
```

Or build the image locally:

```bash
docker build -t dns-recon-tool .
```

Run against a target:

```bash
docker run --rm dns-recon-tool -d example.com
```

---

## Project Structure

```
dns-recon-tool/
├── recon.py           # Main script
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container definition
└── README.md
```

---

## Dependencies

| Package     | Purpose                        |
|-------------|--------------------------------|
| dnspython   | DNS record resolution          |
| requests    | HTTP requests to crt.sh, ipapi |
| rich        | Terminal formatting and output |

---

## Disclaimer

This tool is intended for educational purposes and authorized security assessments only. Do not use it against domains you do not own or have explicit written permission to test. Unauthorized use may violate applicable laws.

---

## Author

**Saksham Banjade**
