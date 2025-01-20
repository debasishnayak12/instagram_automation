from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import os

def instagram_setup_driver(username, password):
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # Create a Service object
        service = Service("C:\\Program Files\\driver\\chromedriver.exe")
        
        # Initialize the driver with service and options
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Open Instagram login page
        driver.get("https://www.instagram.com/accounts/login/")

        time.sleep(20)
        
        # Wait for elements to be present
        wait = WebDriverWait(driver, 10)
        
        # Wait for username field and enter credentials
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.send_keys(username)
        
        # Find and enter password
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(password)

        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Add a small delay before any further actions
        time.sleep(5)

        new_post_button = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "[aria-label='New post']"  # Adjust selector based on Instagram's UI
        )))
        new_post_button.click()
        time.sleep(2)

        
        return driver
    

        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if 'driver' in locals():
            driver.quit()
        return None
    
def upload_media(driver, file_path,caption):
    try:
        # Wait for the file input element
        # Note: Instagram's file input usually has a [type='file'] attribute
        wait = WebDriverWait(driver, 20)
        
        # Look for the file input element
        # This selector might need to be adjusted based on Instagram's current DOM
        file_input = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 
            "input[type='file']"
        )))
        time.sleep(2)
        # Verify file exists before attempting upload
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Verify file type is allowed
        allowed_extensions = ('.jpg', '.jpeg', '.png', '.mp4', '.mov')
        if not file_path.lower().endswith(allowed_extensions):
            raise ValueError(f"File type not allowed. Please use: {allowed_extensions}")
        time.sleep(2)
            
        # Send the file path to the input element
        file_input.send_keys(file_path)
        
        print("Uploading file...")
        # Wait for upload to complete (look for a relevant element that appears after upload)
        # wait.until(EC.presence_of_element_located((
        #     By.CSS_SELECTOR, 
        #     "[aria-label='Post preview']"  # Adjust selector based on Instagram's UI
        # )))
        time.sleep(3)
        print("Finding next button")
        # next_button = driver.find_element_by_name("Next")
        # next_button = driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div/div[3]/div/div")
        # next_button = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[5]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div/div[3]/div/div")))
        # next_button2 = driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div/div[3]/div/div")
        # next_button.click()
        # next_button = wait.until(EC.element_to_be_clickable((
        #     By.XPATH,
        #     "//button[contains(text()='Next')]"
        # )))
        next_button = wait.until(EC.element_to_be_clickable((
                                By.XPATH,
                                "//div[@role='button'][@tabindex='0'][text()='Next']"
                            )))
        print("Next button found")
        next_button.click()
        print("Nex button 2 searching ")
        time.sleep(10)
        next_button2=wait.until(EC.element_to_be_clickable((
                                By.XPATH,
                                "//div[@role='button'][@tabindex='0'][text()='Next']"
                            )))
        print("next 2 found")
        next_button2.click()

        time.sleep(5)

        print("caption finding")
        caption_field = driver.find_element(By.XPATH, "//div[@aria-label='Write a caption...']")
        print("Caption found")
        caption_field.click()
        caption_field.send_keys(caption)
        time.sleep(5)
        print("Share button finding")
        share_button = driver.find_element(By.XPATH, "//div[@role='button'][@tabindex='0'][text()='Share']")
        print('Share button found ')
        share_button.click()

        time.sleep(5)
        print('Success message finding ')
        success_message = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//*[contains(text(), 'Your post has been shared')]"
        )))

        
        # Wait for message to be visible
        wait.until(EC.visibility_of(success_message))
        print("Success messag found")
        
        
        print("File uploaded successfully!")
        return True
    

    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        # Replace with your credentials and file path
        username = "systummm.hr0001"
        password = "test@123"
        file_path = r"C:\Debu\pikachu.PNG"  # Use raw string with full path
        caption = "Hello, Pikachu!"
        
        driver = instagram_setup_driver(username, password)
        if driver:
            if upload_media(driver, file_path,caption):
                # Continue with adding caption, etc.
                print("Proceed with adding caption and other details...")
            else:
                print("Failed to upload media")
                
    except Exception as e:
        print(f"Main error: {str(e)}")
    finally:
        if 'driver' in locals() and driver:
            driver.quit()