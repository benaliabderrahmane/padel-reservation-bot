import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
import time

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Specify the path to chromedriver.exe
service = Service(executable_path=r'C:\Users\benal\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')
options = webdriver.ChromeOptions()
options.binary_location = r'C:\Users\benal\Downloads\chrome-win64\chrome-win64\chrome.exe'

# Initialize the WebDriver with the Service object
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

logging.info("Starting script to automate login and reservation process.")

try:
    logging.info("Navigating to login page.")
    driver.get('https://tmo-padel.gestion-sports.com/connexion.php')

    logging.info("Waiting for email input to become present.")
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'email'))
    )
    email_input.send_keys('') # Add your email address here
    logging.info("Email input found and populated.")

    logging.info("Waiting for CONNEXION/INSCRIPTION button to become clickable.")
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'contact100-form-btn') and contains(text(), 'Connexion / Inscription')]"))
    )
    logging.info("Clicking the CONNEXION/INSCRIPTION button.")
    login_button.click()

    logging.info("Waiting for password input to become visible.")
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='pass']"))
    )
    logging.info("Password input found, attempting to populate it.")

    # Scroll password input into view
    driver.execute_script("arguments[0].scrollIntoView();", password_input)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='pass']")))

    try:
        # Attempt to interact with the password field
        password_input.send_keys('') # Add your password here
    except ElementNotInteractableException:
        logging.info("Password field not interactable, setting value using JavaScript.")
        driver.execute_script("arguments[0].value = 'azerty123';", password_input)

    logging.info("Password input populated.")

    logging.info("Waiting for SE CONNECTER button to become clickable.")
    connect_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'contact100-form-btn') and contains(@class, 'step-2_co') and contains(text(), 'Se connecter')]"))
    )
    logging.info("Clicking the SE CONNECTER button.")
    connect_button.click()

    logging.info("Navigating to member page and then to reservation page.")
    
    # Ensure we have landed on the member page before navigating to reservation
    WebDriverWait(driver, 10).until(
        EC.url_contains('https://tmo-padel.gestion-sports.com/membre')
    )
    driver.get('https://tmo-padel.gestion-sports.com/membre/reservation.html')

    logging.info("Waiting for sport selection dropdown to become present.")
    sport_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'sport'))
    )
    sport_dropdown.click()

    logging.info("Selecting Padel option.")
    padel_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//option[@value='568']"))
    )
    padel_option.click()

    logging.info("Waiting for the date input to become clickable.")
    date_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'date'))
    )
    logging.info("Clicking the date input.")
    date_input.click()

    # Wait for the calendar to be fully interactive
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'ui-datepicker-next'))
    )

    logging.info("Navigating to the correct month and year if required, then selecting the date.")
    
    try:
        while True:
            displayed_month_year = driver.find_element(By.CLASS_NAME, 'ui-datepicker-title').text
            if 'August' in displayed_month_year and '2024' in displayed_month_year:
                break

            next_button = driver.find_element(By.CLASS_NAME, 'ui-datepicker-next')
            if "ui-state-disabled" not in next_button.get_attribute("class"):
                ActionChains(driver).move_to_element(next_button).perform()
                next_button.click()
                time.sleep(0.5)  # Wait for the calendar to update
            else:
                logging.error("Next button is disabled, unable to navigate to the correct month.")
                break

        # Click on the specific date
        specific_date = driver.find_element(By.XPATH, "//a[text()='28']")
        specific_date.click()
        logging.info("Selected date 29/08/2024.")

    except Exception as e:
        logging.error(f"Failed to select the date: {e}")

    # This is where you select the time "09:00"
    logging.info("Waiting for the time dropdown to become clickable.")
    time_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'heure'))
    )
    time_dropdown.click()

    logging.info("Selecting 09:00 option.")
    time_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[@id='heure']/option[@value='09:00']"))
    )
    time_option.click()

    logging.info("Time 09:00 selected successfully.")

    # Wait for court elements to be present before interacting with them
    logging.info("Waiting for court elements to become present.")
    courts = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'bloccourt'))
    )

    logging.info("Listing all available times across all courts.")

    available_times = []
    selected_time = '09:00'  # Adjust this if you want to select a different time
    selected_button = None

    try:
        for court in courts:
            # Find all time buttons within the court
            time_buttons = court.find_elements(By.XPATH, ".//button[contains(@class, 'btn_creneau')]")

            for button in time_buttons:
                time_text = button.text.strip()
                if time_text:
                    available_times.append(time_text)
                    logging.info(f"Available time found: {time_text}")
                    if time_text == selected_time:
                        selected_button = button  # Select the button for the desired time

        if available_times:
            logging.info(f"List of all available times: {available_times}")
        else:
            logging.error("No available times found.")

        # Click on the selected time button
        if selected_button:
            logging.info(f"Clicking the selected time button for {selected_time}.")
            selected_button.click()
        else:
            logging.error(f"Desired time {selected_time} not found.")
            driver.quit()
            exit()

        # Click on the "Partenaire" elements
        logging.info("Clicking on the Partenaire elements.")
        partenaires = driver.find_elements(By.XPATH, "//img[contains(@class, 'openmodalpartenaires')]")
        for partenaire in partenaires:
            partenaire.click()
            time.sleep(1)  # Adjust this delay if necessary for modal interactions

        # Scroll to the reservation button
        logging.info("Scrolling to the reservation confirmation button.")
        reserve_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'buttonaddresa')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", reserve_button)
        time.sleep(1)  # Allow time for any scrolling animations

        # Click on the "Réserver" button
        logging.info("Clicking the reservation confirmation button.")
        reserve_button.click()

        # Click on "Payer sur place"
        logging.info("Waiting for 'Payer sur place' option.")
        payer_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'textConfirmPartie') and contains(text(), 'Payer sur place')]"))
        )
        payer_button.click()

        logging.info("Reservation and payment process completed successfully.")

    except Exception as e:
        logging.error(f"Failed during the time selection or reservation process: {e}")

except TimeoutException as e:
    logging.error(f"TimeoutException: {e}")
    # Debugging aid: Log visible element details if an exception occurs
    visible_elements = driver.find_elements(By.XPATH, "//*[not(ancestor-or-self::*[contains(@style, 'display: none') or contains(@style, 'visibility: hidden')])]")
    logging.info(f"Number of visible elements on the page: {len(visible_elements)}")
    if len(visible_elements) > 0:
        logging.info("List of visible elements:")
        for elem in visible_elements[:10]:  # Limit to the first 10 elements for brevity
            logging.info(f"Visible Element: Tag={elem.tag_name}, Text={elem.text}")

except NoSuchElementException as e:
    logging.error(f"NoSuchElementException: {e}")
except ElementClickInterceptedException as e:
    logging.error(f"ElementClickInterceptedException: {e}")
except ElementNotInteractableException as e:
    logging.error(f"ElementNotInteractableException: {e}")
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
finally:
    logging.info("Adding delay before quitting driver.")
    time.sleep(100)  # 100 second delay before quitting
    logging.info("Quitting driver.")
    driver.quit()
