import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    # Connect to Proton VPN
    # print("Connecting to Proton VPN")
    # _, error = connect_to_vpn()
    # if error:
    #     exit(1)

    # Get movies
    driver = webdriver.Firefox()
    driver.get("https://watchsomuch.to/")

    try:
        close_button_xpath = '//*[@id="UpgradePlans"]/div/div[1]/button[1]'
        close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, close_button_xpath))
        )
        close_button.click()
    except:
        driver.quit()

    search = driver.find_element(By.NAME, "Search")
    search.send_keys("The Mandalorian")
    search.send_keys(Keys.RETURN)

    try:
        movie = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "MediumMovie"))
        )

        content = driver.find_element(By.ID, "Content")

        movies = content.find_elements(By.CLASS_NAME, "MediumMovie")
        for movie in movies:
            title = movie.find_element(By.CLASS_NAME, "title")

            # TODO - Add logic to select the correct movie from user input
            if title.text == "Disney Gallery: Star Wars: The Mandalorian (Documentary-2023)":
                movie_middle = movie.find_element(By.CLASS_NAME, "middle")
                movie_middle.click()
                break
            print(title.text)

    except Exception as e:
        print(e)

def connect_to_vpn():
    # Connect to Proton VPN
    command = ["protonvpn-cli", "c", "-f"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)

    output, error = process.communicate()
    if error:
        print(error.decode("utf-8"))
        return error
    print(output.decode("utf-8"))

    return output, error

if __name__ == "__main__":
    main()

