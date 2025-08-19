import whois
import dns.resolver
import requests
import json
import socket
from datetime import datetime
import os
import sys
import time
import subprocess
import shutil
import re
import threading
import concurrent.futures
import hashlib
import base64
import ssl
import urllib3
from urllib.parse import urljoin, urlparse, quote
from collections import deque
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import csv
import argparse

# Optional imports for advanced features
try:
    import nmap
    NMAP_AVAILABLE = True
except ImportError:
    NMAP_AVAILABLE = False

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

# ANSI color codes for hacker style
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DARK = '\033[90m'
    GREEN_BG = '\033[42m'
    RED_BG = '\033[41m'
    BLINK = '\033[5m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_mask():
    mask = (
        f"{Colors.OKGREEN}{Colors.BOLD}"
        "             .o oOOOOOOOo                                            OOOo\n"
        "             Ob.OOOOOOOo  OOOo.      oOOo.                      .adOOOOOOO\n"
        "             OboO\"\"\"\"\"\"\"\"\"\"\".OOo. .oOOOOOo.    OOOo.oOOOOOo..\"\"\"\"\"\"\"\"'OO\n"
        "             OOP.oOOOOOOOOOOO `\"POOOOOOOOOOOo.   `\"OOOOOOOOOP,OOOOOOOOOOOB'\n"
        "             `O'OOOO'     `OOOOo\"OOOOOOOOOOO` .adOOOOOOOOO\"oOOO'    `OOOOo\n"
        "             .OOOO'            `OOOOOOOOOOOOOOOOOOOOOOOOOO'            `OO\n"
        "             OOOOO                 '\"OOOOOOOOOOOOOOOO\"`                oOO\n"
        "            oOOOOOba.                .adOOOOOOOOOOba               .adOOOOo.\n"
        "           oOOOOOOOOOOOOOba.    .adOOOOOOOOOO@^OOOOOOOba     .adOOOOOOOOOOOO\n"
        "          OOOOOOOOOOOOOOOOO.OOOOOOOOOOOOOO\"`  '\"OOOOOOOOOOOOO.OOOOOOOOOOOOOO\n"
        "          `\"OOOO\"       \"YOoOOOOMOIONODOO\"`  .   `\"OOROAOPOEOOOoOY\"     \"OOO\"\n"
        "             Y           'OOOOOOOOOOOOOO: .oOOo. :OOOOOOOOOOO?'         :`\n"
        "             :            .oO%OOOOOOOOOOo.OOOOOO.oOOOOOOOOOOOO?\n"
        "                          oOOP\"%OOOOOOOOoOOOOOOO?oOOOOO?OOOO\"OOo\n"
        "                          '%o  OOOO\"%OOOO%\"%OOOOO\"OOOOOO\"OOO':\n"
        "                               `$\"  `OOOO' `O\"Y ' `OOOO'  o\n"
        "                                      OP\"          : o\n"
        f"{Colors.ENDC}"
    )
    print(mask)

def print_hacker_banner():
    banner = (
        f"{Colors.RED_BG}{Colors.BOLD}{Colors.HEADER}"
        "╔══════════════════════════════════════════════════════════════╗\n"
        "║                     ANONYMOUS OSINT TOOL                     ║\n"
        "║                    Advanced Reconnaissance                   ║\n"
        "║                     [ WE ARE LEGION ]                        ║\n"
        "╚══════════════════════════════════════════════════════════════╝"
        f"{Colors.ENDC}"
    )
    print(banner)

try:
    import sublist3r
    SUBLIST3R_AVAILABLE = True
except ImportError:
    SUBLIST3R_AVAILABLE = False

try:
    from theHarvester.lib import __main__ as harvester
    HARVESTER_AVAILABLE = True
except ImportError:
    HARVESTER_AVAILABLE = False

try:
    import racon
    RACON_AVAILABLE = True
except ImportError:
    RACON_AVAILABLE = False

try:
    import scrapy
    from scrapy.crawler import CrawlerProcess
    SPIDER_AVAILABLE = True
except ImportError:
    SPIDER_AVAILABLE = False

