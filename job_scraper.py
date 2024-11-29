import requests
from bs4 import BeautifulSoup
import csv


# -----------------------  Job Roles & Descriptions ----------------------------------- #

# Function to fetch and parse the web page
def scrape_flexjobs(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data from {url}. Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = []

    # Locate job listing cards using unique identifiers or classes
    job_cards = soup.find_all('div', class_='sc-jv5lm6-0')
    for card in job_cards:
        try:
            title = card.find('a', class_='sc-jv5lm6-13').text.strip()  # Job title
            company = card.find('div', class_='sc-jv5lm6-2').text.strip()  # Company name
            location = card.find('span', class_='allowed-location').text.strip()  # Job location
            description = card.find('p', class_='sc-jv5lm6-4').text.strip() #Job description
            
            jobs.append({
                "Job Title": title,
                "Company": company,
                "Location": location,
                "Description" : description
            })
        except AttributeError:
            # Skip if any required field is not found
            continue

    return jobs

# Save jobs to a CSV file
def save_to_csv(jobs, filename="flexjobs_listings_1.csv"):
    if not jobs:
        print("No jobs found to save.")
        return
    
    keys = jobs[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(jobs)
    print(f"Saved {len(jobs)} jobs to {filename}")

if __name__ == "__main__":
    # URL for the search page on FlexJobs
    flexjobs_url = "https://www.flexjobs.com/remote-jobs/web-software-development-programming"
    
    print("Scraping FlexJobs for 'Software Engineer' positions...")
    job_listings = scrape_flexjobs(flexjobs_url)
    save_to_csv(job_listings)
