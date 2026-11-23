"""Legacy one-off generator (superseded).

index.html and the public/ pages have since been rebuilt by hand with the shared
assets/public-pages.css, assets/public-pages.js and assets/consent.js files.
Running this script would overwrite those pages with older content, so it now
refuses to run unless --force is passed.
"""
import os
import sys
import zipfile

if "--force" not in sys.argv:
    sys.exit("generate_barmm_files.py is superseded and would overwrite index.html and public/*.html. Re-run with --force to proceed anyway.")

print("Starting BARMM Labour Market Readiness file generation...")

# --- 1. UPDATE INDEX.HTML (SEO & Sidebar Navigation) ---
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

seo_tags = """<meta name="keywords" content="BARMM, Labour Market, SIPP, MTIT, Bangsamoro, Workforce, Investment, TVET, Mindanao, Economic Outlook, Policy Dashboard">
<meta property="og:title" content="BARMM Labour Market Readiness | MTIT">
<meta property="og:description" content="Evidence dashboard, SIPP workforce mapping and programme intelligence for the Bangsamoro Autonomous Region in Muslim Mindanao.">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/mtit-icon-192.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="BARMM Labour Market Readiness | MTIT">
<meta name="twitter:description" content="Evidence dashboard, SIPP workforce mapping and programme intelligence for the Bangsamoro Autonomous Region in Muslim Mindanao.">
<link rel="canonical" href="https://barmm-labour-market.gov.ph/">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "GovernmentOrganization",
  "name": "Ministry of Trade, Investments and Tourism (MTIT) - BARMM",
  "url": "https://barmm-labour-market.gov.ph/",
  "logo": "assets/mtit-icon-192.png",
  "description": "BARMM Labour Market Readiness platform providing evidence-led workforce intelligence and SIPP mapping.",
  "areaServed": {
    "@type": "AdministrativeArea",
    "name": "Bangsamoro Autonomous Region in Muslim Mindanao"
  }
}
</script>"""

html = html.replace('<meta name="description" content="BARMM Labour Market Readiness — evidence dashboard, SIPP workforce mapping and programme intelligence.">',
                    '<meta name="description" content="BARMM Labour Market Readiness — evidence dashboard, SIPP workforce mapping and programme intelligence.">\n' + seo_tags)

css_insert = """
.nav-dropdown{position:relative}
.nav-trigger{width:100%;justify-content:space-between}
.nav-trigger .arrow{transition:transform .2s;font-size:12px}
.nav-dropdown.open .nav-trigger .arrow{transform:rotate(180deg)}
.dropdown-menu{display:none;flex-direction:column;gap:2px;background:#082d22;border-radius:8px;padding:6px;margin-top:4px;border:1px solid #ffffff15}
.nav-dropdown.open .dropdown-menu{display:flex}
.dropdown-menu a{color:#d8e7df;text-decoration:none;padding:9px 12px 9px 42px;border-radius:6px;font-size:14px;display:flex;align-items:center;transition:background .2s}
.dropdown-menu a:hover{background:#ffffff19;color:#fff}
.nav a.nav-link{color:#d8e7df;text-decoration:none;padding:11px 12px;border-radius:9px;display:flex;align-items:center;gap:12px;font-size:15px}
.nav a.nav-link:hover{background:#ffffff19;color:#fff}
.nav a.nav-link span{width:19px;text-align:center;font-size:17px}
"""
html = html.replace('@media print{', css_insert + '\n@media print{')

old_sidebar = """ <button data-page="sipp"><span>⬡</span>SIPP Workforce Map</button>
 <button data-page="public/privacy-policy"><span>⬡</span>Privacy Policy</button>
 </nav>"""

new_sidebar = """ <button data-page="sipp"><span>⬡</span>SIPP Workforce Map</button>
 <a href="public/contact.html" class="nav-link"><span>✉</span>Contact Us</a>
 <div class="nav-dropdown" id="policyDropdown">
   <button class="nav-trigger" type="button"><span>🛡</span>Policies <span class="arrow">▾</span></button>
   <div class="dropdown-menu">
     <a href="public/terms-of-service.html">Terms of Service</a>
     <a href="public/privacy-policy.html">Privacy Policy</a>
     <a href="public/cookie-policy.html">Cookie Policy & Settings</a>
   </div>
 </div>
 </nav>"""
html = html.replace(old_sidebar, new_sidebar)

