import requests
import sys
from urlparse import urljoin
from bs4 import BeautifulSoup
import urllib
from pprint import pprint


class Movie(object):
    
    def __init__(*args):
        self.movies = []
        if len(args) == 0:
            print 'No Argument given'
            #TODO: raise exception or something
            return False
        
        if args[0] == '-d':
            return get_movies_from_directories(args[1:])
        
        return search_movie_names(args)

    
    def get_movies_from_directories(self, dirs):
        #TODO: dirs is a list of all directories
        #handle errors if directories doesn't exist
        #look only for video formats maybe - mp4, avi, etc, etc

    def search_movie_names(self, args):
        for item in args:
            #TODO: purify_name(item)
            search_term = urllib.quote_plus(item)
            url = 'http://www.imdb.com/find?q=' + search_term + '&s=all'
            bs = BeautifulSoup(requests.get(url).content, 'lxml')

            try:
                url_new = urljoin(url,bs.find(
                    'td', attrs={'class':'result_text'}).find('a').get('href'))
                movie_dict = extract_movie_info(url_new)
            except:
                print ('No Result Found. searched: ', search_term, item)
                movie_dict = extract_movie_info()

            movie_dict['original_name'] = item
            movie_dict['search_term'] = search_term
            self.movies.append(movie_dict)
            pprint(movie_dict)

        return True


    def extract_movie_info(self, url=None):
        if not url:
            return { 'name': '', 'rating': '', 'summary': '', 'genre': '', }

        response = requests.get(url).content
        bs = BeautifulSoup(response, 'lxml')
        name = bs.find('h1', attrs={'itemprop':'name'}).text

        try:
            rating = bs.find('span', attrs={'itemprop':'ratingValue'}).text
        except:
            rating = '-'

        try:
            summary = bs.find('div', attrs={'class':'summary_text'}).text.strip()
        except:
            summary = '-'

        try:
            genre = bs.find('span', attrs={'itemprop':'genre'}).text
        except:
            genre = '-'

        return {
                'name': name,
                'rating': rating,
                'summary': summary,
                'genre': genre,
        }


def main():
    obj = Movies(sys.argv[1:])


if __name__ == '__main__':
    main()