class OSINTCollector:
    def __init__(self, domain):
        self.domain = domain
        self.results = {
            "domain": domain,
            "timestamp": datetime.now().isoformat(),
            "whois": {},
            "dns": {},
            "subdomains": [],
            "ports": [],
            "social_media": [],
            "emails": [],
            "headers": {},
            "racon": {},
            "spider": [],
            "vulnerabilities": [],
            "technologies": [],
            "certificates": {},
            "directory_enum": [],
            "api_endpoints": [],
            "backup_files": [],
            "cloud_services": [],
            "reverse_ip": [],
            "dns_zone_transfer": {},
            "email_servers": [],
            "web_technologies": {},
            "security_headers": {},
            "robots_txt": {},
            "sitemap": {},
            "js_files": [],
            "forms": [],
            "comments": [],
            "metadata": {}
        }

    def whois_lookup(self):
        print(f"{Colors.OKCYAN}[+] Performing WHOIS lookup...{Colors.ENDC}")
        try:
            w = whois.whois(self.domain)
            self.results["whois"] = {
                "registrar": str(w.registrar) if w.registrar else "N/A",
                "creation_date": str(w.creation_date) if w.creation_date else "N/A",
                "expiration_date": str(w.expiration_date) if w.expiration_date else "N/A",
                "name_servers": list(w.name_servers) if w.name_servers else [],
                "emails": list(w.emails) if w.emails else []
            }
            print(f"{Colors.OKGREEN}[+] WHOIS Results:{Colors.ENDC}")
            print(Colors.OKGREEN + json.dumps(self.results["whois"], indent=2) + Colors.ENDC)
        except Exception as e:
            print(f"{Colors.FAIL}[-] WHOIS error: {e}{Colors.ENDC}")

    def dns_lookup(self):
        print(f"\n{Colors.OKCYAN}[+] Performing DNS lookup...{Colors.ENDC}")
        record_types = ['A', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        dns_results = {}
        
        for record in record_types:
            try:
                answers = dns.resolver.resolve(self.domain, record)
                dns_results[record] = [str(rdata) for rdata in answers]
                print(f"{Colors.OKGREEN}[{record}] Records:{Colors.ENDC}")
                for rdata in dns_results[record]:
                    print(f"  {Colors.OKBLUE}{rdata}{Colors.ENDC}")
            except Exception as e:
                dns_results[record] = []
                print(f"{Colors.WARNING}[{record}] Not found or error: {e}{Colors.ENDC}")
        
        self.results["dns"] = dns_results

    def crtsh_enum(self):
        print(f"\n{Colors.OKCYAN}[+] Searching subdomains via crt.sh...{Colors.ENDC}")
        url = f"https://crt.sh/?q=%25.{self.domain}&output=json"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                subdomains = set()
                for entry in data:
                    name = entry.get("name_value")
                    if name:
                        names = name.split('\n')
                        for n in names:
                            if not n.startswith("*") and n.endswith(self.domain):
                                subdomains.add(n.strip())
                self.results["subdomains"].extend(list(subdomains))
                print(f"{Colors.OKGREEN}[+] Found {len(subdomains)} unique subdomains:{Colors.ENDC}")
                for sub in sorted(subdomains)[:20]:
                    print(f"  {Colors.OKBLUE}{sub}{Colors.ENDC}")
                if len(subdomains) > 20:
                    print(f"  {Colors.DARK}... and {len(subdomains) - 20} more subdomains{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}[-] Failed to access crt.sh{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}[-] crt.sh error: {e}{Colors.ENDC}")

    def subdomain_enum(self):
        print(f"\n{Colors.OKCYAN}[+] Searching subdomains via Sublist3r...{Colors.ENDC}")
        if not SUBLIST3R_AVAILABLE:
            print(f"{Colors.FAIL}[-] Sublist3r not available. Install with: pip install sublist3r{Colors.ENDC}")
            return
            
        try:
            # Sublist3r requires savefile and enable_bruteforce parameters
            subdomains = sublist3r.main(self.domain, 'subdomains.txt', enable_bruteforce=False, engines=None, verbose=False, silent=True)
            if subdomains:
                unique_subs = list(set(subdomains))
                self.results["subdomains"].extend(unique_subs)
                print(f"{Colors.OKGREEN}[+] Sublist3r found {len(unique_subs)} subdomains:{Colors.ENDC}")
                for sub in sorted(unique_subs)[:15]:
                    print(f"  {Colors.OKBLUE}{sub}{Colors.ENDC}")
                if len(unique_subs) > 15:
                    print(f"  {Colors.DARK}... and {len(unique_subs) - 15} more subdomains{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}[-] No subdomains found via Sublist3r{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}[-] Sublist3r error: {e}{Colors.ENDC}")
            print(f"{Colors.DARK}  Note: Make sure Sublist3r is up to date. Install with: pip install --upgrade sublist3r{Colors.ENDC}")

    def port_scan(self):
        print(f"\n{Colors.OKCYAN}[+] Performing basic port scanning...{Colors.ENDC}")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5900, 8080]
        open_ports = []
        
        try:
            ip = socket.gethostbyname(self.domain)
            print(f"{Colors.OKGREEN}[+] IP Address: {Colors.OKBLUE}{ip}{Colors.ENDC}")
            
            for port in common_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"  {Colors.OKGREEN}Port {port}: OPEN{Colors.ENDC}")
                sock.close()
            
            self.results["ports"] = open_ports
        except Exception as e:
            print(f"{Colors.FAIL}[-] Port scanning error: {e}{Colors.ENDC}")

    def get_http_headers(self):
        print(f"\n{Colors.OKCYAN}[+] Retrieving HTTP headers...{Colors.ENDC}")
        try:
            response = requests.get(f"http://{self.domain}", timeout=5)
            headers = dict(response.headers)
            self.results["headers"] = headers
            
            print(f"{Colors.OKGREEN}[+] HTTP Headers:{Colors.ENDC}")
            for key, value in headers.items():
                print(f"  {Colors.OKBLUE}{key}{Colors.ENDC}: {Colors.DARK}{value}{Colors.ENDC}")
                
        except Exception as e:
            print(f"{Colors.FAIL}[-] HTTP headers error: {e}{Colors.ENDC}")

    def social_media_search(self):
        print(f"\n{Colors.OKCYAN}[+] Searching for social media presence...{Colors.ENDC}")
        social_platforms = {
            "twitter": f"https://twitter.com/search?q={self.domain}",
            "linkedin": f"https://linkedin.com/search/results/all/?keywords={self.domain}",
            "github": f"https://github.com/search?q={self.domain}"
        }
        
        print(f"{Colors.OKGREEN}[+] Possible social media profiles:{Colors.ENDC}")
        for platform, url in social_platforms.items():
            print(f"  {Colors.OKBLUE}{platform}{Colors.ENDC}: {Colors.DARK}{url}{Colors.ENDC}")
            self.results["social_media"].append({"platform": platform, "url": url})

    def email_harvesting(self):
        print(f"\n{Colors.OKCYAN}[+] Performing email harvesting...{Colors.ENDC}")
        if "emails" in self.results["whois"]:
            emails = self.results["whois"]["emails"]
            if emails:
                self.results["emails"].extend(emails)
                print(f"{Colors.OKGREEN}[+] Emails found from WHOIS:{Colors.ENDC}")
                for email in emails:
                    print(f"  {Colors.OKBLUE}{email}{Colors.ENDC}")

    def racon_scan(self):
        print(f"\n{Colors.OKCYAN}[+] Running Raccoon Recon (CLI) if available...{Colors.ENDC}")
        raccoon_path = shutil.which("raccoon") or shutil.which("raccoon.exe")
        output = {"tool": "raccoon", "available": bool(raccoon_path)}
        try:
            if raccoon_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                out_dir = os.path.join(os.getcwd(), f"raccoon_out_{self.domain}_{timestamp}")
                os.makedirs(out_dir, exist_ok=True)
                cmd = [raccoon_path, "-t", self.domain, "-o", out_dir]
                print(f"{Colors.DARK}$ {' '.join(cmd)}{Colors.ENDC}")
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
                output.update({
                    "returncode": proc.returncode,
                    "stdout": proc.stdout[-2000:],
                    "stderr": proc.stderr[-2000:],
                    "output_dir": out_dir
                })
                if proc.returncode == 0:
                    print(f"{Colors.OKGREEN}[+] Raccoon completed. Output in: {out_dir}{Colors.ENDC}")
                else:
                    print(f"{Colors.WARNING}[!] Raccoon exit code {proc.returncode}. Check stderr in results.{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}[!] Raccoon CLI not found. Install with: pip install raccoon-scanner{Colors.ENDC}")
                output.update({
                    "note": "Raccoon CLI not found in PATH."
                })
        except Exception as e:
            print(f"{Colors.FAIL}[-] raccoon error: {e}{Colors.ENDC}")
            output.update({"error": str(e)})
        self.results["racon"] = output

    def spider_scan(self):
        print(f"\n{Colors.OKCYAN}[+] Running spider (web crawler)...{Colors.ENDC}")
        # If Scrapy is available, use it; otherwise, fallback to simple BFS crawler
        if SPIDER_AVAILABLE:
            try:
                from scrapy.spiders import Spider
                from scrapy.http import Request

                class SimpleSpider(Spider):
                    name = "simplespider"
                    custom_settings = {'LOG_ENABLED': False}
                    start_urls = [f"http://{self.domain}"]
                    found_urls = set()

                    def parse(self, response):
                        urls = response.css('a::attr(href)').getall()
                        for url in urls:
                            if url.startswith("http"):
                                if url not in self.found_urls:
                                    self.found_urls.add(url)
                                    yield {"url": url}
                                    yield Request(url, callback=self.parse)

                process = CrawlerProcess(settings={'LOG_ENABLED': False})
                spider = SimpleSpider
                spider.domain = self.domain
                items = []

                def collect_item(item):
                    items.append(item)

                process.crawl(spider)
                process.start()
                print(f"{Colors.OKGREEN}[+] Spider (Scrapy) completed.{Colors.ENDC}")
                found_urls = list(getattr(spider, 'found_urls', []))
                self.results["spider"] = found_urls
                
                # Display found URLs
                if found_urls:
                    print(f"\n{Colors.OKCYAN}[+] URLs found:{Colors.ENDC}")
                    for i, url in enumerate(found_urls[:50], 1):  # Show first 50
                        print(f"  {Colors.OKBLUE}{i:2d}.{Colors.ENDC} {Colors.DARK}{url}{Colors.ENDC}")
                    if len(found_urls) > 50:
                        print(f"  {Colors.WARNING}... and {len(found_urls) - 50} more URLs{Colors.ENDC}")
                return
            except Exception as e:
                print(f"{Colors.WARNING}[!] Scrapy error, fallback to simple BFS: {e}{Colors.ENDC}")

        # Fallback simple BFS crawler
        try:
            max_pages = 50
            start_urls = [f"http://{self.domain}", f"https://{self.domain}"]
            visited = set()
            found = []
            queue = deque(start_urls)
            domain = self.domain

            def is_same_domain(url: str) -> bool:
                try:
                    netloc = urlparse(url).netloc.lower()
                    return netloc.endswith(domain.lower())
                except Exception:
                    return False

            headers = {"User-Agent": "Mozilla/5.0 (compatible; OSINTSpider/1.0)"}

            while queue and len(visited) < max_pages:
                current = queue.popleft()
                if current in visited:
                    continue
                visited.add(current)
                try:
                    resp = requests.get(current, headers=headers, timeout=8, verify=False)
                except Exception:
                    continue
                if not resp.ok:
                    continue
                # Extract hrefs using regex
                for href in re.findall(r'href=[\"\'](.*?)[\"\']', resp.text, flags=re.IGNORECASE):
                    if href.startswith('javascript:') or href.startswith('#') or href.startswith('mailto:'):
                        continue
                    absolute = urljoin(current, href)
                    if absolute.startswith('http') and is_same_domain(absolute):
                        if absolute not in visited and absolute not in queue:
                            queue.append(absolute)
                            found.append(absolute)
                # Limit number of URLs stored
                if len(found) >= 200:
                    break

            self.results["spider"] = list(dict.fromkeys(found))  # unique with order
            print(f"{Colors.OKGREEN}[+] Spider (fallback) completed. URLs found: {len(self.results['spider'])}{Colors.ENDC}")
            
            # Display found URLs
            print(f"\n{Colors.OKCYAN}[+] URLs found:{Colors.ENDC}")
            for i, url in enumerate(self.results["spider"][:50], 1):  # Show first 50
                print(f"  {Colors.OKBLUE}{i:2d}.{Colors.ENDC} {Colors.DARK}{url}{Colors.ENDC}")
            if len(self.results["spider"]) > 50:
                print(f"  {Colors.WARNING}... and {len(self.results['spider']) - 50} more URLs{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}[-] Spider fallback error: {e}{Colors.ENDC}")

    def advanced_port_scan(self):
        """Advanced port scanning with nmap"""
        print(f"\n{Colors.OKCYAN}[+] Performing advanced port scanning...{Colors.ENDC}")
        if not NMAP_AVAILABLE:
            print(f"{Colors.WARNING}[-] Nmap not available. Install with: pip install python-nmap{Colors.ENDC}")
            return
            
        try:
            nm = nmap.PortScanner()
            ip = socket.gethostbyname(self.domain)
            print(f"{Colors.OKGREEN}[+] Scanning IP: {Colors.OKBLUE}{ip}{Colors.ENDC}")
            
            # Scan common ports with service detection
            nm.scan(ip, '21-23,25,53,80,110,111,135,139,143,443,993,995,1723,3306,3389,5900,8080,8443', arguments='-sS -sV --version-intensity 5')
            
            open_ports = []
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    for port in ports:
                        service = nm[host][proto][port]
                        open_ports.append({
                            'port': port,
                            'service': service.get('name', 'unknown'),
                            'version': service.get('version', 'unknown'),
                            'state': service.get('state', 'unknown')
                        })
                        print(f"  {Colors.OKGREEN}Port {port}: {service.get('name', 'unknown')} - {service.get('version', 'unknown')}{Colors.ENDC}")
            
            self.results["ports"] = open_ports
        except Exception as e:
            print(f"{Colors.FAIL}[-] Advanced port scan error: {e}{Colors.ENDC}")

    def ssl_certificate_analysis(self):
        """SSL certificate analysis"""
        print(f"\n{Colors.OKCYAN}[+] Analyzing SSL certificate...{Colors.ENDC}")
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    self.results["certificates"] = {
                        "subject": dict(x[0] for x in cert['subject']),
                        "issuer": dict(x[0] for x in cert['issuer']),
                        "version": cert['version'],
                        "serial_number": cert['serialNumber'],
                        "not_before": cert['notBefore'],
                        "not_after": cert['notAfter'],
                        "san": cert.get('subjectAltName', [])
                    }
                    
                    print(f"{Colors.OKGREEN}[+] SSL Certificate Info:{Colors.ENDC}")
                    print(f"  {Colors.OKBLUE}Subject:{Colors.ENDC} {cert['subject']}")
                    print(f"  {Colors.OKBLUE}Issuer:{Colors.ENDC} {cert['issuer']}")
                    print(f"  {Colors.OKBLUE}Valid Until:{Colors.ENDC} {cert['notAfter']}")
                    
        except Exception as e:
            print(f"{Colors.FAIL}[-] SSL analysis error: {e}{Colors.ENDC}")

    def directory_enumeration(self):
        """Directory enumeration"""
        print(f"\n{Colors.OKCYAN}[+] Performing directory enumeration...{Colors.ENDC}")
        common_dirs = [
            'admin', 'administrator', 'backup', 'config', 'db', 'database', 'dev', 'development',
            'files', 'ftp', 'images', 'img', 'includes', 'install', 'js', 'lib', 'library',
            'log', 'logs', 'media', 'mysql', 'old', 'php', 'phpmyadmin', 'plugins', 'private',
            'public', 'scripts', 'src', 'sql', 'static', 'stats', 'temp', 'test', 'tmp', 'upload',
            'uploads', 'user', 'users', 'web', 'webadmin', 'webmail', 'wordpress', 'wp-admin',
            'wp-content', 'wp-includes', 'xml', 'api', 'v1', 'v2', 'rest', 'swagger', 'docs'
        ]
        
        found_dirs = []
        base_url = f"http://{self.domain}"
        
        def check_dir(dir_name):
            try:
                url = f"{base_url}/{dir_name}"
                response = requests.get(url, timeout=5, allow_redirects=False)
                if response.status_code in [200, 301, 302, 403]:
                    return {"dir": dir_name, "status": response.status_code, "url": url}
            except:
                pass
            return None
        
        # Multi-threaded directory checking
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_dir = {executor.submit(check_dir, dir_name): dir_name for dir_name in common_dirs}
            for future in concurrent.futures.as_completed(future_to_dir):
                result = future.result()
                if result:
                    found_dirs.append(result)
                    print(f"  {Colors.OKGREEN}[{result['status']}] {result['dir']}{Colors.ENDC}")
        
        self.results["directory_enum"] = found_dirs

    def technology_detection(self):
        """Web technology detection"""
        print(f"\n{Colors.OKCYAN}[+] Detecting web technologies...{Colors.ENDC}")
        try:
            response = requests.get(f"http://{self.domain}", timeout=10)
            headers = response.headers
            html = response.text
            
            technologies = []
            
            # Check headers for technologies
            if 'X-Powered-By' in headers:
                technologies.append(f"Server: {headers['X-Powered-By']}")
            if 'Server' in headers:
                technologies.append(f"Server: {headers['Server']}")
            
            # Check HTML for common technologies
            tech_patterns = {
                'WordPress': r'wp-content|wp-includes|wordpress',
                'Drupal': r'drupal|Drupal',
                'Joomla': r'joomla|Joomla',
                'Laravel': r'laravel|Laravel',
                'React': r'react|React',
                'Angular': r'angular|Angular',
                'Vue.js': r'vue|Vue',
                'jQuery': r'jquery|jQuery',
                'Bootstrap': r'bootstrap|Bootstrap',
                'PHP': r'\.php|PHP',
                'ASP.NET': r'\.aspx|\.asp|ASP\.NET',
                'Python': r'python|Python|\.py',
                'Node.js': r'node|Node\.js',
                'Apache': r'apache|Apache',
                'Nginx': r'nginx|Nginx',
                'IIS': r'iis|IIS'
            }
            
            for tech, pattern in tech_patterns.items():
                if re.search(pattern, html, re.IGNORECASE):
                    technologies.append(tech)
            
            self.results["technologies"] = list(set(technologies))
            
            print(f"{Colors.OKGREEN}[+] Technologies detected:{Colors.ENDC}")
            for tech in self.results["technologies"]:
                print(f"  {Colors.OKBLUE}{tech}{Colors.ENDC}")
                
        except Exception as e:
            print(f"{Colors.FAIL}[-] Technology detection error: {e}{Colors.ENDC}")

    def security_headers_check(self):
        """Check security headers"""
        print(f"\n{Colors.OKCYAN}[+] Checking security headers...{Colors.ENDC}")
        try:
            response = requests.get(f"https://{self.domain}", timeout=10)
            headers = response.headers
            
            security_headers = {
                'X-Frame-Options': headers.get('X-Frame-Options', 'Not Set'),
                'X-Content-Type-Options': headers.get('X-Content-Type-Options', 'Not Set'),
                'X-XSS-Protection': headers.get('X-XSS-Protection', 'Not Set'),
                'Strict-Transport-Security': headers.get('Strict-Transport-Security', 'Not Set'),
                'Content-Security-Policy': headers.get('Content-Security-Policy', 'Not Set'),
                'Referrer-Policy': headers.get('Referrer-Policy', 'Not Set'),
                'Permissions-Policy': headers.get('Permissions-Policy', 'Not Set')
            }
            
            self.results["security_headers"] = security_headers
            
            print(f"{Colors.OKGREEN}[+] Security Headers:{Colors.ENDC}")
            for header, value in security_headers.items():
                status = f"{Colors.OKGREEN}✓{Colors.ENDC}" if value != 'Not Set' else f"{Colors.FAIL}✗{Colors.ENDC}"
                print(f"  {status} {Colors.OKBLUE}{header}{Colors.ENDC}: {Colors.DARK}{value}{Colors.ENDC}")
                
        except Exception as e:
            print(f"{Colors.FAIL}[-] Security headers check error: {e}{Colors.ENDC}")

    def robots_txt_analysis(self):
        """Analyze robots.txt"""
        print(f"\n{Colors.OKCYAN}[+] Analyzing robots.txt...{Colors.ENDC}")
        try:
            response = requests.get(f"http://{self.domain}/robots.txt", timeout=10)
            if response.status_code == 200:
                robots_content = response.text
                self.results["robots_txt"] = {
                    "content": robots_content,
                    "disallow": re.findall(r'Disallow:\s*(.+)', robots_content, re.IGNORECASE),
                    "allow": re.findall(r'Allow:\s*(.+)', robots_content, re.IGNORECASE),
                    "sitemap": re.findall(r'Sitemap:\s*(.+)', robots_content, re.IGNORECASE)
                }
                
                print(f"{Colors.OKGREEN}[+] Robots.txt found:{Colors.ENDC}")
                if self.results["robots_txt"]["disallow"]:
                    print(f"  {Colors.WARNING}Disallow:{Colors.ENDC}")
                    for path in self.results["robots_txt"]["disallow"]:
                        print(f"    {Colors.DARK}{path}{Colors.ENDC}")
                if self.results["robots_txt"]["sitemap"]:
                    print(f"  {Colors.OKBLUE}Sitemap:{Colors.ENDC}")
                    for sitemap in self.results["robots_txt"]["sitemap"]:
                        print(f"    {Colors.DARK}{sitemap}{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}[-] Robots.txt not found{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}[-] Robots.txt analysis error: {e}{Colors.ENDC}")

    def save_results(self, filename=None):
        if not filename:
            filename = f"osint_results_{self.domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n{Colors.OKGREEN}[+] Results saved to: {filename}{Colors.ENDC}")

    def run_all(self):
        print(f"{Colors.HEADER}{Colors.BOLD}[+] Starting OSINT for domain: {self.domain}{Colors.ENDC}")
        print(f"{Colors.DARK}{'='*50}{Colors.ENDC}")
        
        # Basic reconnaissance
        self.whois_lookup()
        self.dns_lookup()
        self.crtsh_enum()
        self.subdomain_enum()
        
        # Network scanning
        self.port_scan()
        self.advanced_port_scan()
        self.ssl_certificate_analysis()
        
        # Web analysis
        self.get_http_headers()
        self.security_headers_check()
        self.technology_detection()
        self.robots_txt_analysis()
        self.directory_enumeration()
        
        # Information gathering
        self.social_media_search()
        self.email_harvesting()
        self.racon_scan()
        self.spider_scan()
        
        print(f"\n{Colors.DARK}{'='*50}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}[+] OSINT finished!{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}📊 Summary:{Colors.ENDC}")
        print(f"  {Colors.OKCYAN}Subdomains found: {len(set(self.results['subdomains']))}{Colors.ENDC}")
        print(f"  {Colors.OKCYAN}Open ports: {len(self.results['ports'])}{Colors.ENDC}")
        print(f"  {Colors.OKCYAN}Emails found: {len(set(self.results['emails']))}{Colors.ENDC}")
        print(f"  {Colors.OKCYAN}Technologies: {len(self.results['technologies'])}{Colors.ENDC}")
        print(f"  {Colors.OKCYAN}Directories: {len(self.results['directory_enum'])}{Colors.ENDC}")
        print(f"  {Colors.OKCYAN}Security headers: {len([h for h in self.results['security_headers'].values() if h != 'Not Set'])}{Colors.ENDC}")

