#%%
# creating the client object and fetching sample_commits table from dataset
from google.cloud import bigquery
client = bigquery.Client()
dataset_ref = client.dataset("github_repos", project="bigquery-public-data")
dataset = client.get_dataset(dataset_ref)
table_ref = dataset_ref.table("sample_commits")
sample_commits_table = client.get_table(table_ref)

#%%
# creating a query to find out committers with most commits in 2016, returning committer's names and number of commits in descending order of commits
max_commits_query = """
                    SELECT committer.name AS committer_name,
                            COUNT(1) AS num_commits
                    FROM `bigquery-public-data.github_repos.sample_commits`
                    WHERE EXTRACT(YEAR FROM committer.date) = 2016
                    GROUP BY committer_name
                    ORDER BY num_commits DESC
                    
                    """

#%%
# fetching new languages table from dataset
table_ref = dataset_ref.table("languages")
languages_table = client.get_table(table_ref)

#%%
# creating query to find out which languages appear in the most repositories, returning language names and number of repositories featuring the language in descending order of # of repositories
pop_lang_query = """SELECT language.name AS language_name,
                    COUNT(*) AS num_repos
                    FROM `bigquery-public-data.github_repos.languages`,
                        UNNEST(language) AS language
                    GROUP BY language_name
                    ORDER BY num_repos DESC
                    
                 """

#%%
# creating query to find out which language takes up the most data in the repository with the largest number of languages, returning language names and bytes in descending order of bytes
all_langs_query = """SELECT language.name , language.bytes 
                        FROM `bigquery-public-data.github_repos.languages`,
                             UNNEST(language) AS language
                        WHERE repo_name = 'polyrabbit/polyglot'
                        ORDER BY language.bytes DESC
                  """