# Automated Google Form Filler

This Python application uses Selenium to automatically fill out a Google Form multiple times, selecting random answers for each question. It simulates user interaction with radio buttons, checkboxes, and navigates through the form until the submit button is reached.

## Requirements

- Python 3.x
- Google Chrome
- ChromeDriver (Ensure it's installed and properly set up for Selenium)
- Selenium

### Installation

1. Install the necessary dependencies using `pip`:
   ```bash
   pip install selenium
   ```

2. Make sure ChromeDriver is installed and added to your system PATH. You can download it from: [ChromeDriver Download](https://sites.google.com/a/chromium.org/chromedriver/).

## How It Works

### 1. **Initialization**
- The script uses Selenium WebDriver to interact with the Google Form.
- Chrome is used as the browser to automate the process.

### 2. **Clicking Buttons & Filling Forms**
- For each question, it selects either a radio button or checkbox randomly.
- It skips the "뒤로" (Back) button and clicks the "다음" (Next) button until the "제출" (Submit) button is detected and clicked.
- The script repeats the process until the form is submitted `200` times.

---

## Code Breakdown

### Line-by-Line Explanation

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
```

- **Imports:**
  - `webdriver`: Selenium's WebDriver for automating the browser.
  - `By`: Helps locate elements by CSS selectors, XPath, etc.
  - `WebDriverWait`: Allows waiting for elements to appear.
  - `EC`: Contains expected conditions for waiting, like when an element is clickable.
  - `random`: Used for selecting random options for questions.
  - `time`: Provides sleep functionality to introduce delays between actions to mimic human behavior.

```python
driver = webdriver.Chrome()
```

- **Initialize WebDriver:**
  - Opens a new Chrome browser session.

```python
def click_element(driver, element):
    """Click the element using JavaScript to avoid interception errors."""
    try:
        driver.execute_script("arguments[0].click();", element)
        print("Element clicked using JavaScript.")
    except Exception as e:
        print(f"Error clicking element with JavaScript: {e}")
        element.click()
```

- **`click_element` Function:**
  - **Purpose**: Safely clicks on an element, first attempting using JavaScript to avoid issues like element interception.
  - **Explanation**:
    - `driver.execute_script("arguments[0].click();", element)`: Clicks the element using JavaScript.
    - If it fails, the script falls back to using the normal `.click()` method.

```python
def fill_google_form(form_url, submission_count=200):
    try:
        for i in range(submission_count):
            driver.get(form_url)
            time.sleep(2)
```

- **`fill_google_form` Function:**
  - **Purpose**: Main function that fills out the Google Form multiple times.
  - **Explanation**:
    - `driver.get(form_url)`: Navigates to the provided Google Form URL.
    - `time.sleep(2)`: Waits for 2 seconds to ensure the form has loaded properly.

```python
            print(f"Filling form submission #{i + 1}...")
```

- **Printing Status:**
  - Prints which form submission number the script is currently working on.

```python
            while True:
                questions = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
                for question in questions:
```

- **Question Loop:**
  - Finds all questions in the form, which are identified by the CSS role of "listitem".

```python
                    radio_buttons = question.find_elements(By.CSS_SELECTOR, 'div[role="radio"]')
                    if radio_buttons:
                        option = random.choice(radio_buttons[:2])
                        click_element(driver, option)
                        print("Radio button selected.")
```

- **Radio Button Handling:**
  - Finds all radio button elements within each question.
  - Randomly selects one of the first two radio options and clicks it.

```python
                    checkboxes = question.find_elements(By.CSS_SELECTOR, 'div[role="checkbox"]')
                    if checkboxes:
                        option = random.choice(checkboxes[:2])
                        click_element(driver, option)
                        print("Checkbox selected.")
```

- **Checkbox Handling:**
  - Similar to radio buttons, but for checkboxes. It randomly selects one of the first two checkboxes.

```python
                next_buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
                next_button = None
```

- **Finding Next Button:**
  - Searches for buttons that are likely to be "Next" or "Submit".

```python
                for button in next_buttons:
                    button_text = button.text.strip()
                    if button_text == "다음":  # "다음" means "Next" in Korean
                        next_button = button
                        break
                    elif button_text == "뒤로":  # Ignore "뒤로" (Back)
                        print("Skipping '뒤로' button.")
                        continue
```

- **Selecting the "Next" Button:**
  - Loops through all buttons and skips any with the text "뒤로" (Back).
  - If it finds a button with the text "다음" (Next), it selects it.

```python
                if next_button:
                    click_element(driver, next_button)
                    print("Clicked '다음' (Next) button.")
                    time.sleep(2)
```

- **Clicking "Next":**
  - If the "Next" button is found, it clicks it and waits 2 seconds before proceeding to the next page.

```python
                else:
                    submit_buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
                    for submit_button in submit_buttons:
                        if submit_button.text.strip() == "제출":  # "제출" means "Submit" in Korean
                            click_element(driver, submit_button)
                            print(f"Form #{i + 1} submitted successfully.")
                            break
```

- **Submitting the Form:**
  - If no "Next" button is found, it searches for the "Submit" button (labeled "제출" in Korean).
  - Once found, it clicks the "Submit" button.

```python
                    else:
                        print("No 'Next' or 'Submit' button found. Exiting.")
                        break
```

- **Form End Condition:**
  - If neither "Next" nor "Submit" buttons are found, the loop breaks.

```python
            time.sleep(random.uniform(2, 5))  
```

- **Random Delay Between Submissions:**
  - Adds a random delay between form submissions to mimic human behavior.

```python
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
```

- **Error Handling & Cleanup:**
  - If an error occurs, it prints the error message.
  - Closes the browser once the process is complete or if an error occurs.

```python
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfuiE5D1KytdDgjSq8QQjrPVrdJ5jzuztXzR79DT7n4nHBibw/viewform?usp=send_form&usp=embed_facebook"
```

- **Form URL:**
  - Replace this with the URL of your Google Form.

```python
fill_google_form(form_url, submission_count=200)
```

- **Calling the Function:**
  - Starts the process of filling the form 200 times.

---

## Contribution

Feel free to fork this repository, open issues, or submit pull requests for improvements!

---

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
