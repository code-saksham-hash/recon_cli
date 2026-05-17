import dns.resolver
import requests
import argparse
import socket
from rich.console import Console

console = Console()

# ---- 1. DNS Query ----
def dns_query(domain):
    records = {}
    for rtype in ['A', 'MX', 'TXT', 'NS', 'CNAME']:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            records[rtype] = [str(r) for r in answers]
        except:
            records[rtype] = []
    return records

# ---- 2. crt.sh with retry ----
def crt_subdomains(domain):
    for attempt in range(3):  # retry 3 times
        try:
            url = f"https://crt.sh/?q=%25.{domain}&output=json"
            res = requests.get(url, timeout=15)
            if res.status_code != 200:
                continue
            data = res.json()
            subdomains = set()
            for entry in data:
                name = entry['name_value']
                for sub in name.split('\n'):
                    sub = sub.strip()
                    if domain in sub and '*' not in sub:
                        subdomains.add(sub)
            return sorted(subdomains)
        except Exception as e:
            console.print(f"  [red]crt.sh attempt {attempt+1} failed: {e}[/red]")
    return []

# ---- 3. Bigger Brute Force ----
def bruteforce(domain):
    wordlist = [
        'www', 'mail', 'dev', 'api', 'staging', 'admin', 'blog',
        'shop', 'app', 'vpn', 'remote', 'test', 'portal', 'cdn',
        'ftp', 'smtp', 'pop', 'imap', 'webmail', 'mx', 'ns1', 'ns2',
        'static', 'media', 'images', 'assets', 'beta', 'alpha',
        'dashboard', 'login', 'auth', 'secure', 'payments', 'pay',
        'gateway', 'internal', 'intranet', 'corp', 'office', 'git',
        'gitlab', 'github', 'jenkins', 'ci', 'jira', 'confluence',
        'support', 'help', 'docs', 'status', 'monitor', 'grafana',
        'prometheus', 'kibana', 'elastic', 'redis', 'db', 'database',
        'mysql', 'postgres', 'mongo', 'api2', 'v1', 'v2', 'old',
        'new', 'cloud', 'mobile', 'android', 'ios', 'web', 'proxy'
    ]
    found = []
    for word in wordlist:
        subdomain = f"{word}.{domain}"
        try:
            dns.resolver.resolve(subdomain, 'A')
            found.append(subdomain)
        except:
            pass
    return found

# ---- 4. ASN Lookup ----
def asn_lookup(domain):
    try:
        ip = socket.gethostbyname(domain)
        res = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10)
        data = res.json()
        return {
            'ip': ip,
            'asn': data.get('asn', 'N/A'),
            'org': data.get('org', 'N/A'),
            'country': data.get('country_name', 'N/A'),
            'city': data.get('city', 'N/A')
        }
    except:
        return None

# ---- 5. Reverse DNS ----
def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return 'N/A'

# ---- Main ----
def main():
    parser = argparse.ArgumentParser(description='DNS Recon Tool')
    parser.add_argument('-d', '--domain', required=True, help='Target domain')
    args = parser.parse_args()
    domain = args.domain

    console.print(f"\n[bold cyan]Recon started on: {domain}[/bold cyan]\n")

    # ASN Info
    console.print("[bold yellow]ASN Info:[/bold yellow]")
    asn = asn_lookup(domain)
    if asn:
        console.print(f"  [green]IP[/green]      → {asn['ip']}")
        console.print(f"  [green]ASN[/green]     → {asn['asn']}")
        console.print(f"  [green]Org[/green]     → {asn['org']}")
        console.print(f"  [green]Country[/green] → {asn['country']}")
        console.print(f"  [green]City[/green]    → {asn['city']}")
        console.print(f"  [green]RevDNS[/green]  → {reverse_dns(asn['ip'])}")

    # DNS Records
    console.print("\n[bold yellow]DNS Records:[/bold yellow]")
    records = dns_query(domain)
    for rtype, values in records.items():
        if values:
            for v in values:
                console.print(f"  [green]{rtype}[/green] → {v}")

    # crt.sh
    console.print("\n[bold yellow]Subdomains from crt.sh:[/bold yellow]")
    subs = crt_subdomains(domain)
    if subs:
        for s in subs:
            console.print(f"  [green]→[/green] {s}")
    else:
        console.print("  [red]None found[/red]")

    # Brute force
    console.print("\n[bold yellow]Brute Force Results:[/bold yellow]")
    bf = bruteforce(domain)
    if bf:
        for s in bf:
            console.print(f"  [green]→[/green] {s}")
    else:
        console.print("  [red]None found[/red]")

    console.print("\n[bold cyan]Done![/bold cyan]\n")

if __name__ == "__main__":
    main()