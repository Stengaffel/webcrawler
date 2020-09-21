import requests
from bs4 import BeautifulSoup

from help_functions import relevant_title, clean_string


def linkedin_parse(search_terms, bad_words):

    # Set to keep track of duplicates
    title_set = set()

    # Set for saving the job-entries
    job_set = set()

    # Number of bad titles
    bad_titles = 0

    for query in search_terms:
        # Urls that rank by date and relevancy
        linkedin_urls = [f'https://se.linkedin.com/jobs/search?keywords={query}&location=Sverige&geoId=105117694&trk=public_jobs_jobs-search-bar_search-submit&sortBy=DD&redirect=false&position=1&pageNum=0', f'https://se.linkedin.com/jobs/search?keywords={query}&location=Sverige&geoId=105117694&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0']

        for url in linkedin_urls:
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'html.parser')

            # Find all job-entries
            job_entries = soup.find_all('li', class_="result-card job-result-card result-card--with-hover-state")

            for li in job_entries:

                # Handle title
                title = li.find(class_='result-card__title job-result-card__title')
                if title != []:
                    title = title.text

                    # Check if the title contains bad words
                    if not relevant_title(title, bad_words):
                        bad_titles += 1
                        continue
                    # Check if the title has been seen before
                    if title in title_set:
                        continue
                    else:
                        # Clean the string from dangerous characters for the sql
                        title = clean_string(title)
                        title_set.add(title)
                print(title)

                # Print the company name
                company = li.find(class_='result-card__subtitle job-result-card__subtitle')
                if company != []:
                    company = company.text.strip()
                print(company)

                # Print the location
                location = li.find(class_='job-result-card__location')
                if location != []:
                    location = location.text.strip()
                print(location)

                # Print the link
                link = li.find(class_='result-card__full-card-link')
                if link != []:
                    link = link['href']
                print(link)

                job_set.add((title, company, location, link))

                print()

    print(f'{len(title_set)} relevant articles found')
    print(f'{bad_titles} irrelevant articles found')

    return job_set
