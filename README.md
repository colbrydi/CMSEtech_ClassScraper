# CMSEtech_ClassScraper
Scraper to collect MSU class and course information and save to a spreadsheet. This project was started by [smit1920](https://github.com/smit1920/CMSEtech_ClassScraper) and then updated by [sunxian1217](https://github.com/sunxian1217), both members of the CMSETech Team. 

## Status
This code is working but a little unstable. As of January 1st 2024 the best version was in <Dynamic_Scraper.ipynb>.  

This version requires the installation of the gekodriver.exe file (in windows) to work.  Just put the file in the main git
directory. 

## Next
See the [Issues List](https://github.com/colbrydi/CMSEtech_ClassScraper/issues) for items that need to be fixed.

## Instructions

### 1. Setup
In your terminal, clone this repo and install these dependencies:
```
pip install geckodriver-autoinstaller
pip install selenium
pip install webdriver_manager
```
If any of these dependencies don't work, or if I missed any, please let me know.

### 2. Scrape [Course Description](https://reg.msu.edu/Courses/Search.aspx)
This repo can scrape from the website for courses' general information (credits, prereqs, offered semesters, etc.) and put all the information into a pandas data frame. To use this feature, simply run <Course_Catalogue_Scraper.ipynb>.

### 3. Scrape [MSU SIS](https://student.msu.edu/splash.html)
This repo can scrape from the website for classes' specific information (schedule, instructors, location, etc.). This feature is seen in <Dynamic_Scraper.ipynb>:

- Go into Dynamic_Scraper.ipynb>
- Run the first code block
- In the second code block, there are two editable functions: `get_driver` and `login_to_SIS`. For `get_driver`, choose between `Chrome` and `Firefox` as your popup (there's no differences, but your machine might only be able to run on one, so test it out). Please note that if you run this notebook in Jupyter you will see a popup window on your screen, but you won't be able to if you use JupyterHub. For `login_to_SIS`, your authentication method can either be `Phone` or `Okta`, choose whichever one you prefer. Run the code block
- Type in your MSU NetID (netid@msu.edu) and your MSU password (Don't worry it's redacted and won't last after the session) into the popup spaces
- The function will choose the authorization method by Phone number, so you will receive an SMS code, please type this into the popup space
- Run the next three code blocks, up until the second to last one
- If you want to choose a different semester to scrape (Not Fall Semester 2024), you can change the second parameter of the `scrape_by_semester` function and also the name of the csv file you want to save your data into
- Run the last two code blocks

### 4. Make a timetable for all courses in a semester
<Make_Timetable.ipynb> will take in the csv file scraped from MSU SIS and make a timetable for all the courses in the semester:

- Run <Dynamic_Scraper.ipynb> first (instructions above)
- Go into <Make_Timetable.ipynb> and change the csv file in the third line of the first code block to the name of your csv file
- Run the notebook

### 5. Scrape for instructors' teaching history
An instructor taught many courses across multiple semesters, this repo can help them obtain the information more easily. Please note that this feature can only be run using Jupyter, not JupyterHub (it will spit out errors):

- Go into <Get_FacNames.ipynb> and run the first five code blocks
- Type in the cmsetech@msu.edu password into the popup space and run the rest of the notebook
- <Get_FacNames.ipynb> is used to convert professors' NetIDs into their names
- Go into <Scrape_by_Instructors.ipynb> and run the first code block
- In the second code block, there are two editable functions: `get_driver` and `login_to_SIS`. For `get_driver`, choose between `Chrome` and `Firefox` as your popup (there's no differences, but your machine might only be able to run on one, so test it out). Please note that if you run this notebook in Jupyter you will see a popup window on your screen, but you won't be able to if you use JupyterHub. For `login_to_SIS`, your authentication method can either be `Phone` or `Okta`, choose whichever one you prefer. Run the code block
- Type in your MSU NetID (netid@msu.edu) and your MSU password (Don't worry it's redacted and won't last after the session) into the popup spaces
- The function will choose the authorization method by Phone number, so you will receive an SMS code, please type this into the popup space
- Run the next code block
- You can change the `start_semester` and `end_semester` parameters of the `search_multiple_semesters`function depending on how far back or ahead you want to scrape
- Run the rest of the notebook. Note that this notebook takes a long time to run and might be quite fragile
