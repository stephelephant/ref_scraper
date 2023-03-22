from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np


def box_score(url):
  # collect HTML data - boxscore URL
  html = urlopen(url)
  # geting whole soup and then break into team soups
  soup = BeautifulSoup(html, features="html.parser")

  # finding these urls to identify teams playing somewhere on the boxscore page
  teamhref = soup.findAll(href=re.compile('teams/.../...._games.html'), limit=2)

  # extracting 3 letter initials of team - ex. GSW or LAL
  team_strings = []
  for href in teamhref:
    hrefstring = str(href)
    team_string = hrefstring[16:19]
    team_strings.append(team_string)
  
  # should probably change to home and away - two is home
  one = team_strings[0]
  two = team_strings[1]

  team1 = soup.findAll(id=f'box-{one}-game-basic')[0]
  team2 = soup.findAll(id=f'box-{two}-game-basic')[0]

  def team_box(soupvar):
    
    # scraping box score stats for columns
    titles = soupvar.findAll('tr', limit=3)[1].findAll('th')
    df_columns = [title.getText() for title in titles[1:len(titles)]]
    df_columns.insert(0,'Player')


    # helper function for finding the correct <tr> tags for players
    def filterstat(string):
      string = str(string)
      stats_to_find = ['mp', 'scope="row"','fga','fg']
      bool_list = [stat in string for stat in stats_to_find]
      return all(bool_list)

    # scrape all rows and then using function to find players
    players_rows = soupvar.findAll("tr", limit=10000)
    players_rows = [row for row in players_rows if filterstat(row)]


    # getting unique player names 
    player_set = {player.th.getText() for player in players_rows}
    player_set.remove('Team Totals')

    # loop to get the first row of stats for each player
    player_stats = []

    for player in player_set:
      for row in players_rows:
        if player in row.th.getText():
          td = row.findAll('td')
          stats = []
          stats.append(player)
          for t in td:
            stats.append(str(t.getText()))
          player_stats.append(stats)
          break

    # create dataframe and return team box score
    df = pd.DataFrame(player_stats)
    df.columns = df_columns
    return df
  
  # creating a box for each team and make a total box score
  a = team_box(team1)
  a['team'] = one
  b = team_box(team2)
  b['team'] = two
  
  df = pd.concat([a,b])

  def time_converter(x):
    minute, seconds = x.split(":")
    perc = int(seconds)/60
    minutes = round((float(minute) + perc), 2)
    return minutes
  
  df['MP'] = df.MP.apply(time_converter)
  


  def plus_minus(x):
    if x == '':
        return 0
    elif int(x) == 0:
      return 0
    elif str(x)[0] == "+":
      return int(x.replace("+",""))
    else:
      return int(x)
  
  df[r'+/-'] =  df[r'+/-'].apply(plus_minus)


  df = df.replace("",np.NaN)

  for col in df.columns[2:-2]:
    if "%" in str(col):
      df[col] = df[col].astype('float64')
    else:
      df[col] = df[col].astype('int64')
      
  ymd = str(url)[-17:-9]

  df.name = f"{ymd}_{one}vs{two}_BoxScore.csv"

  return df




def get_game_links(start_year,end_year):
    
    
    baseurl = r'https://www.basketball-reference.com/leagues/NBA_'
    

    months = ['october','november', 'december', 'january', 'february', 'march', 
              'april', 'may', 'june', 'july', 'august', 'september']

    years = range(start_year,end_year+1)

    schedule_urls = []
    for year in years:
        for month in months:
            schedule_urls.append(baseurl + str(year) + '_games-' + str(month) + ".html")
        
    list_of_games = []
    
    for url in schedule_urls:
        try:
            html = urlopen(url)
            soup = BeautifulSoup(html, features='html.parser')
            th = soup.findAll(name='th', attrs={'data-stat':'date_game'}, scope='row')
            games = [str(h)[22:34] for h in th]
            for game in games:
                list_of_games.append(game)
        except:
            print(f'{url} failed')

    
    

    baseurl = 'https://www.basketball-reference.com/boxscores/'
    box_score_urls = [baseurl + str(game) + '.html' for game in list_of_games]
    
    
    return box_score_urls
