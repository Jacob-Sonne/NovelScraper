#!/usr/bin/env python3
import sys
import os
from scraper_factory import get_scraper_for_url
from scraper_context import ScraperContext

def save_chapter(novel_title, chapter_title, chapter_text):
    # Sanitize folder and filename
    safe_title = "".join(c for c in chapter_title if c.isalnum() or c in " _-").strip()
    safe_folder = "".join(c for c in novel_title if c.isalnum() or c in " _-").strip()
    safe_folder = os.path.join("Novels", safe_folder)

    # Create folder if it doesn't exist
    if not os.path.exists(safe_folder):
        os.makedirs(safe_folder)
    
    filepath = os.path.join(safe_folder, f"{safe_title}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(chapter_text)

    print(f"Saved: {filepath}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <url>")
        sys.exit(1)

    url = sys.argv[1]

    strategy = get_scraper_for_url(url)
    context = ScraperContext(strategy)

    while url:
        data = context.scrape(url)

        novel_title = data.get("novel_title")
        chapter_title = data.get("chapter_title")
        chapter_text = data.get("chapter_text")
        next_chapter_link = data.get("next_chapter_link")

        save_chapter(novel_title, chapter_title, chapter_text)

        if next_chapter_link:
            url = next_chapter_link
        else:
            print("No more chapters to scrape")
            break


if __name__ == "__main__":
    main()