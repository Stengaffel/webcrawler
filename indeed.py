import requests
from bs4 import BeautifulSoup

from help_functions import relevant_title, clean_string


def indeed_parse(search_terms, bad_words):

    # Set to keep track of duplicates                                           
    title_set = set()

    # Set for saving the job-entries                                            
    job_set = set()

    # Number of bad titles                                                      
    bad_titles = 0

    for query in search_terms:

        indeed_url = f'https://se.indeed.com/jobs?q={query}&start=0'

        while True:
            html_text = requests.get(indeed_url).text
            soup = BeautifulSoup(html_text, 'html.parser')

            # Find all job-entries                                              
            job_entries = soup.find_all('div', class_ = 'jobsearch-SerpJobCard unifiedRow row result')
            for div in job_entries:

                # Handle title                                                  
                title = div.h2.a.text.strip()

                # Check if the title contains bad words                         
                if not relevant_title(title, bad_words):
                    bad_titles += 1
                    continue
                # Check if title has been seen before
                if title in title_set:
                    continue
                else:
                    # Clean the string from dangerous characters for the sql
                    title = clean_string(title)
                    title_set.add(title)

                print(title)

                # Print the company name
                company = div.find(class_ = 'company')
                if company != []:
                    if company.text != None:
                        company = company.text.strip()
                    elif company.a.text != None:
                        company = company.a.text.strip()
                    else:
                        company = ''
                    print(company)

                # Print the location
                location = div.find(class_ = 'location accessible-contrast-color-location')
                if location.text != None:
                    location = location.text.strip()
                else:
                    location = ''
                print(location)

                # Print the link
                link = div.h2.a['href']
                link = f'https://se.indeed.com{link.strip()}'
                print(link)

                job_set.add((title, company, location, link))

                print()

            # Go to next page if it exists
            next_button = soup.find(attrs={'aria-label' : 'Nästa'})
            if next_button:
                indeed_url = f"https://se.indeed.com{next_button['href']}"
            else:
                break

    print(f'{len(title_set)} relevant articles found')
    print(f'{bad_titles} irrelevant articles found')

    return job_set
