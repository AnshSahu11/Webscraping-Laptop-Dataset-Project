import time
import random

# Selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Undetected ChromeDriver
import undetected_chromedriver as uc


def main():
    # 1. Setup undetected_chromedriver with custom options
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/90.0.4430.93 Safari/537.36")

    # 2. Initialize driver (only once!)
    driver = uc.Chrome(version_main=133, options=options)

    driver.get("https://www.smartprix.com/laptops")
    print("Page loaded: https://www.smartprix.com/laptops")
    time.sleep(5)  # Allow extra time for the page to load fully

    # 3. Interact with checkboxes (using explicit waits)
    # try://*[@id="app"]/main/div[1]/div[3]/div[3]
    #     # Wait for the first checkbox to be clickable and click it
    #     checkbox1 = WebDriverWait(driver, 15).until(
    #         EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/main/aside/div/div[5]/div[2]/label[1]/input'))
    #     )
    #     checkbox1.click()
    #     print("Checkbox 1 clicked.")
    #     time.sleep(3)
    #
    #     # Wait for the second checkbox to be clickable and click it
    #     checkbox2 = WebDriverWait(driver, 15).until(
    #         EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/main/aside/div/div[5]/div[2]/label[2]/input'))
    #     )
    #     checkbox2.click()
    #     print("Checkbox 2 clicked.")
    #     time.sleep(3)
    # except Exception as e:
    #     print("Error clicking checkboxes:", e)

    # 4. Repeatedly click "Load More" until no more content loads
    counter = 1
    old_height = driver.execute_script('return document.body.scrollHeight')

    while True:
        try:
            # Wait for the "Load More" button to be clickable
            load_more_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/main/div[1]/div[3]/div[3]'))
            )
            # Scroll the button into view
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_btn)
            time.sleep(1)

            try:
                load_more_btn.click()
            except Exception as click_error:
                print("Normal click failed, trying JavaScript click:", click_error)
                driver.execute_script("arguments[0].click();", load_more_btn)

            print(f"Clicked Load More {counter} times.")
            counter += 1

            # Wait a bit for new content to load (randomized to mimic human behavior)
            time.sleep(3 + random.random() * 2)

            # Check page height to determine if new content has been loaded
            new_height = driver.execute_script('return document.body.scrollHeight')
            print(f"Old Height: {old_height}, New Height: {new_height}")

            if new_height == old_height:
                print("Page height did not increase; stopping load more.")
                break
            old_height = new_height

        except Exception as e:
            print("Error in Load More loop:", e)
            break

    # 5. Save the final HTML to a file
    html = driver.page_source
    with open('laptop.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("HTML saved to 'laptop.html'.")

    # 6. Close the browser
    time.sleep(2)
    driver.quit()


if __name__ == "__main__":
    main()
