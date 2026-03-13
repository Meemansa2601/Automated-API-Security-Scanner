from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn
import time

app = FastAPI()

# --- SECURITY GATEKEEPER (CORS) ---
# This allows your index.html to communicate with this Python server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SECURITY KNOWLEDGE BASE ---
KNOWLEDGE_BASE = {
    "http": {
        "test": "Insecure Protocol (HTTP)",
        "status": "🔴 Critical",
        "color": "#ef4444",
        "risk": "Data is sent in plain text. Hackers can intercept passwords via Man-in-the-Middle attacks.",
        "fix": "Enforce HTTPS and install an SSL certificate (use Let's Encrypt)."
    },
    "rate_limit": {
        "test": "Rate Limit Missing",
        "status": "🔴 Critical",
        "color": "#ef4444",
        "risk": "No request speed limit detected. Attackers can crash the API or use Brute Force to guess passwords.",
        "fix": "Implement a rate limiter to block users who send more than 10-20 requests per minute."
    },
    "server_header": {
        "test": "Server Header Exposure",
        "status": "🟡 Medium",
        "color": "#f59e0b",
        "risk": "The API reveals exactly what software the server is running (e.g., 'Apache/2.4'). This helps hackers find specific software exploits.",
        "fix": "Configure the server to hide the 'Server' and 'X-Powered-By' headers."
    },
    "discovery": {
        "test": "Endpoint Auto-Discovery",
        "status": "⚠️ Exposed",
        "color": "#f59e0b",
        "risk": "Common hidden paths (like /admin or /config) were found. These are often targeted first by attackers.",
        "fix": "Disable directory listing and restrict access to administrative paths using IP whitelisting."
    }
}

@app.get("/scan")
def scan_api(url: str):
    # Ensure the URL has a scheme
    if not url.startswith("http"):
        url = "http://" + url
        
    results = []
    score = 100

    # 1. HTTPS Check
    if not url.startswith("https"):
        results.append(KNOWLEDGE_BASE["http"])
        score -= 30
    
    # 2. Rate Limit Test (5 rapid requests)
    success_count = 0
    for _ in range(5):
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200: success_count += 1
        except: pass
    
    if success_count >= 5:
        results.append(KNOWLEDGE_BASE["rate_limit"])
        score -= 30

    # 3. Server Header Check
    try:
        r = requests.get(url, timeout=2)
        if "Server" in r.headers:
            results.append(KNOWLEDGE_BASE["server_header"])
            score -= 10
    except: pass

    # 4. Endpoint Auto-Discovery (The Hacker Feature)
    common_paths = ["/admin", "/login", "/api", "/config", "/.env", "/debug", "/test"]
    discovered = []
    base_url = url.rstrip('/')

    for path in common_paths:
        try:
            # We check if the path exists by looking at the status code
            check_url = base_url + path
            r = requests.get(check_url, timeout=1)
            if r.status_code in [200, 403, 401]:
                discovered.append(path)
        except:
            continue

    if discovered:
        discovery_report = KNOWLEDGE_BASE["discovery"].copy()
        discovery_report["risk"] = f"Exposed paths found: {', '.join(discovered)}. These are prime targets for reconnaissance."
        results.append(discovery_report)
        score -= 20

    # If the API is perfect
    if not results:
        results.append({
            "test": "Final Security Audit",
            "status": "✅ Passed",
            "color": "#10b981",
            "risk": "No common vulnerabilities detected in the basic scan. The API appears to follow baseline security standards.",
            "fix": "Keep your server software updated and perform deep penetration tests monthly."
        })

    # Add a small delay so the UI loader looks realistic
    time.sleep(1.5)

    return {"score": max(0, score), "reports": results}

if __name__ == "__main__":
    print("🚀 Sentinel Scanner Backend is booting up...")
    uvicorn.run(app, host="127.0.0.1", port=8000)