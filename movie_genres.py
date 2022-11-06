# Get up to top 50 popular movies by genre and store the data in CSV file.
# Attributes saved:
# 1) genre
# 2) number of movies
# 3) title
# 4) year
# 5) length
# 6) rating
import requests
from bs4 import BeautifulSoup

class IMDB_Scraper:
    def __init__(self):
        self.num_of_movies = []
        self.genres = ['action', 'action-comedy', 'adventure', 'animation', 'biography', 'comedy', 'comedy-romance', 'crime',
                        'documentary', 'drama', 'family', 'fantasy', 'film-noir', 'history', 'horror', 'music', 'musical',
                        'mystery', 'romance', 'sci-fi', 'short-film', 'sport', 'superhero', 'thriller', 'war', 'western']

    def __get_num_of_movies(self, line):
        return (line.split(' ')[2]).replace(',', '')

    def __scrape_movies_by_genre(self, genre, f):
        url = 'https://www.imdb.com/search/title/?title_type=feature&genres=' + genre + '&explore=genres'
        response = requests.get(url)
        html = BeautifulSoup(response.text, 'html.parser')

        try:
            try:
                num_of_movies = self.__get_num_of_movies(str(html.select('.desc > span')[0]))
                self.num_of_movies.append(num_of_movies)
            except:
                self.num_of_movies.append('0')
                return # no movies found

            movie_containers = html.find_all('div', class_ = 'lister-item mode-advanced')

            for container in movie_containers:
                try:
                    title = container.h3.a.text
                    year = str(container.h3.find('span', class_ = 'lister-item-year text-muted unbold').text)
                    yearFound = False

                    for y in range(1800, 2024):
                        if str(y) in year:
                            year = str(y)
                            yearFound = True
                            break

                    if not yearFound:
                        raise Exception()

                    rating = container.find('div', class_ = 'inline-block ratings-imdb-rating')
                    rating = rating.find('strong').text
                    length = container.p.find('span', class_ = 'runtime').text.split(' ')[0]
                    f.write(genre + ',' + num_of_movies + ',' + title + ',' + year + ',' + rating + ',' + length + '\n')
                except:
                    pass # the movie doesn't have all needed attributes
        except:
            pass

        response.close()

    def scrape_movies(self):
        try:
            headers = 'Genre,Total movies with this genre,Title,Year,Length,Rating\n'
            movies_file = open('Movies.csv', 'w')
            movies_file.write(headers)

            for genre in self.genres:
                self.__scrape_movies_by_genre(genre, movies_file)
            
            try:
                genres_file = open('Genres.csv', 'w')
                headers = 'Genre,Total movies for that genre\n'
                genres_file.write(headers)

                if (len(self.num_of_movies) == len(self.genres)):
                    for i in range(0, len(self.genres)):
                        genres_file.write(self.genres[i] + ',' + self.num_of_movies[i] + '\n')
                else:
                    print("Error! Lengths don't match")
            except Exception as e:
                print(e)
            finally:
                genres_file.close()
        except Exception as e:
            print(e)
        finally:
            movies_file.close()


if __name__ == '__main__':
    scraper = IMDB_Scraper()
    scraper.scrape_movies()