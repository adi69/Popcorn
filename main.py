import requests
import sys
import os
import re
import csv
from urlparse import urljoin
from bs4 import BeautifulSoup
import urllib
from pprint import pprint


class Movies(object):
    
    def __init__(self, args):
        self.movies = []
        if len(args) == 0:
            print 'No Argument given'
            #TODO: raise exception or something
            return 
        
        if args[0] == '-d':
            args = self.get_movies_from_directories(args[1:])
        
        self.search_movie_names(args)
        self.to_csv()
    
    def get_movies_from_directories(self, dirs):
        #TODO: dirs is a list of all directories
        #handle errors if directories doesn't exist
        #look only for video formats maybe - mp4, avi, etc, etc
        result = []
        for directory in dirs:
            try:
                os.chdir(os.path.expanduser(directory))
            except Exception as e:
                print Exception
                continue

            files = os.listdir('.')

            for file_name in files:
                if os.path.isfile(file_name):
                    file_name = re.sub('[.][^.]*$','*', file_name)
                result.append(self.__purify_name(file_name))
                    
        return result

    def __purify_name(self, name):
        year_match = re.search('\W([0-9]){4}\W', name)
        year = name[year_match.start():year_match.end()] if year_match else ''
        name = re.sub('\((.*)\)|\[(.*)\]|\{(.*)\}','', name)
        name = re.sub('\W',' ', name)
        return name + year


    def search_movie_names(self, args):
        for item in args:
            #TODO: purify_name(item)
            search_term = urllib.quote_plus(item)
            url = 'http://www.imdb.com/find?q=' + search_term + '&s=all'
            bs = BeautifulSoup(requests.get(url).content, "html.parser")

            try:
                url_new = urljoin(url,bs.find(
                    'td', attrs={'class':'result_text'}).find('a').get('href'))
                movie_dict = self.extract_movie_info(url_new)
            except:
                print ('No Result Found. searched: ', search_term, item)
                movie_dict = self.extract_movie_info()

            movie_dict['original_name'] = item
            movie_dict['search_term'] = search_term
            self.movies.append(movie_dict)
            pprint(movie_dict)

        return True


    def extract_movie_info(self, url=None):
        if not url:
            return { 'name': '', 'rating': '', 'summary': '', 'genre': '', }

        response = requests.get(url).content
        bs = BeautifulSoup(response, "html.parser")
        name = bs.find('h1', attrs={'itemprop':'name'}).text.encode('utf-8')

        try:
            rating = bs.find('span', attrs={'itemprop':'ratingValue'}).text
        except:
            rating = '-'

        try:
            summary = bs.find('div', attrs={'class':'summary_text'}).text.strip().encode('utf-8')
        except:
            summary = '-'

        try:
            genre = bs.find('span', attrs={'itemprop':'genre'}).text.encode('utf-8')
        except:
            genre = '-'

        return {
                'name': name,
                'rating': rating,
                'summary': summary,
                'genre': genre,
        }

    def to_csv(self):
        f = csv.writer(open('movies_list.csv', 'wb+'))
        f.writerow(['original_name','name', 'rating', 'genre', 'summary'])
        for item in self.movies:
            f.writerow([item['original_name'], item['name'], item['rating'],
                    item['genre'], item['summary']])


def main():
    obj = Movies(sys.argv[1:])


if __name__ == '__main__':
    main()