def main():
    clear_screen()
    print_ascii_mask()
    print_hacker_banner()
    print(f"{Colors.DARK}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKGREEN}ANONYMOUS OSINT TOOL - Interactive Menu{Colors.ENDC}")
    print(f"{Colors.DARK}{'='*60}{Colors.ENDC}")
    
    if len(sys.argv) < 2:
        domain = input(f"{Colors.OKCYAN}Enter target domain (e.g. example.com): {Colors.ENDC}").strip()
    else:
        domain = sys.argv[1]
    
    collector = OSINTCollector(domain)
    options = [
        ("WHOIS Lookup", collector.whois_lookup),
        ("DNS Lookup", collector.dns_lookup),
        ("Subdomain via crt.sh", collector.crtsh_enum),
        ("Subdomain via Sublist3r", collector.subdomain_enum if SUBLIST3R_AVAILABLE else None),
        ("Basic Port Scan", collector.port_scan),
        ("Advanced Port Scan (Nmap)", collector.advanced_port_scan),
        ("SSL Certificate Analysis", collector.ssl_certificate_analysis),
        ("HTTP Headers", collector.get_http_headers),
        ("Security Headers Check", collector.security_headers_check),
        ("Technology Detection", collector.technology_detection),
        ("Directory Enumeration", collector.directory_enumeration),
        ("Robots.txt Analysis", collector.robots_txt_analysis),
        ("Social Media Search", collector.social_media_search),
        ("Email Harvesting", collector.email_harvesting),
        ("Racon (Recon Automation)", collector.racon_scan),
        ("Spider (Web Crawler)", collector.spider_scan),
        ("Run ALL (FULL SCAN)", collector.run_all),
        ("Save results to file", collector.save_results),
        ("Exit", None)
    ]
    
    while True:
        print(f"\n{Colors.BOLD}{Colors.OKCYAN}Select an option:{Colors.ENDC}")
        for idx, (desc, func) in enumerate(options, 1):
            if func is None and desc == "Subdomain via Sublist3r":
                print(f" {Colors.DARK}{idx}. {desc} (Sublist3r not available){Colors.ENDC}")
            elif func is None and desc == "Racon (Recon Automation)":
                print(f" {Colors.DARK}{idx}. {desc} (racon not available){Colors.ENDC}")
            elif func is None and desc == "Spider (Web Crawler)":
                print(f" {Colors.DARK}{idx}. {desc} (scrapy/spider not available){Colors.ENDC}")
            elif func is None and desc == "Advanced Port Scan (Nmap)":
                print(f" {Colors.DARK}{idx}. {desc} (nmap not available){Colors.ENDC}")
            else:
                print(f" {Colors.OKGREEN}{idx}. {desc}{Colors.ENDC}")
        
        try:
            choice = input(f"{Colors.OKCYAN}Enter option number: {Colors.ENDC}").strip()
            if not choice.isdigit():
                print(f"{Colors.WARNING}Input must be a number.{Colors.ENDC}")
                continue
            choice = int(choice)
            if choice < 1 or choice > len(options):
                print(f"{Colors.WARNING}Invalid option.{Colors.ENDC}")
                continue
            if options[choice-1][1] is None:
                if options[choice-1][0] == "Exit":
                    print(f"{Colors.DARK}Exiting...{Colors.ENDC}")
                    break
                else:
                    print(f"{Colors.WARNING}Feature not available.{Colors.ENDC}")
                    continue
            if options[choice-1][0] == "Save results to file":
                filename = input(f"{Colors.OKCYAN}Output filename (leave blank for auto): {Colors.ENDC}").strip()
                collector.save_results(filename if filename else None)
            else:
                options[choice-1][1]()
        except KeyboardInterrupt:
            print(f"\n{Colors.DARK}Exiting...{Colors.ENDC}")
            break
        except Exception as e:
            print(f"{Colors.FAIL}An error occurred: {e}{Colors.ENDC}")

if __name__ == "__main__":
    main() 
