import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn

app = FastAPI()

# --- SECURITY GATEKEEPER ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- THE ANALYST KNOWLEDGE BASE ---
KNOWLEDGE_BASE = {
    "http": {
        "test": "Transport Security Audit",
        "status": "🔴 Critical",
        "color": "#ef4444",
        "analogy": "Sending a postcard through the mail. Anyone who touches it can read exactly what you wrote.",
        "risk": "Data is sent in plain text via HTTP. Hackers can intercept passwords via Man-in-the-Middle attacks.",
        "fix": "Enforce HTTPS and install an SSL certificate (e.g., Let's Encrypt)."
    },
    "rate_limit": {
        "test": "Brute Force Simulation",
        "status": "🔴 Critical",
        "color": "#ef4444",
        "analogy": "A door that lets a thief try 10,000 keys a second until one finally fits.",
        "risk": "API allowed rapid login attempts without blocking. This confirms a lack of Rate Limiting.",
        "fix": "Implement a '429 Too Many Requests' response to throttle automated traffic."
    },
    "server_header": {
        "test": "Information Leakage",
        "status": "🟡 Medium",
        "color": "#f59e0b",
        "analogy": "Leaving a blueprint of your house's security system sitting on the front lawn.",
        "risk": "The API reveals server software versions (e.g., Apache/IIS), helping hackers find specific exploits.",
        "fix": "Configure the server to hide the 'Server' and 'X-Powered-By' headers."
    },
    "discovery": {
        "test": "Endpoint Auto-Discovery",
        "status": "⚠️ Exposed",
        "color": "#f59e0b",
        "analogy": "Having a 'Secret Back Door' that isn't actually locked.",
        "risk": "Hidden paths (like /admin or /config) were found publicly available via reconnaissance.",
        "fix": "Disable directory listing and restrict administrative paths to internal IP addresses."
    }
}

# --- UPGRADED ASYNC CHATBOT (Expert Brain) ---
@app.get("/chat")
async def chat_bot(msg: str):
    msg = msg.lower()
    await asyncio.sleep(0.4) 

    if "brute force" in msg or "rate limit" in msg:
        return {
            "reply": "🛡️ **Preventive Measure:** Use the 'SlowAPI' library.\n\n"
                     "**Code Example (FastAPI):**\n"
                     "```python\nfrom slowapi import Limiter\n"
                     "limiter = Limiter(key_func=get_remote_address)\n\n"
                     "@app.post('/login')\n"
                     "@limiter.limit('5/minute')\n"
                     "async def login():\n"
                     "    return {'msg': 'Protected'}\n```"
        }

    if "https" in msg or "http" in msg or "protocol" in msg:
        return {
            "reply": "🔒 **Recommended Fix:** Enforce SSL at the server level.\n"
                     "If using FastAPI, add this middleware to force HTTPS:\n\n"
                     "```python\nfrom fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware\n\n"
                     "app.add_middleware(HTTPSRedirectMiddleware)\n```"
        }

    if "header" in msg or "server info" in msg or "talking" in msg:
        return {
            "reply": "🚫 **How to Fix Information Leakage:**\n\n"
                     "1. **Nginx:** Add `server_tokens off;` to your config.\n"
                     "2. **Apache:** Set `ServerTokens Prod` and `ServerSignature Off`.\n"
                     "3. **FastAPI:** Start uvicorn with: `uvicorn app:app --no-server-header`"
        }

    if "admin" in msg or "discovery" in msg:
        return {
            "reply": "🚪 **Preventive Measure:** Move your admin panel to a custom UUID path (e.g., `/admin-7b2-x91`) and use IP Whitelisting so only your office IP can access it."
        }

    return {"reply": "I am your Security Analyst. Ask me about the risks I found, or say 'Give me code for the Brute Force fix'!"}

# --- ASYNC SCANNER ENDPOINT ---
@app.get("/scan")
async def scan_api(url: str):
    if not url.startswith("http"): url = "http://" + url
    base_url = url.rstrip('/')
    results, score = [], 100

    # 1. Transport Security Audit
    if not url.startswith("https"):
        results.append(KNOWLEDGE_BASE["http"]); score -= 30

    # 2. Brute Force Simulation
    attack_success = 0
    blocked = False
    for _ in range(5):
        try:
            r = requests.post(f"{base_url}/login", data={'u':'admin','p':'123'}, timeout=1)
            if r.status_code == 429:
                blocked = True; break
            attack_success += 1
        except: pass
    if not blocked and attack_success > 2:
        results.append(KNOWLEDGE_BASE["rate_limit"]); score -= 30

    # 3. Information Leakage
    try:
        r = requests.get(base_url, timeout=2)
        if "Server" in r.headers:
            results.append(KNOWLEDGE_BASE["server_header"]); score -= 10
    except: pass

    # 4. Endpoint Auto-Discovery
    common_paths = ["/admin", "/login", "/config", "/.env"]
    found = []
    for path in common_paths:
        try:
            r = requests.get(base_url + path, timeout=1)
            if r.status_code in [200, 401, 403]: found.append(path)
        except: continue
    if found:
        report = KNOWLEDGE_BASE["discovery"].copy()
        report["risk"] = f"Exposed paths found: {', '.join(found)}."; results.append(report); score -= 20

    if not results:
        results.append({"test": "General Audit", "status": "✅ Passed", "color": "#10b981", "analogy": "A well-guarded fortress.", "risk": "No baseline vulnerabilities found.", "fix": "Regular maintenance."})

    await asyncio.sleep(2.0) 
    return {"score": max(0, score), "reports": results}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)