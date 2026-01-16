import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import os

BASE_URL = "https://fastapi.tiangolo.com"
PAGES = [
    "/",
    "/tutorial/",
    "/advanced/",
]

os.makedirs("docs", exist_ok=True)

for path in PAGES:
    url = BASE_URL + path
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    main = soup.find("main")
    if not main:
        continue

    text = md(str(main))

    filename = path.strip("/").replace("/", "_") or "home"
    with open(f"docs/{filename}.md", "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Saved {filename}")
