import requests
import re
from bs4 import BeautifulSoup

# Check if the title is relevant. True if relevant, false if not
def relevant_title(title, bad_words):
    edited = str(title).lower()

    for word in bad_words:
        match = re.match(word, edited)
        if match:
            #print(title)
            #print(match)
            return False
    
    return True

def main():
    # Strings that will be used in the queries
    search_terms = ['ex-jobb', 'thesis']

    # Words that should not be included in the title
    bad_words = ['phd', 'postdoc', 'professor', 'trainee', 'doctoral']

    # Set to keep track of duplicates
    title_set = set()

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
                    break

                # Check if title has been seen before
                if title in title_set:
                    break
                else:
                    title_set.add(title)

                print(title)

                # Print the company name
                company = div.find(class_ = 'company')
                if company != []:
                    if company.text != None:
                        print(company.text.strip())
                    elif company.a.text != None:
                        print(company.a.text.strip())

                # Print the location
                location = div.find(class_ = 'location accessible-contrast-color-location')
                if location.text != None:
                    print(location.text.strip())

                # Print the link
                link = div.h2.a['href']
                print(f'https://se.indeed.com{link.strip()}')

                print()
            
            # Go to next page if it exists
            next_button = soup.find(attrs={'aria-label' : 'Nästa'})
            if next_button:
                indeed_url = f"https://se.indeed.com{next_button['href']}" 
            else:
                break
            
    print(f'{len(title_set)} relevant articles found')
    print(f'{bad_titles} irrelevant articles found')


if __name__ == '__main__':
    main()