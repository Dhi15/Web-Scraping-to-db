from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3


try:
    response = requests.get("https://www.imdb.com/chart/top/")
    soup = BeautifulSoup(response.text,'html.parser')
    movies = soup.find('tbody',{"class": "lister-list"}).find_all('tr')
    movie_list = {'movie_rank':[],'movie_name':[],'movie_year':[],'movie_rate':[]}

    for movie in movies:
        movie_name = movie.find('td',class_="titleColumn").a.text
        rank = movie.find('td',class_="titleColumn").get_text(strip=True).split('.')[0]
        rate = movie.find('td',class_="ratingColumn").strong.text
        year = movie.find('td',class_="titleColumn").span.text.replace('(',"")
        year = year.replace(')',"")
        movie_list["movie_rank"].append(rank)
        movie_list["movie_name"].append(movie_name)
        movie_list["movie_year"].append(year)
        movie_list["movie_rate"].append(rate)

except Exception as e:
    print(e)

df=pd.DataFrame(data=movie_list)
print(df.head())

conn=sqlite3.connect("test.db")
cursor=conn.cursor()
qry="CREATE TABLE IF NOT EXISTS movies(movie_rank,movie_name,movie_year,movie_rate)"
cursor.execute(qry)
for i in range(len(df)):
    cursor.execute("insert into movies values (?,?,?,?)",df.iloc[i])

conn.commit()
conn.close()