js_insert = """
$("#policyDropdown .nav-trigger").addEventListener("click", (e) => {
  e.stopPropagation();
  $("#policyDropdown").classList.toggle("open");
});
document.addEventListener("click", (e) => {
  const dropdown = $("#policyDropdown");
  if (dropdown && !dropdown.contains(e.target)) {
    dropdown.classList.remove("open");
  }
});
"""
html = html.replace('$$(".nav button").forEach(b=>b.addEventListener("click",()=>showPage(b.dataset.page)));',
                    js_insert + '\n$$(".nav button").forEach(b=>b.addEventListener("click",()=>showPage(b.dataset.page)));')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("✔ Updated index.html")

# --- 2. GENERATE PUBLIC PAGES ---
shared_css = """
:root{--green:#0b3d2e;--green2:#155b45;--green3:#237758;--mint:#e8f2ed;--gold:#c6a15b;--ink:#1d2b25;--muted:#69776f;--line:#e0e8e3;--bg:#f4f7f5;--white:#fff;--red:#b84a4a;--shadow:0 8px 28px rgba(12,48,35,.07)}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:"Roboto Condensed",Arial,sans-serif;font-size:16px;line-height:1.6}
h1,h2,h3{font-family:"Montserrat",sans-serif;color:var(--green);margin-top:0}
h1{font-size:clamp(24px,4vw,36px);font-weight:800;margin-bottom:10px}
h2{font-size:clamp(18px,2.5vw,24px);font-weight:700;margin-top:30px;margin-bottom:15px;border-bottom:2px solid var(--mint);padding-bottom:8px}
h3{font-size:18px;font-weight:600;color:var(--green2);margin-top:20px}
p{margin:0 0 16px;color:var(--ink)}
a{color:var(--green2);text-decoration:none;font-weight:600}
a:hover{text-decoration:underline;color:var(--green)}
.container{max-width:900px;margin:0 auto;padding:40px 20px}
header{background:var(--green);color:#fff;padding:20px 0;box-shadow:var(--shadow)}
.header-inner{max-width:1200px;margin:0 auto;padding:0 20px;display:flex;align-items:center;gap:15px}
.logo{width:50px;height:50px;background:#fff;border-radius:50%;display:grid;place-items:center;border:2px solid var(--gold);overflow:hidden}
.logo img{width:100%;height:100%;object-fit:cover}
.brand-text h1{color:#fff;font-size:18px;margin:0;letter-spacing:.5px}
.brand-text p{color:#b9d0c5;font-family:"Poppins",sans-serif;font-size:12px;margin:4px 0 0}
.card{background:var(--white);border:1px solid var(--line);border-radius:13px;box-shadow:var(--shadow);padding:30px;margin-bottom:24px}
.eyebrow{font:600 10px "Poppins",sans-serif;color:var(--green3);text-transform:uppercase;letter-spacing:1.2px;margin-bottom:8px}
ul,ol{padding-left:20px;margin-bottom:16px}
li{margin-bottom:8px}
footer{background:var(--green);color:#b9d0c5;padding:30px 0;margin-top:40px;font-size:14px;text-align:center}
footer a{color:var(--gold)}
.breadcrumb{font:600 11px "Poppins",sans-serif;color:var(--muted);text-transform:uppercase;letter-spacing:1px;margin-bottom:20px}
.breadcrumb a{color:var(--muted)}
.btn{display:inline-block;background:var(--green2);color:#fff;padding:12px 24px;border-radius:8px;font-family:"Poppins",sans-serif;font-weight:600;transition:filter .2s}
.btn:hover{filter:brightness(1.1);text-decoration:none}
.contact-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px;margin-top:20px}
.contact-item{background:var(--mint);padding:20px;border-radius:10px;border:1px solid var(--line)}
.contact-item h3{margin-top:0;color:var(--green)}
.notice{border-left:4px solid var(--gold);background:#fbf7ed;padding:16px 20px;color:#62502a;font-size:15px;border-radius:0 8px 8px 0;margin:20px 0}
@media(max-width:600px){.header-inner{flex-direction:column;text-align:center}.container{padding:20px 15px}}
"""

def page(title, desc, content):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{title} | BARMM Labour Market Readiness | MTIT</title><meta name="description" content="{desc}"><meta name="keywords" content="BARMM, MTIT, Bangsamoro, Labour Market, SIPP, Policy, Privacy, Terms, Contact"><meta property="og:title" content="{title} | BARMM Labour Market Readiness"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Poppins:wght@500;600;700&family=Roboto+Condensed:wght@400;500;600;700&display=swap" rel="stylesheet"><style>{shared_css}</style></head><body><header><div class="header-inner"><div class="logo"><img src="../assets/MTIT-logo.webp" alt="MTIT Logo"></div><div class="brand-text"><h1>BARMM LABOUR MARKET READINESS</h1><p>Workforce intelligence platform</p></div></div></header><main class="container"><div class="breadcrumb"><a href="../index.html">Home</a> / {title}</div>{content}</main><footer><p>&copy; 2026 Ministry of Trade, Investments and Tourism (MTIT) – Bureau of Investments<br>Bangsamoro Autonomous Region in Muslim Mindanao (BARMM)<br><a href="../index.html">Dashboard Home</a> | <a href="contact.html">Contact Us</a></p></footer></body></html>"""

