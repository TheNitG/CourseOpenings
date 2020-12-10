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
# Multithreading package
from threading import Thread


# Function to find the products and their respective prices from the search term taking in a CRN as an argument
def is_course_open(crn, driver):
    # Get the page
    driver.get(url)
    # Find the CRN element to edit
    course_number = driver.find_element_by_name('crn')
    # Edit the CRN element
    course_number.send_keys(str(crn))
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
    # Close the web-driver
    driver.close()
    # Return True if open, else False
    return is_open


# Method to display the course status
def show_course_status():
    # Get the CRN from the entry box
    crn = entry.get()
    # Make the web-driver
    driver = make_driver()
    # Add the web-driver to the list of web-drivers
    drivers.append(driver)
    # Get the boolean value for if the course is open or not
    status_value = is_course_open(crn, driver)
    # Display OPEN if open, else display CLOSED
    status['text'] = crn + ' OPEN' if status_value else ' CLOSED'
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
        status_value = is_course_open(crn, driver)
        # Updates the status text to the current status with the number of attempts and OPEN or CLOSED
        status['text'] = crn + ' Attempt Number ' + str(attempt) + '\nCLOSED'
        # Update the window with the text
        window.update()
    # If the code gets this far, the course is open, so the status text should be updated to OPEN
    status['text'] = crn + ' OPEN'
    # Update the window with the text
    window.update()
    # Quit the web-driver
    driver.quit()
    # Display Windows toast notification for 60 seconds (or whatever amount of time you want it to be in seconds)
    # when the course is open (DISCLAIMER: changing the time changes the amount of time it takes before the next
    # notification to pop up, if it hasn't been the set duration amount of time, a new notification won't pop up)
    notification.show_toast("Course Opening!", "Course CRN: " + crn + " is now open!", duration=5, threaded=True)


# Make the driver by attempting to use different chrome.exe paths and throw a WebDriverException if unsuccessful
def make_driver():
    # Define the browser type and configure options to work
    options = webdriver.ChromeOptions()
    # Make it so browser runs in background
    options.add_argument('headless')
    # Path to the chromedriver included in this repository
    chrome_driver_binary = "./chromedriver"
    # Create the driver object which will be None until the try-except is executed
    try:
        # Path to the chrome executable (change if needed to your chrome.exe path)
        options.binary_location = r"\Program Files\Google\Chrome\Application\chrome.exe"
        # Attempt to create the driver with the necessary configurations
        driver_attempt = webdriver.Chrome(chrome_driver_binary, options=options)
        # Return if successful
        return driver_attempt
    except WebDriverException:
        try:
            # Try another common path
            options.binary_location = r"\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            # Attempt to create the driver with the necessary configurations
            driver_attempt = webdriver.Chrome(chrome_driver_binary, options=options)
            # Return if successful
            return driver_attempt
        except WebDriverException:
            try:
                # Try another common path
                options.binary_location = r"\Users\%UserName%\AppData\Local\Google\Chrome\Application\chrome.exe"
                # Attempt to create the driver with the necessary configurations
                driver_attempt = webdriver.Chrome(chrome_driver_binary, options=options)
                # Return if successful
                return driver_attempt
            except WebDriverException:
                # Sets the status to what to do if the file isn't found
                status['text'] = 'Please go into CourseOpenings.py and enter the location of your chrome.exe file'
                raise WebDriverException('Please go into CourseOpenings.py and enter the path of your chrome.exe file')


# Method that properly closes the webdriver, window, and the program
def close_all():
    # Quit all web-drivers
    for driver in drivers:
        driver.quit()
    # Quit the window
    window.destroy()
    # Exit the program
    exit(0)


# Run the show_course_status method as a thread
def thread_course_status():
    # Create the thread
    current_thread = Thread(target=show_course_status)
    # Make thread close when program closes
    current_thread.daemon = True
    # Start the thread
    current_thread.start()


# Create a list to store all web-drivers
drivers = []
# Create the window
window = tk.Tk()
# Makes a new Windows toast notification object
notification = ToastNotifier()
# Declare the URL of the Timetable
url = 'https://apps.es.vt.edu/ssb/HZSKVTSC.P_DispRequest'
# Create a quit button that has the close_all method
tk.Button(text='Quit', command=close_all).pack(side=tk.BOTTOM)
# Add a label that says Product
tk.Label(text='Add CRN:').pack()
# Add a text box to type your search keyword(s)
entry = tk.Entry()
entry.pack()
# Create button to submit search
submit = tk.Button(text='Search', command=thread_course_status)
submit.pack()
# Create a status label that will change to OPEN or CLOSED based on whether a course is open or closed
tk.Label(text='Status:').pack()
status = tk.Label(text='No course')
status.pack()
# Run the window
window.mainloop()
