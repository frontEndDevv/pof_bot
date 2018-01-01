import requests
import urllib2
from bs4 import BeautifulSoup
import time

people = []
next_page = []
uname = raw_input("Username: ")
pw = raw_input("Password: ")

url = 'https://www.pof.com/processLogin.aspx'
values = {'username': uname,
          'password': pw,
	  'login': '',
	  'tfset': '240',
	  'sid': 'rrfrxhoodhkpgdk50ulyfkaq',
		}

#Header data
header_data = \
	{
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
		'Upgrade-Insecure-Requests': '1',
		'Referer': 'http://www.pof.com/inbox.aspx',
		'Origin': 'http://www.pof.com',
		'Host': 'www.pof.com',
		'Cookie': 'ft=Thursday, April 28, 2016 6:39:19 PM; installid=ae58ae64-b5af-4ec1-a561-3d227d1916c8; isfirstrun=everyoneonline.aspx; my_ipcountry=1; username=WayneKenneyy; user_idb=129008014; usernameb=WayneKenneyy; tmp_track=129008014; pof_cookie=id_129008014__79_5545__89_4259462418; ASP.NET_SessionId=rrfrxhoodhkpgdk50ulyfkaq; POFIMSession=635974982832470010; isfirstrun_mmv=meetme.aspx; t_user_id=129008014; __utma=181982502.1458391091.1461893952.1461926258.1461953365.4; __utmb=181982502.5.9.1461953575493; __utmc=181982502; __utmz=181982502.1461896824.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=181982502.|2=intent=want%20to%20date%20but%20nothing%20serious=1^3=age=26=1^4=Gender=Male%20United%20States=1; _gat=1; ingres=appSessionIDPrefix=bfbd5adf-9abf-4c31-abcb-bff305d4386f; _ga=GA1.2.1458391091.1461893952',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Content-Length': '97',
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
		'Accept-Language': 'en-US,en;q=0.8',
		'Accept-Encoding': 'gzip, deflate',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	}


s = requests.Session()
login = s.post(url, data=values, headers=header_data)
print 'logged in'

# message eash user
def add_to_fav(link):
	page = s.get(link)
	soup = BeautifulSoup(page.content, 'lxml')
	# get username
	username = soup.find_all('span',{'id':'username2'})
	uname = ''
	for u in username:
		uname = u.text
	fav = soup.find_all('a',{'rel':'nofollow','class':'plain'})
	fav_link = ''
	for i in fav:
		fav_link = i['href']
	s.get('http://www.pof.com/'+fav_link)
	print uname + ' added'
	

# get profile page 
def get_profiles(link):
	page = s.get(link)
	print ''
	print 'scraping profile links... '
	print ''
	soup = BeautifulSoup(page.content, 'lxml')
	profiles = soup.find_all(class_='profile')
	for div in profiles:
		people.append(div.a['href'])
		# print div.a['href']
	# send dm function
	for i in people:
		try:
			add_to_fav('http://www.pof.com/'+i)
		except:
			print 'add_to_fav function not called: '+i

# link to users not contacted
# http://www.pof.com/lastonlinemycity.aspx?SID=c2e5szexunx2yjtwxdbc5yik&guid=114640101&page=1&count=700

# get links to profile pages from newest users page
def get_links():
	recent = s.get('http://www.pof.com/lastsignup.aspx?SID=c2e5szexunx2yjtwxdbc5yik&guid=114640101&page=1&count=700')
	soup = BeautifulSoup(recent.content, 'lxml')
	try:
		# harvest get profile links from pages
		for i in range(1,21):
			next_page.append('lastsignup.aspx?SID=c2e5szexunx2yjtwxdbc5yik&guid=114640101&page='+str(i)+'&count=700')
			get_profiles('http://www.pof.com/lastsignup.aspx?SID=c2e5szexunx2yjtwxdbc5yik&guid=114640101&page='+str(i)+'&count=700')
	except:
		print 'profile page out of range'



# logout 
get_links()
s.post('http://www.pof.com/abandon.aspx')
print ''
print 'Contact me on my blog: www.icecoldtruths.blogspot.com'
print ''
print 'Check out my subreddit: /r/DarkGame'
time.sleep(120)