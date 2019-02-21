class Template:
	# this file will contain the templates used to render each page on the website, so that it is all stored here, instead of in the "main" class
	# general page template, which will make a page based on a name, and the content of the page
	def page (self,name,content):
		return "<html><head>" + self.stylesheet() + "<title>" + name + "</title></head><body>" + self.header() + "<h1>" + name + "</h1>" + content + "</body></html>"
	#def home():
	#	return "<html><head>" + stylesheet() + "<title>Home</title></head><body>" + header() + """<h1> Homepage </h1><p class="card">Welcome to my awesome site... awesomeness coming soon</p></body></html>"""
	#def projects():
	#	return "
	#def misc():
	#
	#def about():
	#
	#def admin():
	#
	def header(self):
		return """<div class = "topnav">
		<a href="/">Home</a>
		<a href="/projects">Projects</a>
		<a href="/misc">Misc</a>
		<a href="/about">About</a>
		<a href="/control">Admin</a>
		</div>
	"""
	def stylesheet(self):
		return """<link rel="stylesheet" href = "/style.css">"""
	def error(self):
		return """<div class = "card">
		<p>sorry, the page you're looking for actually doesn't exist...
		</p></div>"""

	def aoe(self):
		return"""<div class = "card">
		<h2> Age of Empires 2 </h2>
		<img src = "/resources/ageofempires.jpg" class = "regimage" alt ="an image from age of empires">
		<p>While I'll be honest that I am mostly writing this article so that I have some content to run tests on on the site,
		age of empires 2 is one of my favorite games of all time. I first played it when I was very young, and didn't really
		understand what was happening, or how to play. I watched my dad, and after begging for a long time, I was finally allowed
		to play, and I played it for years. I remember sharing cheat codes around with my friends at school, and setting up lan
		games at our house, where we would all have to move the disk around from person to person to get the game started on every computer.
		</p><p>I stopped playing age of empires when I got older, I didn't really touch it through most of Jr high, and highschool, but when they remastered the game ( with the HD edition on steam) I picked it up right away, and enjoyed a bit of
		a nostalgia trip, before putting it away again. But when I got to college, I ended up playing it with a bunch of roommates,
		and I realized that there was a lot of depth to the game that I had always missed, and so I started looking up video tutorials
		for strategies, like fast castling, and archer rushing, and before I knew it, I had pounded 100 hours into the game. 
		</p><p>I don't play age of empires every day, or even every month anymore, but every once in a blue moon ill boot it up to 
		enjoy some random maps with friends, or to slaughter a bunch of AI's while I listen to a podcast or something.
		</p></div>
		"""

	def dishonored(self):
		return """<div class = card>
		<h2> Dishonored </h2>
		<img src = "/resources/dishonored.jpg" class = "regimage" alt = " an image of the main protagonist from dishonored">
		<p>Dishonored probably wins the prize for "game that I have the most merch for". I love dishonored. It's a steampunky stealth
		first person RPG, and the first game that really got me into the "stealth games" genre. I really liked that you had the
		blink ability to move around the map, blinking from cover to cover, without being detected. this really made it more fun, because
		you could be agressivly stealthy, as you move around the map, and it combined really well with levels that had a great 
		deal of verticality, and a great climbing system, that let you really move around all three dimensions of a level. It 
		also had a ton of freedom to complete a mission in any way you could find. there was lots of ways to get around, and lots of 
		hidden secrets in levels, making it really fun to replay. and the world was mysterious, and beautifully depressing,
		taking place in a city that was in the midst of a plague, and it really shows, with soldiers patrolling areas, enforcing curfew, 
		or even a district full of the dead and dying, abandoned and flooded by the rest of the city.
		</p><p>if this wasn't a rough draft I would put a closing statement here, but instead here's a snarky line about how I will 
		definitely come back and finish this later ;)
		</p></div>
		"""	
