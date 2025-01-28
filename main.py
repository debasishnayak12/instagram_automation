from playwright.sync_api import sync_playwright
import os
import time
import random

# Function to add random delays between actions
def random_delay(min_seconds=1, max_seconds=5):
    time.sleep(random.randint(min_seconds, max_seconds))

# Function to log in to Instagram
def login(page, username, password):
    try:
        print(f"Logging in as {username}...")
        page.goto("https://www.instagram.com/accounts/login/")
        random_delay(2, 4)

        # Fill in the login form
        page.fill("input[name='username']", username)
        random_delay(1, 3)
        page.fill("input[name='password']", password)
        random_delay(1, 3)

        # Click the login button
        page.click("button[type='submit']")
        random_delay(5, 7)  # Wait for login to complete

        # Handle "Save Login Info" prompt (if it appears)
        try:
            page.click("button:has-text('Not Now')", timeout=5000)
        except:
            pass

        print(f"Logged in successfully as {username}.")
        return True

    except Exception as e:
        print(f"Login failed for {username}: {str(e)}")
        return False

# Function to upload media and add caption
def upload_media(page, file_path, caption):
    try:
        print("Navigating to the create post page...")
        page.goto("https://www.instagram.com/")
        random_delay(3, 5)

        # Click the "Create" button
        create_button = page.wait_for_selector("svg[aria-label='New post']", timeout=10000)
        create_button.click()
        print("create button clicked")
        random_delay(3, 5)

        # Wait for the file input to appear
        file_input = page.wait_for_selector("input[type='file']", timeout=10000)
        random_delay(2, 4)

        # Verify file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Verify file type is allowed
        allowed_extensions = ('.jpg', '.jpeg', '.png', '.mp4', '.mov')
        if not file_path.lower().endswith(allowed_extensions):
            raise ValueError(f"File type not allowed. Please use: {allowed_extensions}")

        # Upload the file
        file_input.set_input_files(file_path)
        random_delay(5, 7)  # Wait for the file to upload

        # Add caption (if provided)
        if caption:
            caption_field = page.wait_for_selector("textarea[aria-label='Write a caption…']", timeout=10000)
            caption_field.fill(caption)
            random_delay(2, 4)

        # Click the share button
        share_button = page.wait_for_selector("button:has-text('Share')", timeout=10000)
        share_button.click()
        random_delay(5, 7)  # Wait for the post to complete

        print("Media uploaded successfully.")
        return True

    except Exception as e:
        print(f"Media upload failed: {str(e)}")
        return False

# Function to log out of Instagram
def logout(page):
    try:
        print("Logging out...")
        page.goto("https://www.instagram.com/accounts/logout/")
        random_delay(3, 5)

        # Click the logout button
        page.click("button:has-text('Log Out')")
        random_delay(3, 5)

        print("Logged out successfully.")
        return True

    except Exception as e:
        print(f"Logout failed: {str(e)}")
        return False

# Main function to automate the process for multiple accounts
def automate_instagram(accounts, file_path, caption):
    with sync_playwright() as p:
        # Launch a browser
        browser = p.chromium.launch(headless=False)  # Set headless=True for production
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={"width": 1280, "height": 1024}
        )
        page = context.new_page()

        for account in accounts:
            username = account["username"]
            password = account["password"]

            # Log in
            if not login(page, username, password):
                continue  # Skip to the next account if login fails

            # Upload media
            if not upload_media(page, file_path, caption):
                logout(page)  # Log out if upload fails
                continue  # Skip to the next account

            # Log out
            if not logout(page):
                continue  # Skip to the next account if logout fails

            print(f"Completed process for {username}.\n")

        # Close the browser
        browser.close()

# List of accounts (replace with your own)
accounts = [
    {"username": "systummm.hr0001", "password": "test@123"},
    {"username": "systummm.hr0001", "password": "test@123"}
    # Add up to 100 accounts here
]

# File path and caption
file_path = r"C:\Debu\pikachu.PNG" # Replace with your file path
caption = "Check out this cool post!"  # Replace with your caption

# Run the automation
automate_instagram(accounts, file_path, caption)