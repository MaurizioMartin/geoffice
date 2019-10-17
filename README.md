# geoffice

Geoffice is a web application made in Django with the purpose of find the best location for placing your office. 

It was made for the final project of the Ironhack's Data Analytics bootcamp.

# Process

It all started with a Crunchbase dataset with almost 19K companies. I created a model grouping all the companies by category_codes and creating 4 clusters. When a new company is introduced, the system can classify it and return companies with a similar category.

The process of search is simple for user. They just need to fill a small survey with three questions: "","" and "". Once submitted, the system will make NLP and will return keywords.

## Role

A model was created by analysing the descriptions of all the companies and making IF-IDF. When, for example, an answer like "" is submitted, the system will return "" and "". Then, those keywords will be compared between all the category codes with the Jaro distance. This will return a percentage where the max value will be considered as the ROLE.

## Location

With a python library called "". The location will be extracted from the text.

## Near

To extract the preferences the company wants to have near, I use NLTK and extract the nouns of the text.

# Search

Once we have the keywords, the search begins:

- It starts with the Latitude and Longitude of the center of the selected city.
- It calculate the position of the near companies with similar category-codes and recalculate to be in the middle of them.
- Then, the system searchs for the position of the preferences and recalculate as much as preferences the company have.
- Finally it return a Latitude and Longitude in the middle of the companies and preferences in the selected city.

# API's

In order to find the coordenates, I use the Google API's and Zomato API. 