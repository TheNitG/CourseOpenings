# CourseOpenings
CourseOpenings is a python application that can determine if a certain course (by CRN) is open or closed. If the course is closed, it will periodically check and notify when the course is open through a Windows notifcation. This application uses multi-threading to let you search for multiple classes at once and notify you when multiple classes are open. The goal of this project is to be an open-source alternative to paid sites that tell you when a course is available. This application is currently intended for Virginia Tech Courses and won't work for other colleges. This will also not work as intended in MacOS as it uses a Windows notification package to notify users when a course becomes available.
## Getting Started
To use this python application, you must first clone the repository. Then you must follow the prerequisites.
### Prerequisites
You must have python 3.8 or newer installed for the intended experience. Older versions may work; however, there is no guarantee and 3.8 was the version used for programming.
```
https://www.python.org/downloads/ and select version 3.8 or newer. Please check the option to add python to PATH.
```
You must install the required packages noted in requirements.txt.
```
$ pip install -r requirements.txt
```
Google Chrome (not alpha or beta version unless you want to change the path in CourseOpenings.py) must also be installed on the computer to allow the application to function.
```
https://www.google.com/chrome/ and click Download Chrome. (You may unclick the usage statistics box before installing for added privacy if you wish)
```
## Using the Application
To use the application, you can run the script called RunCourseOpenings.bat by double-clicking it to launch the application. Or run the CourseOpenings.py file manually by navigating to the folder where CourseOpenings.py is located and pressing shift + right click in File Explorer and clicking the "open powershell window here" option and typing the command from below.
```
$ python CourseOpenings.py
```
# Customizing the Application
If you feel inclined, you can edit the CourseOpenings.py program and change the "interval" variable to whatever amount of time (in seconds) you want the application rechecking for course availability. You can also change the "Spring 2021" string to whichever term you would like in case the application is not up to date. Please feel free to contribute to making the application better.
# Discord Bot
A more comprehensive version with additional functionality can be found here: [CourseOpeningsBot](https://github.com/TheNitG/CourseOpeningsBot).
