# Get top 50 movies by genre and store the data in CSV file.
# Attributes saved:
# 1) genre
# 2) number of movies
# 3) title
# 4) year
# 5) rating
import requests
from bs4 import BeautifulSoup

class IMDB_Scraper:
    def __init__(self):
        self.movies = []
        self.genres = ['action', 'action-comedy', 'adventure', 'animation', 'biography', 'comedy', 'comedy-romance', 'crime',
                        'documentary', 'drama', 'family', 'fantasy', 'film-noir', 'history', 'horror', 'music', 'musical',
                        'mystery', 'romance', 'sci-fi', 'short-film', 'sport', 'superhero', 'thriller', 'war', 'western']

    def __get_num_of_movies(self, line):
        num = int((line.split(' ')[2]).replace(',', ''))
        return num

    def __scrape_movies_by_genre(self, genre):
        url = 'https://www.imdb.com/search/title/?title_type=feature&genres=' + genre + '&explore=genres'
        response = requests.get(url)
        html = BeautifulSoup(response.text, 'html.parser')

        try:
            num_of_movies = self.__get_num_of_movies(str(html.select('.desc > span')[0]))
            print(num_of_movies)
        except:
            return

        response.close()

    def scrape_movies(self):
        for genre in self.genres:
            self.__scrape_movies_by_genre(genre)


if __name__ == '__main__':
    print()
    scraper = IMDB_Scraper()
    scraper.scrape_movies()