contact_content = """
<div class="eyebrow">Get in Touch</div><h1>Contact Us</h1><p>We welcome inquiries from policymakers, researchers, development partners, and the public regarding the BARMM Labour Market Readiness platform, the Strategic Investment Priority Plan (SIPP), and regional workforce data.</p><div class="card"><h2>Platform & Data Inquiries</h2><p>For technical support, data methodology questions, or workbook integration requests, please reach out to the MTIT Data & Policy Support team.</p><div class="contact-grid"><div class="contact-item"><h3>📧 Email</h3><p><a href="mailto:labourmarket@mtit.barmm.gov.ph">labourmarket@mtit.barmm.gov.ph</a></p></div><div class="contact-item"><h3>📍 Office</h3><p>Ministry of Trade, Investments and Tourism<br>Bangsamoro Government Center<br>Cotabato City, BARMM</p></div></div></div><div class="card"><h2>Investment & SIPP Queries</h2><p>For questions regarding investment leads, SIPP tier classifications, and regional priority activities, please contact the Bureau of Investments (BOI) BARMM regional office.</p><p><a href="mailto:invest@boi.barmm.gov.ph" class="btn">Contact BOI BARMM</a></p></div><div class="notice"><strong>Note on Data Usage:</strong> The data presented in this dashboard is sourced from the Philippine Statistics Authority (PSA) and other validated regional workbooks. We do not collect primary survey data through this platform.</div>
"""

privacy_content = """
<div class="eyebrow">Legal & Compliance</div><h1>Privacy Policy</h1><p><em>Last Updated: November 2026</em></p><p>The Ministry of Trade, Investments and Tourism (MTIT) respects your privacy and is committed to protecting the personal data you share while interacting with the BARMM Labour Market Readiness platform. This policy outlines how we handle information in compliance with the Data Privacy Act of 2012 (Republic Act No. 10173).</p><div class="card"><h2>1. Information We Collect</h2><p>This platform is designed as a <strong>local-first, read-only evidence dashboard</strong>. We do not require user accounts, nor do we collect personal identifiable information (PII) to access the core labour market data.</p><h3>Local Storage Data</h3><p>If you use the "Project Register" feature to save local investment or workforce notes, this data is stored exclusively in your browser's IndexedDB or localStorage. <strong>No data is transmitted to our servers.</strong></p><h3>Analytics & Usage</h3><p>We may use anonymized, aggregated analytics to understand platform usage and improve regional policy support. This data cannot be traced back to individual users.</p></div><div class="card"><h2>2. How We Use Information</h2><ul><li>To maintain the functionality and security of the platform.</li><li>To respond to direct inquiries submitted via our Contact page.</li><li>To generate aggregated, non-identifiable reports on regional workforce trends.</li></ul></div><div class="card"><h2>3. Data Sharing & Disclosure</h2><p>We do not sell, trade, or rent your personal information. Data is only shared with authorized BARMM government agencies for statutory policy formulation, strictly adhering to data privacy regulations.</p></div><div class="card"><h2>4. Your Rights</h2><p>Under the Data Privacy Act, you have the right to access, correct, or request the deletion of any personal information we may hold (e.g., if you contacted us directly via email). To exercise these rights, please contact our Data Protection Officer at <a href="mailto:privacy@mtit.barmm.gov.ph">privacy@mtit.barmm.gov.ph</a>.</p></div>
"""

