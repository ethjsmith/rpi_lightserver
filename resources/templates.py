class Template:
	# this file will contain the templates used to render each page on the website, so that it is all stored here, instead of in the "main" class
	# general page template, which will make a page based on a name, and the content of the page
	def readContent(self,obj,url):
	# this method takes an object, and runs all of the functions, appending their returns together, and then returns that. great for if you want to fill a page with something
		content = ""
		for z in dir(obj):
			if not z.startswith("__") and not z.startswith("error"):
				if callable(getattr(obj,z)):
					call = getattr(obj,z)
					# adds the content to the return, with a character set breaking between the content
					content += str(self.generatePreview(call(),z,url)) + " "
		return content
	def generatePreview(self, content,name,url):
		pre = '''<br><a class = "noa" href = "'''+url+"/"+ name + '''"> <div class = "preview"><img src = "/resources/images/''' + name + """.jpg"><h4> """ + name + "</h4>"
		content = str(content.split("</p>")[0])
		content = pre + content + """<br><br><h6> READ MORE </h6></div></a>"""
		return content
	def page (self,name,content):
		return "<html><head>" + self.stylesheet() + "<title>" + name + "</title></head><body>" + self.header(0) + "<h1>" + name + "</h1>" + """ <div class = "card "> <img src="/resources/images/""" + name + """.jpg" class = "regimage">"""  + content + "</div></body></html>"
	# generates a dynamic header based on what page is called
	def header(self,selected):
		x = """<div class = "topnav">
		<a href="/">Home</a>
		<a href="/projects">Projects</a>
		<a href="/misc">Misc</a>
		<a href="/blog">Blog</a>
		<a href="/about">About</a>
		<a href="/control">Admin</a>
		</div>
		"""
		if selected == 0:
			return x
		else :
			x = x.split(selected + "\"",1)
			x[0] = x[0] + selected + "\" class = \"current\" "
			z = " "
			for part in x:
				z+= part
			return z

	def generatePage(self,router, content):
		#this function generates pages based on custom routes (router), and the content from the (content) object
		if getattr(content,str(router),"error") != "error":
			run = getattr(content,str(router),"error")
			return self.page(str(router),run())
		else:
			return self.page("error",self.error())



		return "something"
	def stylesheet(self):
		return '''<link rel="stylesheet" href = "/style.css">
			<link rel="shortcut icon" type="image/png" href = "/resources/favicon.png"/>'''
	def error(self):
		return """<div class = "card">
		<p>sorry, the page you're looking for actually doesn't exist...
		</p></div>"""

