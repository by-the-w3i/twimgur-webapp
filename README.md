
# __TWIMGUR webapp__

>This web app is called "twimgur" which is using twitter and imgur APIs to search with a given key. User will get three embedded twitter post and three imgur posts. The framework is based on the MVC-CGI api.

## USAGE
```bash
python3 -m mvc.server controller.py
```

## ACHEIVEMENTS
* "Your project must use the MvcCgi api I have provided"
    * POST and GET methods work
    * Avoid redundent code. Try to reuse VIEW and MODEL in controller as much as we can.
      (eg. We use "{content}" in default page instead of loading all html over again)

* "It must accept input from the user"
    * Prompt user for searching keys
    * Enable saving favorites to database (session.json) for users.

* "It must store some data and use the stored data ..."
    * Display the lastest three search keys in favorites.
    * Clicking the tag in favorites will retrieve data from database.
![444](/444.png)

* "It must call an external API or scrape another web page."
    * pythontwitter
    * imgurpython

## Limitation:
	(1) Can only show up 3 saved data in "favorite" section
	(2) User can not delete the data in database

## Example
![111](/111.png)
![222](/222.png)
![333](/333.png)
