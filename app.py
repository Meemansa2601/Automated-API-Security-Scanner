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
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# --- THE ANALYST KNOWLEDGE BASE ---
KNOWLEDGE_BASE = {
    "http": {
        "test": "Transport Security Audit",
        "status": "",
        "color": "#ef4444",
        "analogy": "Sending a postcard through the mail. Anyone who touches it can read exactly what you wrote.",
        "risk": "Data is sent in plain text via HTTP. Hackers can intercept passwords via Man-in-the-Middle attacks.",
        "fix": "Enforce HTTPS and install an SSL certificate (e.g., Let's Encrypt)."
    },
    "rate_limit": {
        "test": "Brute Force Simulation",
        "status": "",
        "color": "#ef4444",
        "analogy": "A door that lets a thief try 10,000 keys a second until one finally fits.",
        "risk": "API allowed rapid login attempts without blocking. This confirms a lack of Rate Limiting.",
        "fix": "Implement a '429 Too Many Requests' response to throttle automated traffic."
    },
    "server_header": {
        "test": "Information Leakage",
        "status": "",
        "color": "#f59e0b",
        "analogy": "Leaving a blueprint of your house's security system sitting on the front lawn.",
        "risk": "The API reveals server software versions (e.g., Apache/IIS), helping hackers find specific exploits.",
        "fix": "Configure the server to hide the 'Server' and 'X-Powered-By' headers."
    },
    "discovery": {
        "test": "Endpoint Auto-Discovery",
        "status": "",
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

    # Explanation responses
    if "explain" in msg and ("brute force" in msg or "rate limit" in msg):
        return {
            "reply": "🔍 **Brute Force Simulation Explained:**\n\n"
                     "This test attempts multiple rapid login attempts to check if your API properly blocks repeated failed authentication attempts.\n\n"
                     "**What it tests:**\n"
                     "• Rate limiting implementation\n"
                     "• Account lockout mechanisms\n"
                     "• IP-based throttling\n"
                     "• Response to repeated failures\n\n"
                     "**Why it matters:** Without rate limiting, attackers can try thousands of password combinations per minute to break into user accounts."
        }

    if "explain" in msg and ("http" in msg or "https" in msg or "protocol" in msg):
        return {
            "reply": "🔍 **Transport Security Audit Explained:**\n\n"
                     "This test checks if your API uses HTTPS encryption to protect data transmitted between clients and your server.\n\n"
                     "**What it tests:**\n"
                     "• SSL/TLS certificate presence\n"
                     "• Encryption protocol version\n"
                     "• Secure data transmission\n"
                     "• Protection against eavesdropping\n\n"
                     "**Why it matters:** HTTP sends all data in plain text, allowing anyone on the network to read sensitive information like passwords and API keys."
        }

    if "explain" in msg and ("header" in msg or "server info" in msg or "talking" in msg):
        return {
            "reply": "🔍 **Information Leakage Explained:**\n\n"
                     "This test analyzes HTTP headers to identify if your server is revealing sensitive technical information.\n\n"
                     "**What it tests:**\n"
                     "• Server software version (Apache, Nginx, etc.)\n"
                     "• Programming language/framework details\n"
                     "• System architecture information\n"
                     "• Debug information exposure\n\n"
                     "**Why it matters:** Revealing server details helps attackers find specific vulnerabilities for your exact software version and configuration."
        }

    if "explain" in msg and ("admin" in msg or "discovery" in msg):
        return {
            "reply": "🔍 **Endpoint Auto-Discovery Explained:**\n\n"
                     "This test probes common administrative and sensitive paths to check if they're improperly exposed.\n\n"
                     "**What it tests:**\n"
                     "• Common admin panel paths (/admin, /admin/login)\n"
                     "• Configuration endpoints (/config, /settings)\n"
                     "• Debug and development routes\n"
                     "• Sensitive file access (/.env, /config.php)\n\n"
                     "**Why it matters:** Exposed administrative interfaces provide direct access to system controls and sensitive data."
        }

    # Code fix responses (preventive measures)
    if ("fix" in msg or "prevent" in msg or "solve" in msg) and ("brute force" in msg or "rate limit" in msg):
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

    if ("fix" in msg or "prevent" in msg or "solve" in msg) and ("https" in msg or "http" in msg or "protocol" in msg):
        return {
            "reply": "🔒 **Recommended Fix:** Enforce SSL at the server level.\n"
                     "If using FastAPI, add this middleware to force HTTPS:\n\n"
                     "```python\nfrom fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware\n\n"
                     "app.add_middleware(HTTPSRedirectMiddleware)\n```"
        }

    if ("fix" in msg or "prevent" in msg or "solve" in msg) and ("header" in msg or "server info" in msg or "talking" in msg):
        return {
            "reply": "🚫 **How to Fix Information Leakage:**\n\n"
                     "1. **Nginx:** Add `server_tokens off;` to your config.\n"
                     "2. **Apache:** Set `ServerTokens Prod` and `ServerSignature Off`.\n"
                     "3. **FastAPI:** Start uvicorn with: `uvicorn app:app --no-server-header`"
        }

    if ("fix" in msg or "prevent" in msg or "solve" in msg) and ("admin" in msg or "discovery" in msg):
        return {
            "reply": "🚪 **Preventive Measure:** Move your admin panel to a custom UUID path (e.g., `/admin-7b2-x91`) and use IP Whitelisting so only your office IP can access it."
        }

    # Legacy fallback responses (for backward compatibility)
    if "brute force" in msg or "rate limit" in msg:
        return {
            "reply": "🔍 **Brute Force Simulation:** This test checks if your API blocks repeated login attempts. Ask me to 'explain brute force' for details or 'fix brute force' for preventive measures."
        }

    if "https" in msg or "http" in msg or "protocol" in msg:
        return {
            "reply": "🔍 **Transport Security:** This test checks for HTTPS encryption. Ask me to 'explain HTTP security' for details or 'fix HTTP security' for preventive measures."
        }

    if "header" in msg or "server info" in msg or "talking" in msg:
        return {
            "reply": "🔍 **Information Leakage:** This test analyzes HTTP headers for exposed server information. Ask me to 'explain information leakage' for details or 'fix information leakage' for preventive measures."
        }

    if "admin" in msg or "discovery" in msg:
        return {
            "reply": "🔍 **Endpoint Discovery:** This test probes for exposed administrative paths. Ask me to 'explain endpoint discovery' for details or 'fix endpoint discovery' for preventive measures."
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