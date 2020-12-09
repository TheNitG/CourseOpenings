# Import necessary packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import requests
from bs4 import BeautifulSoup
import tkinter as tk


# Function to find the products and their respective prices from the search term
def is_course_open(course):
    # Define the browser type and configure options to work
    options = webdriver.ChromeOptions()
    # Path to the chrome executable (change if needed to your chrome.exe path)
    options.binary_location = r"\Program Files\Google\Chrome\Application\chrome.exe"
    # Make it so browser runs in background
    options.add_argument('headless')
    # Path to the chromedriver included in this repository
    chrome_driver_binary = "./chromedriver"
    # Create the driver with the necessary configurations
    driver = webdriver.Chrome(chrome_driver_binary, options=options)
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
    driver.close()
    # Return True if open, else False
    return is_open


# Method to display the course status
def show_course_status():
    # Get the boolean value for if the course is open or not
    status_value = is_course_open(entry.get())
    # Display OPEN if open, else display CLOSED
    status['text'] = 'OPEN' if status_value else 'CLOSED'


# Create the window
window = tk.Tk()
# Add a label that says Product
tk.Label(text='CRN:').pack()
# Add a text box to type your search keyword(s)
entry = tk.Entry()
entry.pack()
# Create button to submit search
submit = tk.Button(text='Search', command=show_course_status)
submit.pack()
tk.Label(text='Status:').pack()
status = tk.Label(text='No course')
status.pack()
# Run the window
window.mainloop()
