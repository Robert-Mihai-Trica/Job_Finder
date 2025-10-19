import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_jobs(keyword="Technical Support", location="Romania", pages=1):
    jobs = []

    for page in range(pages):
        start = page * 25
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keyword}&location={location}&f_AL=true&f_WT=2&start={start}"
        
        print(f"🔍 Caut pe pagina {page+1}...")
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        
        if response.status_code != 200:
            print("❌ Nu am putut accesa pagina")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("li")

        for job in job_cards:
            title_elem = job.find("h3")
            company_elem = job.find("h4")
            link_elem = job.find("a")

            if title_elem and company_elem and link_elem:
                title = title_elem.get_text(strip=True)
                company = company_elem.get_text(strip=True)
                link = link_elem["href"].split("?")[0]

                jobs.append([title, company, link])

        time.sleep(2)  

    return jobs


if __name__ == "__main__":
    job_results = scrape_jobs(keyword="Technical Support", location="Romania", pages=2)

    df = pd.DataFrame(job_results, columns=["Title", "Company", "Link"])
    df.to_csv("jobs_safe.csv", index=False, encoding="utf-8")

    print(f"✅ Am găsit {len(job_results)} joburi. Export în jobs_safe.csv")
