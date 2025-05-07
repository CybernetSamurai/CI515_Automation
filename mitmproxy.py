from mitmproxy import http
import re

# Define a general list of sensitive keywords to search for
SENSITIVE_KEYWORDS = [
    "email", "username", "address", "birthday", "order",
    "loyalty", "ip", "transaction", "customerid", "device",
    "os", "usage", "sessionid", "locationid", "third-party"
]

# Case-insensitive keyword maatching in text (body or headers)
def detect_sensitive_data(text):
    found = []
    for keyword in SENSITIVE_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", text, re.IGNORECASE):
            found.append(keyword)
    return found

def process_flow(flow: http.HTTPFlow, is_response: bool):
    # Get content and headers
    content = flow.response.text if is_response else flow.request.text
    headers = flow.response.headers if is_response else flow.request.headers

    # Combine headers and body content into a single string for scanning
    combined_text = content + "\n" + "\n".join(f"{k}: {v}" for k, v in headers.items())

    found_files = detect_sensitive_data(combined_text)
    if found_fields:
        print("\n[!] Potential Sensitive Data Leakage Detected")
        print(f"{'Response' if is_response else 'Request'} URL: {flow.request.pretty_url}")
        print(f"Fields Detected: {', '.join(set(found_fields))}")
        print("-" * 50)

def request(flow: http.HTTPFlow):
    process_flow(flow, is_response=False)

def response(flow: http.HTTPFlow):
    process_flow(flow, is_response=True)
