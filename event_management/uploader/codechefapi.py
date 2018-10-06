import re
from urllib import request
from urllib.request import Request
from bs4 import BeautifulSoup


def is_url(url):
	url_pattern = r'^https?://(.*?)\.(.*?)$'
	result = re.findall(url_pattern, url)

	if len(result) is 0:
		return False
	return True

def make_url(url, ext):
	if ext[0] is '/':
		return url + ext
	else:
		return url + '/' + ext



class ExtractData(BeautifulSoup):

	#static variable
	# stop_words = set(stopwords.words("english"))



	def  __init__(self, response, verbose=False):

		self.verbose = verbose

		# for i in symbols_and_stops_words:
		#         ExtractData.stop_words.add(i)
		super().__init__(response, "lxml")
		self.response = response


		# self.remove_tag("script");
		# self.remove_tag("style");
		# self.remove_tag("meta");
		# self.remove_tag("head");

		# self.get_text()


	def collect_data(self):
		data = dict()

		data['rating'] = int(self.find('div', 'rating-number').string)

		user_details = self.find('section', 'user-details-container')

		solved = self.find('section', 'rating-data-section problems-solved')
		wa = re.search(r'(?<=name:\\\'wrong_answers\\\',y:)[0-9]+',self.response)
		sa = re.search(r'(?<=name:\\\'solutions_accepted\\\',y:)[0-9]+',self.response)
		tle = re.search(r'(?<=name:\\\'time_limit_exceeded\\\',y:)[0-9]+',self.response)
		ce = re.search(r'(?<=name:\\\'compile_error\\\',y:)[0-9]+',self.response)
		spa = re.search(r'(?<=name:\\\'solutions_partially_accepted\\\',y:)[0-9]+',self.response)
		rte = re.search(r'(?<=name:\\\'runtime_error\\\',y:)[0-9]+',self.response)



		data['wrong_answers'] = int(wa.group())
		data['solutions_accepted'] = int(sa.group())
		data['time_limit_exceeded'] = int(tle.group())
		data['compile_error'] = int(ce.group())
		data['solutions_partially_accepted'] = int(spa.group())
		data['runtime_error'] = int(rte.group())


		# for i in script:
		#     print(dir(i))
		# print(script)
		#
		# print(script)

		solved = solved.find_all('h5')


		data['fully_solved'] = int(re.search(r'\d+',solved[0].string).group())
		data['partially_solved'] = int(re.search(r'\d+',solved[1].string).group())


		return data
	# def remove_tag(self, tag_name):
	#
	#     for _tag in self.findAll(tag_name):
	#             _tag.decompose()



	# def get_text(self):
	#
	#     self.data = [
	#             word
	#             for text in self.strings
	#             for word in word_tokenize(text)
	#             ]
	#
	#     self.frequency_data = Counter()
	#
	#     for word in self.data:
	#
	#         word = word.lower()
	#         if word in ExtractData.stop_words:
	#             continue
	#         if re.match(r'(\\n)+', word):
	#             continue
	#         if re.match(r'(\\x[a-z0-9]{2,})+', word):
	#             continue
	#         self.frequency_data[word]+=1
	#
	#     print(self.frequency_data.most_common(60)



class Spider:

	def __init__(self,url, verbose=False):
		self.url = url
		self.domain = ''
		self.response = ''
		self.verbose = verbose
		self.get_domain()
		self.USER_AGENT = '''Mozilla/5.0
							 (Macintosh; Intel Mac OS X 10_9_3)
							 AppleWebKit/537.75.14 (KHTML, like Gecko)
							 Version/7.0.3 Safari/7046A194A'''
		if(self.verbose):
			print("Visiting domain : " + self.domain)
		self.urls = []
		self.visit()

	def get_domain(self):

		pattern = r'(http[s]?://[a-zA-Z0-9]+?\.?[a-zA-Z0-9\-]+\.[a-z]{2,})'
		result = re.findall(pattern, self.url)

		if(result):
			self.domain = result[0]

	def visit(self):

			if(self.verbose):
				print("Visiting {}".format(self.url))

			try:
				request_obj = Request(self.url)
				request_obj.add_header('User-Agent',self.USER_AGENT)
				request_obj.add_header('Content-Type', 'text/html')
				response_obj = request.urlopen(request_obj)
				self.response = str(response_obj.read());
				self.find_urls(str(self.response))
			except Exception as e:
				print(e)

			#print(self.urls)


	def find_urls(self, response):

		url_find_pattern = r'<a href="?\'?([^"\'>]*)'
		results = re.findall(url_find_pattern, response)

		if(results):

			for url in results:
				if is_url(url):
					self.urls.append(url)
				else:
					self.urls.append(make_url(self.domain, url))


urls = []

def get_data_by_username(url):

	spider = Spider(url)

	data = ExtractData(spider.response)

	return data.collect_data()

if __name__ == '__main__':
	content = ""
	url = "https://codechef.com/users/Ankit_22"
	urls.append(url)
	spider = Spider(url)

	# with open('test.txt', 'w') as f:
	#     f.write(spider.response)

	data = ExtractData(spider.response)

	data.collect_data()


	mydivs = data.find("div","rating-number")


	# print(mydivs)
	# print(dir(data))



	#spider.find_urls(content)
	#print(content)
