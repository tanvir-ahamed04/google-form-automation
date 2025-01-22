from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time


driver = webdriver.Chrome()

def click_element(driver, element):
    """Click the element using JavaScript to avoid interception errors."""
    try:
        driver.execute_script("arguments[0].click();", element)
        print("Element clicked using JavaScript.")
    except Exception as e:
        print(f"Error clicking element with JavaScript: {e}")
        element.click()

def fill_google_form(form_url, submission_count=200):
    try:
        for i in range(submission_count):
            driver.get(form_url)
            time.sleep(2)

            print(f"Filling form submission #{i + 1}...")

            while True:
                questions = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
                for question in questions:

                    radio_buttons = question.find_elements(By.CSS_SELECTOR, 'div[role="radio"]')
                    if radio_buttons:
                        option = random.choice(radio_buttons[:2])
                        click_element(driver, option)
                        print("Radio button selected.")


                    checkboxes = question.find_elements(By.CSS_SELECTOR, 'div[role="checkbox"]')
                    if checkboxes:

                        option = random.choice(checkboxes[:2])
                        click_element(driver, option)
                        print("Checkbox selected.")

                next_buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
                next_button = None

                for button in next_buttons:
                    button_text = button.text.strip()
                    if button_text == "다음":  # "다음" means "Next" in Korean
                        next_button = button
                        break
                    elif button_text == "뒤로":  # Ignore "뒤로" (Back)
                        print("Skipping '뒤로' button.")
                        continue

                if next_button:
                    click_element(driver, next_button)
                    print("Clicked '다음' (Next) button.")
                    time.sleep(2)  # Wait for the next page to load
                else:
                    # If no "다음" button is found, check for the "제출" (Submit) button
                    submit_buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
                    for submit_button in submit_buttons:
                        if submit_button.text.strip() == "제출":  # "제출" means "Submit" in Korean
                            click_element(driver, submit_button)
                            print(f"Form #{i + 1} submitted successfully.")
                            break
                    else:
                        print("No 'Next' or 'Submit' button found. Exiting.")
                        break

            # Add a delay between submissions
            time.sleep(random.uniform(2, 5))  

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

# URL of your Google Form
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfuiE5D1KytdDgjSq8QQjrPVrdJ5jzuztXzR79DT7n4nHBibw/viewform?usp=send_form&usp=embed_facebook"

# Call the function to fill the form 200 times
fill_google_form(form_url, submission_count=200)
