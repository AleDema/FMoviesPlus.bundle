import re,urllib,urlparse,base64,time

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib import resolvers


# SSL Web Proxy
name = 'MyAddr'

PROXY_URL = "https://ssl-proxy.my-addr.org/myaddrproxy.php/"
PROXY_PART0 = "/myaddrproxy.php/http/%s/"
PROXY_PART1 = "/myaddrproxy.php/https/%s/"
PROXY_PART1_REPLACE = "/"
PROXY_PART2A = "/myaddrproxy.php/https/"
PROXY_PART2B = "/myaddrproxy.php/http/"
PROXY_PART2_REPLACE = "//"
PROXY_PART3 = "//%s//%s"
PROXY_PART3_REPLACE = "//%s"

class proxy:
	def __init__(self):
		self.base_link = 'https://ssl-proxy.my-addr.org'
		self.name = name
		self.base_link_usage = '/'
		self.captcha = False
		self.ssl = True
		self.speedtest = 0
		self.headers = {'Connection' : 'keep-alive'}
		self.working = self.testSite()
		
	def testSite(self):
		x1 = time.time()
		http_res = client.request(url=self.base_link, output='responsecode')
		self.speedtest = time.time() - x1
		if http_res not in client.HTTP_GOOD_RESP_CODES:
			return False
		return True
		
	def request(self, url, close=True, redirect=True, followredirect=False, error=False, proxy=None, post=None, headers=None, mobile=False, limit=None, referer=None, cookie=None, output='', timeout='30', httpsskip=False, use_web_proxy=False):
	
		if headers == None:
			headers = self.headers
		else:
			headers['Connection'] = self.headers['Connection']

		return requestdirect(url=url, close=close, redirect=redirect, followredirect=followredirect, error=error, proxy=proxy, post=post, headers=headers, mobile=mobile, limit=limit, referer=referer, cookie=cookie, output=output, timeout=timeout, httpsskip=httpsskip, use_web_proxy=use_web_proxy)
			
def requestdirect(url, close=True, redirect=True, followredirect=False, error=False, proxy=None, post=None, headers=None, mobile=False, limit=None, referer=None, cookie=None, output='', timeout='30', httpsskip=False, use_web_proxy=False):
	#try:
	urlhost = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
	
	print "Requesting: %s Using via: %s" % (url, PROXY_URL)
	
	if headers == None:
		headers = {'Connection' : 'keep-alive'}
	headers['User-Agent'] = client.randomagent()
	
	page_data_string = client.request(url = PROXY_URL + url, close=close, redirect=redirect, followredirect=followredirect, error=error, proxy=proxy, post=post, headers=headers, mobile=mobile, limit=limit, referer=referer, cookie=cookie, output=output, timeout=timeout, httpsskip=httpsskip, use_web_proxy=use_web_proxy)
	
	page_data_string = unicode(page_data_string, "utf-8")

	PROXY_PART0A = PROXY_PART0 % urlhost
	PROXY_PART1A = PROXY_PART1 % urlhost
	PROXY_PART3A = PROXY_PART3 % (urlhost,urlhost)
	PROXY_PART3A_REPLACE = PROXY_PART3_REPLACE % urlhost
	
	page_data_string = page_data_string.replace(PROXY_PART0A, PROXY_PART1_REPLACE)
	page_data_string = page_data_string.replace(PROXY_PART1A, PROXY_PART1_REPLACE)
	page_data_string = page_data_string.replace(PROXY_PART2A, PROXY_PART2_REPLACE)
	page_data_string = page_data_string.replace(PROXY_PART2B, PROXY_PART2_REPLACE)
	page_data_string = page_data_string.replace(PROXY_PART3A, PROXY_PART3A_REPLACE)
	
	return page_data_string
	# except Exception as e:
		# print "Error: %s - %s" % (name, e)	
		# return None