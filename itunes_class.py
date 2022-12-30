#Dependencies 
import requests
from datetime import date
import pandas as pd

#Class
class iTunes():
    '''
    A class for analyzing iTunes data.
    
    Attributes
    ----------
    artist : str
        A string with the artist's name.
    limit : int
        A rate limit for the number of tracks queried.
    URL : str
        The base URL for the http request.
    date : pd.datetime object
        Records the day of download.
    headers : dictionary
        HTTP headers to send along request.
    
    Methods
    -------
    parser_wrangler(self):
        Downloads the iTunes data and creates tuples for latter use.
    
    playtime(self, dtrackTimeMillis):
        Calculates each tracks runtime as a tuple of (minutes, seconds).
    '''

    def __init__(self):
        self.artist = 'Pixies'
        self.limit = 200
        self.URL = 'https://itunes.apple.com/search?term='+self.artist+\
        '&attribute=artistTerm&entity=song&limit='+str(self.limit)
        self.date = str(date.today())
        self.headers = {
            'authority': 'https://www.apple.com/itunes/',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'accept': 
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'sec-fetch-site': 'none',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,es-MX;q=0.8,es;q=0.7'
                        }
        # create list of attribute variables of interest
        self.attrs = ['collectionId', 'trackPrice', 'trackTimeMillis', 'primaryGenreName', 
                      'contentAdvisoryRating', 'isStreamable', 'artistId', 'trackName'] 

    def parser_wrangler(self):
        '''
        parser_wrangler():
        This function downloads iTunes data and creates tuples for latter use. 
        Arguments:
        ----------
        Class's instance attributes (selfs).
        Returns:
        ----------
        Tuple of four (df, attrs_df, pct_miss, trackTimeMillis).
        '''
        df = pd.DataFrame.from_dict(requests.get(self.URL, headers=self.headers).json()['results'])
        df['crawl_time'] = self.date #variable to identify the date of download
        attrs_df = df[(self.attrs)].reset_index(drop=True) # keep only those variables of interest
        pct_miss = (df.isnull().sum() * 100 / len(df)).round(1).sort_values(ascending = False) #create missing values df
        trackTimeMillis = attrs_df.trackTimeMillis
        return(df, attrs_df, pct_miss, trackTimeMillis)
    
    def playtime(self, trackTimeMillis):
        '''
        playtime():
        This function calculates each tracks runtime as a tuple of (minutes, seconds). 
        Arguments:
        ----------
        Class' instance attributes (selfs).
        Returns:
        -----------
        Tuple of four (df, attrs_df, pct_miss, trackTimeMillis).
        '''
        track_minutes = trackTimeMillis/60000 #create minutes
        track_seconds = round((track_minutes % 1)*0.6*100,0) #create seconds from minute's decimals transformed in seconds
        track_minutes = round(track_minutes, 0) # trim minutes to integer value
        return(track_minutes, track_seconds)

#Use this class  
data = iTunes() # Call upon the class
df, attrs_df, pct_miss, trackTimeMillis = data.parser_wrangler() # Unpack tuple generated using 'parser_wrangler'