terms_content = """
<div class="eyebrow">Legal & Compliance</div><h1>Terms of Service</h1><p><em>Last Updated: November 2026</em></p><p>Welcome to the BARMM Labour Market Readiness platform. By accessing or using this dashboard, you agree to comply with the following terms and conditions set forth by the Ministry of Trade, Investments and Tourism (MTIT).</p><div class="card"><h2>1. Purpose of the Platform</h2><p>This platform provides evidence-based labour market intelligence, SIPP workforce mapping, and economic indicators to support strategic investment and policy formulation in the Bangsamoro Autonomous Region in Muslim Mindanao (BARMM).</p></div><div class="card"><h2>2. Data Accuracy & Interpretation</h2><p>The data presented is sourced from the Philippine Statistics Authority (PSA), regional workbooks, and validated institutional records. While we strive for accuracy:</p><ul><li>Indicators are subject to revision and methodological updates by source agencies.</li><li>Investment leads and SIPP mappings represent strategic priorities and early market signals, not guaranteed capital expenditures or confirmed job vacancies.</li><li>Users are responsible for their own interpretation of the data for academic, commercial, or policy research.</li></ul></div><div class="card"><h2>3. Intellectual Property</h2><p>All dashboard designs, visualizations, and proprietary code are the intellectual property of MTIT and the Bangsamoro Government. Source data remains the property of the respective originating agencies (e.g., PSA). You may cite and share insights from this platform for non-commercial, public-interest purposes provided proper attribution is given.</p></div><div class="card"><h2>4. Acceptable Use</h2><p>You agree not to use this platform to:</p><ul><li>Scrape, data-mine, or use automated bots to extract bulk datasets without prior written authorization.</li><li>Misrepresent the data to spread misinformation regarding regional economic stability.</li><li>Attempt to breach the local-storage security or application architecture.</li></ul></div><div class="card"><h2>5. Limitation of Liability</h2><p>The MTIT and the Bangsamoro Government shall not be held liable for any direct or indirect investment decisions, financial losses, or policy outcomes resulting from the use of the data provided on this platform.</p></div>
"""

cookie_content = """
<div class="eyebrow">Legal & Compliance</div><h1>Cookie Policy & Settings</h1><p><em>Last Updated: November 2026</em></p><p>This policy explains how the BARMM Labour Market Readiness platform uses cookies and local browser storage technologies to ensure a seamless and secure user experience.</p><div class="card"><h2>1. What Are Cookies & Local Storage?</h2><p>Cookies are small text files stored on your device. Local Storage (and IndexedDB) are similar technologies that allow web applications to save data directly in your browser for offline access and state management.</p></div><div class="card"><h2>2. How We Use Local Storage</h2><p>This platform is designed with a <strong>privacy-first, local-data architecture</strong>. We do not use third-party tracking cookies or advertising networks.</p><h3>Essential Storage (Required)</h3><ul><li><strong>Application State:</strong> Remembers your current view, filters, and chart preferences.</li><li><strong>Project Register:</strong> Saves your locally added investment and workforce project records securely in your browser's IndexedDB.</li><li><strong>Service Worker Cache:</strong> Allows the dashboard to load faster and function offline (Progressive Web App capabilities).</li></ul></div><div class="card"><h2>3. Managing Your Settings</h2><p>Because we do not use tracking cookies, there is no "cookie banner" or opt-out mechanism required. However, you have full control over your local data:</p><ul><li><strong>Clear Local Records:</strong> You can delete your saved Project Register entries at any time by navigating to <em>Data & Sources</em> and clicking "Reset local project records".</li><li><strong>Browser Settings:</strong> You can clear your browser's cache and local storage via your browser's privacy settings. Note that doing so will erase any locally saved projects.</li></ul></div><div class="card"><h2>4. Third-Party Services</h2><p>We utilize open-source charting libraries (Chart.js) and web fonts (Google Fonts). These services operate under their own privacy policies and do not track your activity across our dashboard.</p></div>
"""

os.makedirs('public', exist_ok=True)

with open('public/contact.html', 'w', encoding='utf-8') as f:
    f.write(page("Contact Us", "Contact the MTIT BARMM Labour Market Readiness team for data, SIPP, and workforce inquiries.", contact_content))
print("✔ Generated public/contact.html")

with open('public/privacy-policy.html', 'w', encoding='utf-8') as f:
    f.write(page("Privacy Policy", "Read the MTIT BARMM privacy policy regarding data handling, local storage, and user rights.", privacy_content))
print("✔ Generated public/privacy-policy.html")

with open('public/terms-of-service.html', 'w', encoding='utf-8') as f:
    f.write(page("Terms of Service", "Terms of service for using the BARMM Labour Market Readiness platform and data.", terms_content))
print("✔ Generated public/terms-of-service.html")

with open('public/cookie-policy.html', 'w', encoding='utf-8') as f:
    f.write(page("Cookie Policy", "Cookie and local storage policy for the BARMM Labour Market Readiness platform.", cookie_content))
print("✔ Generated public/cookie-policy.html")

# --- 3. CREATE ZIP ARCHIVE ---
with zipfile.ZipFile('barmm-labor-market-updates.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('index.html')
    zipf.write('public/contact.html')
    zipf.write('public/privacy-policy.html')
    zipf.write('public/terms-of-service.html')
    zipf.write('public/cookie-policy.html')

print("\n✅ Success! 'barmm-labor-market-updates.zip' has been created in your directory.")
