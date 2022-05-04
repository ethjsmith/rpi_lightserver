# RPI lightserver
a project I made to host my own website, with a bunch of backend functionality, like controlling the IOT lights in my house. Also doubles as a blog ( when I bother to write articles for it )

## Requirements
Python 3

#### Packages:
- Flask
- flask_login
- flask_sqlalchemy
#### Programs:
 [rpi_rf](https://github.com/milaq/rpi-rf) is the program I use to send rf signals. it really simplifies the process, and it works great.
#### Config File:
Create a file called secret.py, which contains values for configuring the RF sender module, and the IO pin that the transmitter is connected to, as well as a secret key. Attached is an example config.
```python
def system():
	key="""qwerty"""
	return key
def config():
        # This is the GPIO data pin that is connected to the RF sender module
        rpi_gpio_pin = '21'
        # These are the codes sent by the RPI to toggle lights
        outlet1on = '1655303'
        outlet1off = '1655302'
        # there should be 2 codes per light, one for on, and one for off ( if it works like mine does )
        outlet2on = '6832647'
        outlet2off = '6832646'

        return [rpi_gpio_pin,outlet1on,outlet1off,outlet2on,outlet2off]
```
#### Database setup:
currently you can create and load the database with some defaults by running the `initalize_db.py` file

## TOD0
- [ ] rework site style, and add more templates for generic pages.
- [ ] Standardize naming conventions ( specifically Post/Article)
- [ ] improve ability to add paragraphs to articles ?
- [ ] look into/ implement WTF forms
- [ ] add logical db link between articles(content) and users
- [ ] give admins better ability to manage users
## Known/tracked bugs
- [ ] generictemplate.html rework to markup object instead of `|safe` variable ( possible security)
