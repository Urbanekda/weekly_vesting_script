from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from PIL import Image
import io
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.firefox.options import Options

app = Flask(__name__)
CORS(app) 

options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)


data = []

honorable_mentions = []

def get_vesting_screenshot():
    try:
        vesting_chart = driver.find_element(By.CSS_SELECTOR, ".recharts-responsive-container")
    except Exception as e:
        print(f"An error has occure: {e}")
        
    location = vesting_chart.location
    size = vesting_chart.size
    screenshot = driver.get_screenshot_as_png()
    print("Getting Screenshot")
    image = Image.open(io.BytesIO(screenshot))
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    cropped_image = image.crop((left, top, right, bottom))
    print("Cropping image")
    cropped_image.save("vesting_chart.png")

def scrape_table(url):
    print(f"Initializing session: {url}")
    driver.get(url)
    print("Loading page content...")
    vestingGroups = []
    
    while not vestingGroups:
        time.sleep(2)
        try:
            table = driver.find_element(By.CSS_SELECTOR, "div.css-14hw9e8:nth-child(2)")
            table_container = driver.find_element(By.CSS_SELECTOR, "div.css-14hw9e8:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)")
            
            try:
                ticker = driver.find_element(By.CSS_SELECTOR, ".css-g65rr5")
                ticker_text = ticker.text
                if not ticker_text:
                    ticker_text = "xxx"
            except NoSuchElementException:
                ticker_text = "xxx"

            project_name = driver.find_element(By.CSS_SELECTOR, ".css-1vy8s6x")
            driver.execute_script("arguments[0].scrollIntoView(true);", table_container)
            
            print("Searching page...")
            driver.implicitly_wait(5)
        
            get_vesting_screenshot

            print("loading")
            rows = table.find_elements(By.CLASS_NAME, "tr")

            if rows:
                first_row = rows[2]
                first_row_cells = first_row.find_elements(By.CLASS_NAME, "td")
                first_unlock_date = first_row_cells[0].text.split("\n")[0].strip()
                
                for row in rows:
                    cells = row.find_elements(By.CLASS_NAME, "td")
                    print(f"Found {len(cells)} cells")
                    print(f"Processing row {row.id}")
                
                    if cells:
                        
                        unlock_date = cells[0].text.split("\n")[0].strip()
                        if unlock_date == first_unlock_date:
                            row_data = {
                                    "unlockDate": cells[0].text.split("\n")[0].strip(),
                                    "allocationGroup": cells[1].text.strip(),
                                    "amount": cells[2].text.split("\n")[0].strip(),
                                    "supplyIncrease": cells[3].text.strip(),
                                    "targetWallet": cells[4].text.strip(),
                                    "valuation": cells[2].text.split("\n")[1].strip(),
                                    "ticker": f"${ticker_text.strip()}",
                                    "name": f"{project_name.text.strip()}",
                                    "link": url
                                }

                            vestingGroups.append(row_data)
        except Exception as e:
            print(f"Error occurred: {e}")

    print("Finished browsing")
    
    return vestingGroups

linkList = ["https://coinbrain.com/coins/bnb-0xd06716e1ff2e492cc5034c2e81805562dd3b45fa",
"https://coinbrain.com/coins/bnb-0x73fbd93bfda83b111ddc092aa3a4ca77fd30d380",
"https://coinbrain.com/coins/eth-0x2dff88a56767223a5529ea5960da7a3f5f766406",
"https://coinbrain.com/coins/eth-0xf091867ec603a6628ed83d274e835539d82e9cc8",
"https://coinbrain.com/coins/eth-0x013062189dc3dcc99e9cee714c513033b8d99e3c"]

#print("Enter cb links one by one, press enter. Type 'done' to proceed with extraction.")
    
#while True:
 #   cbLink = input("Enter Ethereum Address:")
  #  if cbLink == "done":
   #     break
    #linkList.append(cbLink)

#for link in linkList:
 #   data.append(scrape_table(link))
#driver.quit


@app.route('/api/scrape/main', methods=['GET'])
def get_vesting_data():
    for link in linkList:
       data.append(scrape_table(link))
    driver.quit
    return jsonify(data)

@app.route('/api/test', methods=['GET'])
def get_test_data():
    global data
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)