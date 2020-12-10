# Import necessary packages
# Time package used for sleep function
from time import sleep
# Web browser packages
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
# Windows toast notification package
from win10toast import ToastNotifier
# GUI package
import tkinter as tk


# Function to find the products and their respective prices from the search term
def is_course_open(course):
    # Define the browser type and configure options to work
    options = webdriver.ChromeOptions()
    # Make it so browser runs in background
    options.add_argument('headless')
    # Path to the chromedriver included in this repository
    chrome_driver_binary = "./chromedriver"
    # Create the driver object which will be None until the try-except is executed
    driver = None
    try:
        # Path to the chrome executable (change if needed to your chrome.exe path)
        options.binary_location = r"\Program Files\Google\Chrome\Application\chrome.exe"
        # Attempt to create the driver with the necessary configurations
        driver = webdriver.Chrome(chrome_driver_binary, options=options)
    except WebDriverException:
        try:
            # Try another common path
            options.binary_location = r"\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            # Attempt to create the driver with the necessary configurations
            driver = webdriver.Chrome(chrome_driver_binary, options=options)
        except WebDriverException:
            try:
                # Try another common path
                options.binary_location = r"\Users\%UserName%\AppData\Local\Google\Chrome\Application\chrome.exe"
                # Attempt to create the driver with the necessary configurations
                driver = webdriver.Chrome(chrome_driver_binary, options=options)
            except WebDriverException:
                # Sets the status to what to do if the file isn't found
                status['text'] = 'Please go into CourseOpenings.py and enter the location of your chrome.exe file'
    # Declare the URL of the Timetable
    url = 'https://apps.es.vt.edu/ssb/HZSKVTSC.P_DispRequest'
    # Get the page
    driver.get(url)
    # Find the CRN element to edit
    course_number = driver.find_element_by_name('crn')
    # Edit the CRN element
    course_number.send_keys(str(course))
    # Find the term dropdown to interact with
    select_term = Select(driver.find_element_by_name('TERMYEAR'))
    # Select the Spring 2021 (term of interest for add/drop right now) option
    select_term.select_by_visible_text('Spring 2021')
    # Find the course availability dropdown to interact with
    select_open = Select(driver.find_element_by_name('open_only'))
    # Select the only open sections option
    select_open.select_by_visible_text('ONLY OPEN Sections')
    # Emulate the enter keypress to submit the form
    course_number.send_keys(Keys.ENTER)
    # Determine if the course is open
    is_open = 'NO SECTIONS FOUND FOR THIS INQUIRY' not in driver.page_source
    # Close the browser
    driver.quit()
    # Return True if open, else False
    return is_open


# Method to display the course status
def show_course_status():
    # Get the CRN from the text box
    crn = entry.get()
    # Get the boolean value for if the course is open or not
    status_value = is_course_open(crn)
    # Display OPEN if open, else display CLOSED
    status['text'] = 'OPEN' if status_value else 'CLOSED'
    # Update the window with the text
    window.update()
    # Attempts variable used to keep track of how many times tried (to show it is still running and retrying)
    attempt = 1
    # While the course is closed, keep retrying
    while not status_value:
        # Wait 60 seconds between each check (or whatever amount of time you want it to be in seconds)
        sleep(60)
        # Increment the number of attempts
        attempt += 1
        # Checks if the course is open now
        status_value = is_course_open(crn)
        # Updates the status text to the current status with the number of attempts and OPEN or CLOSED
        status['text'] = 'Attempt Number ' + str(attempt) + '\nCLOSED'
        # Update the window with the text
        window.update()
    # If the code gets this far, the course is open, so the status text should be updated to OPEN
    status['text'] = 'OPEN'
    # Display Windows toast notification for 60 seconds (or whatever amount of time you want it to be in seconds)
    # when the course is open (DISCLAIMER: changing the time changes the amount of time it takes before the next
    # notification to pop up, if it hasn't been the set duration amount of time, a new notification won't pop up)
    notification.show_toast("Course Opening!", "Course CRN: " + crn + " is now open!", duration=5, threaded=True)


# Create the window
window = tk.Tk()
# Makes a new Windows toast notification object
notification = ToastNotifier()
# Add a label that says Product
tk.Label(text='CRN:').pack()
# Add a text box to type your search keyword(s)
entry = tk.Entry()
entry.pack()
# Create button to submit search
submit = tk.Button(text='Search', command=show_course_status)
submit.pack()
# Create a status label that will change to OPEN or CLOSED based on whether a course is open or closed
tk.Label(text='Status:').pack()
status = tk.Label(text='No course')
status.pack()
# Run the window
window.mainloop()
