Web of authors is a tool for social networking to find connections between authors via the papers that the have written on a specific subject and documented in the Web Of Science.
This tool can be used to see the achievements of peers or the connections between scientists. 

Usage:

There are three major components to this project. 

1. Data retrieval from web of science using selenium webdriver.
Use webofsciencescraper.py to scrape the data from web of science. webofsciencescraper.py takes two arguments. The first argument is the URL of the web of science page that you would like to scrape and the second is the file that you would like to store the data in. Make sure you put the url in parenthesis in order to avoid any string escaping errors.

2. Convert the data from paper profiles to author profiles.
 
For this use amp.py. apm.py takes two arguments as well. The first argument is the destination file of step one and the second argument is another JSON file where you can store the author profiles.

3. Display of data using the D3.js library and the data captured in step one. 
This uses zoom.php. To change the file that it requests from, you will have to go into the source code and change it directly.

Notes: 
-links and redirections need to be changed to fit the folder in which they are stored.
-These files will not work off server. JS files attempting to access JSON files
-When getting the web of science link, you must be in the Core Collection setting(not “All Databases”).
- You can run the names through last name fixer to merge potentially duplicate names.

Future:
Ideally I wanted to make a profile for each author that showed the papers that they wrote and a list of people that they have worked with.

There is a glitch in apm.py that I have not been able to figure out. This glitch excludes some researchers from the Co-Authors tuple of others leading to a large mess on the graph when multiple siblings of the same parent node are clicked.