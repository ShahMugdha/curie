# content_sources/vsco.py
VSCO_PROFILES = [
    "https://vsco.co/vsco/profile",
    "https://vsco.co/analogfilm/profile"
]

def fetch_vsco_links():
    return [
        {"title": "VSCO Visuals", "url": url, "source": "VSCO", "type": "image"}
        for url in VSCO_PROFILES
    ]
