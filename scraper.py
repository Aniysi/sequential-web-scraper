# scraping_legale_con_playwright.py - Scraper responsabile con Playwright

from playwright.sync_api import sync_playwright
import time
import random
import re
from pathlib import Path
from urllib.robotparser import RobotFileParser
import logging

# Configura il logging per vedere cosa succede
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    def __init__(self, start_url: str, end_url: str):
        self.start_url = start_url.strip()
        self.end_url = end_url.strip()
        self.text_selector = "#dle-content > article > div.block.story.shortstory"
        self.forward_selector = "#next"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        }

    def check_robots_txt(self) -> bool:
        """Check if scraping is permitted by robots.txt"""
        try:
            rp = RobotFileParser()
            rp.set_url(f"{self.start_url.rstrip('/')}/robots.txt")
            rp.read()

            # Verifica se il bot (user-agent) può accedere
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            can_fetch = rp.can_fetch(user_agent, self.start_url)

            if not can_fetch:
                logger.warning("Scraping prohibited by robots.txt")
            return True

        except Exception as e:
            logger.warning(f"Failed to read robots.txt: {e}")
            # Se non si può leggere, assumiamo che sia "sicuro"
            return True

    def scrape_selected(self, url: str) -> list[str]:
        """Extract data with Playwright (simulate real browser)"""
        
        if not self.check_robots_txt():
            logger.error("Scraping prohibited by robots.txt")
            return []

        with sync_playwright() as p:
            # Avvia browser in modalità headless = False per debug
            browser = p.chromium.launch(headless=False, slow_mo=500)  # lento per vedere cosa succede

            page = browser.new_page()

            try:
                logger.info(f"🔄 Load page: {url}")

                # Imposta User-Agent reale (simula un utente normale)
                page.set_extra_http_headers({
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                })

                # Vai alla pagina
                response = page.goto(url, wait_until="networkidle", timeout=20_000)

                if response.status != 200:
                    logger.error(f"HTTP error: {response.status} - {response.reason}")
                    return []

                # Attendi che il contenuto JS si carichi
                page.wait_for_load_state("networkidle")

                # Crea ritardo casuale per simulare interazione umana
                time.sleep(random.uniform(3, 6))

                results = []

                # Estrai elementi con il selettore CSS fornito
                elements = page.query_selector_all(self.text_selector)

                for el in elements:
                    text = el.inner_text().strip()
                    if text:
                        results.append(text)
                        logger.info(f"✅ Found: {text}")

                # Estrai elementi con il selettore CSS fornito
                elements = page.query_selector_all(self.forward_selector)

                for el in elements:
                    href = el.get_attribute("href")
                    if href:
                        results.append(href)
                        logger.info(f"✅ Found: {href}")


                # Se non trova nulla, mostra un messaggio utile
                if not results:
                    logger.warning("⚠️ No element found with given selector.")

                return results

            except Exception as e:
                logger.error(f"❌ Error during scraping: {e}")
                return []

            finally:
                browser.close()

        return []
    

    def scrape(self):

        # Create temp folder
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        
        url = self.start_url

        # End condition
        end = False

        while True:
            results = self.scrape_selected(url)
            
            if not results or len(results) < 1:
                logger.error("❌ No results to save, attempting again.")
                continue
            
            # Extract first line for filename
            content = results[0]
            first_line = content.split('\n')[0].strip()
            
            # Sanitize filename
            safe_filename = re.sub(r'[<>:"/\\|?*]', '', first_line)
            safe_filename = safe_filename[:100].strip().replace(' ', '_')
            
            if not safe_filename:
                safe_filename = "scraped_content"
            
            # Save to .txt file
            filepath = temp_dir / f"{safe_filename}.txt"
            filepath.write_text(content, encoding='utf-8')
            
            logger.info(f"💾 Saved to: {filepath}")
            print(f"Content saved to: {filepath}")

            # CHeck end condition
            if end:
                break
            
            # Update link
            url = results[1]
            if url == self.end_url:
                end = True

        return temp_dir


        



