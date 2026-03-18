#--------------------------------------------------------------------------------
# __      __      ___.     _________                        .__                
#/  \    /  \ ____\_ |__   \_   ___ \_________  _  _______  |  |   ___________ 
#\   \/\/   // __ \| __ \  /    \  \/\_  __ \ \/ \/ /\__  \ |  | _/ __ \_  __ \
# \        /\  ___/| \_\ \ \     \____|  | \/\     /  / __ \|  |_\  ___/|  | \/ 
#  \__/\  /  \___  >___  /  \______  /|__|    \/\_/  (____  /____/\___  >__|   
#       \/       \/    \/          \/                     \/          \/       
#
#
#  Q: What does it need to do?
#  A: It needs to go through every link it can find
#     Links are inside <a href='link'></a>
#     Flag is inside <h1>flag{}</h1>
#
#  
#  websites dict:
#
#  +---key-----value---+
#  | 'url0' |    0     |
#  | 'url1' |    1     |
#  +-------------------+
#
#  value: 0 = visited; 1 = not visited
#  This way the logic permits increasing 1 to visit multiple times.
# 
#---------------------------------------------------------------------------------


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "[whateverurl]"
websites = {} # Dictionary so that every url is unique
websites[url] = 1


def find_flag(soup):
    for flag in soup.find_all('h1'):
       if 'flag{' in str(flag):
           print("!!! Flag Found: " + str(flag))
           return True
    return False


def save_links(soup, base_url, webs_to_add):
    for link in soup.find_all('a'):
        href = link.get('href')
        newurl = urljoin(base_url, href)
        if newurl not in websites and newurl not in webs_to_add:
            webs_to_add[newurl] = 1 
        #print("--> newurl: " + newurl)
        #print("--> websites: ")
        #print(webs_to_add)
        

all_visited = 0
#proceed = 'y'
while not all_visited: # while not all pages are visited continue to visit them
    webs_to_add = {}
    all_visited= 1 # 1=no page left to visit; 0=still pages left to visit
    for page in websites:
        if websites.get(page): #if not visited then visit (not visited = 1)
            all_visited = 0
            try:
                r = requests.get(page, timeout=5)
                r.raise_for_status()
            except requests.RequestException as e:
                #------For better automation either skin the url or try again automatically, no input
                input(f"Failed: {page} -> {e}") 
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            if find_flag(soup):
                exit(0)
            save_links(soup, page, webs_to_add)
            
            #--- now visited 
            websites[page] = 0
            #---
            
    # Update websites links
    websites.update(webs_to_add)
    print(len(websites))
    #proceed = input("Continue?: ")

print(websites)
