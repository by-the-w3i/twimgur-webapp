#!/usr/local/bin/python3
import cgi,cgitb, os
from mvc import mvccgi
from mvc.mvccgi import BaseController, BaseModel

# external API twitter
import twitter
from imgurpython import ImgurClient


class MyController(BaseController):
	headers = ["key", "twitter_code", "imgur_code"]
	model = BaseModel("session.json", headers)

	def twimgur_POST(self, params):
		if 'searchkey' in params:
			name = params['searchkey'].value.strip()
			if name != "":
				check = self.model.find({"key":name})
				if len(check) > 0:
					data_tb = check[0]
					return self.loadPage("result", "result.html", {"back_key":"", "title":"result", "twitterPart":data_tb["twitter_code"], "imgurPart":data_tb["imgur_code"]})
				twitterResult = self.searchTwitter(self.getTwitterAPI(), name)
				imgurResult = self.searchImgur(self.getImgurAPI(), name)
				self.model.updateOrAdd({"key":name},{"twitter_code":twitterResult, "imgur_code":imgurResult})
				return self.loadPage("result", "result.html", {"back_key":name,"title":"result", "twitterPart":twitterResult, "imgurPart":imgurResult})
		if "back" in params:
			if params["back"].value.strip()!="":
				self.model.delete({"key":params["back"].value.strip()})
		return self.twimgur_GET(params)


	def twimgur_GET(self, params):
		data_key = ""
		if "fav1" in params and params["fav1"].value.strip() != "":
			data_key = params["fav1"].value.strip()
		elif "fav2" in params and params["fav2"].value.strip() != "":
			data_key = params["fav2"].value.strip()
		elif "fav3" in params and params["fav3"].value.strip() != "":
			data_key = params["fav3"].value.strip()
		if data_key!="":
			data_tb = self.model.find({"key":data_key})[0]
			return self.loadPage("result", "result.html", {"back_key":"", "title":"result", "twitterPart":data_tb["twitter_code"], "imgurPart":data_tb["imgur_code"]})
		return self.loadPage("search", "search.html", self.fillTheFavo())

	def getTwitterAPI(self):
		return twitter.Api(consumer_key="oMjKGhkDyR0YukQSbTcE9oE61",
		                  consumer_secret="psUjPY2RByV08saoxyNl2WIvPeaFTb4NZd9fyrCLZRyeOb86wg",
		                  access_token_key="928301044748226560-NcKXs0yExJvlxHqTtXibrsk0hNOGk8J",
		                  access_token_secret="M5K2XRngoeVPjjUOsp33aiZ9c1wBH1XhXjsD8n2rxtfja")

	def searchTwitter(self, api, key):
		result = ""
		for status in api.GetSearch(term=key, count=3):
			result+=api.GetStatusOembed(status.id)['html']
		return result

	def getImgurAPI(self):
		client_id = '958c2d905df65ca'
		client_secret = '9a3ea56c9dd06cdf9507008afa57022aeb13b85b'
		return ImgurClient(client_id, client_secret)

	def searchImgur(self, client, key):
		items = client.gallery_search(key)
		cnt = 0
		result = ""
		for item in items:
			itemID = item.id
			if item.is_album:
				itemID = 'a/'+itemID
			if cnt == 3:break
			result += '<blockquote class="imgur-embed-pub" lang="en" data-id="{}"><a href="//imgur.com/{}">{}</a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>'.format(itemID, item.id, item.title)
			cnt += 1
		return result

	def fillTheFavo(self):
		tb = {"favtxt1":"", "favtxt2":"", "favtxt3":"", "favv1":"", "favv2":"", "favv3":""}
		cnt = 1
		for k in self.model.storage["data"][0][-1::-1]:
			tb["favv"+str(cnt)] = k
			tb["favtxt"+str(cnt)] = k
			cnt += 1
			if cnt > 3:
				break
		return tb

	def loadPage(self, title, f, params):
		page = self.viewer.getPage(f, params)
		return self.viewer.getDefaultPage({"title":title, "content":page})



cgitb.enable()
v = mvccgi.BaseViewer("./default.html")
c = MyController(v)
method = os.environ['REQUEST_METHOD']

c.respond(cgi.FieldStorage(), method)
