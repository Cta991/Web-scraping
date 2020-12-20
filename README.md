# Web-scraping
This repository records my process of learning web scraping by doing projects.

Projects:
- Scrap_by_list and Scrap_by_category: basically 2 alternatives in scraping http://books.toscrape.com/. Scrap_by_list is more complicated since it scrape all the books and include the category of each book, while Scrap_by_list only return all the books. The data is saved inside a sqlite3 databse.
- Yahoo_finance and Yahoo_finance_2: scrape https://finance.yahoo.com/. However, user need to input the link of the stock/bond he/she is looking for manually to run these code. Yahoo_finance will then return the list of information available on the required stock/bond, which the user can access by inputting the listed information name. Yahoo_finance_2 goes 1 step furthur and save the list of information inside a sqlite3 database.
- tiki_4: scrape https://tiki.vn/nha-sach-tiki/c8322. It can be altered to scrape any other product, not just book. This code also save all the book's information available on the website into a sqlite3 databse.
- amazon.py: scrape https://www.amazon.com/(just the gaming console category). Also save all the book's information available on the website into a sqlite3 databse.
