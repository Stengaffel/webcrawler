import sqlite3

# imports from local files
from indeed import indeed_parse
from linkedin import linkedin_parse

# Add ads to database
def add_to_database(job_set, table):
    conn = sqlite3.connect('ads.sqlite')

    query = f'INSERT OR IGNORE INTO {table}(title, company, location, link)\nVALUES '

    # Make an exception for the first iteration
    first_it = True
    for job in job_set:
        if first_it: first_it = False
        else:
            query = query + ',\n'
        query = query + f"('{job[0]}', '{job[1]}', '{job[2]}', '{job[3]}')"

#    query = query + f"ON DUPLICATE KEY UPDATE 'date' = 'date';"
    query = query + ";"

    print(query)

    # Execute the query
    c = conn.cursor()
    c.execute(query)
    conn.commit()


def main():

    # Strings that will be used in the queries                                  
    search_terms = ['ex-jobb', 'thesis']

    # Words that should not be included in the title                            
    bad_words = ['phd', 'postdoc', 'professor', 'trainee', 'doctoral']

    indeed_ads = indeed_parse(search_terms, bad_words)
    add_to_database(indeed_ads,'indeed_ads')

    linkedin_ads = linkedin_parse(search_terms, bad_words)
    add_to_database(linkedin_ads, 'linkedin_ads')


if __name__ == '__main__':
    main()
