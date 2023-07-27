import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MOVIE_DIR = "/home/nsengupta5/Videos/Movies/"
SUBTITLE_DIR = "/home/nsengupta5/Videos/Movies/subtitles/"

def main():
    # connect_to_vpn()
    driver = get_driver()
    driver.get("https://watchsomuch.to/")
    close_popup(driver)
    movie = search_movie(driver)

    try:
        movies = get_movie_list(driver)
        movie_choice = get_movie_choice(movies)
        choose_movie(movies, movie_choice)

        try:
            download_options = get_download_list(driver)
            download_choice = get_download_choice(download_options)
            movie_title = choose_download(download_options, download_choice)
            download_movie(driver.current_url, movie_title)

        except Exception as e:
            print(f"Download Parent Error: {e}")

    except Exception as e:
        print(f"Other Error: {e}")

    # disconnect_from_vpn()
    driver.get("https://subscene.com/")
    search_sub(driver, movie)
    print("Done")

def connect_to_vpn():
    print("Connecting to Proton VPN...")
    command = ["protonvpn-cli", "c", "-f"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)

    output, error = process.communicate()
    if error:
        print(error.decode("utf-8"))
        exit(1)
    print(output.decode("utf-8"))

def disconnect_from_vpn():
    print("Disconnecting from Proton VPN...")
    command = ["protonvpn-cli", "d"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)

    output, error = process.communicate()
    if error:
        print(error.decode("utf-8"))
        exit(1)
    print(output.decode("utf-8"))

def get_movie_id(url):
    # Get movie id from url
    download_part = url.split("/")[-2]
    return download_part.split("-")[-1]

def get_url_safe_title(title):
    # Get url safe title
    title_arr = title.split(" ")
    if "-" in title_arr:
        title_arr.remove("-")

    cleaned_words = []

    for word in title_arr:
        cleaned_word = word.replace("(", "").replace(")", "").replace(":", "")
        cleaned_words.append(cleaned_word)
    return ".".join(cleaned_words[:-1])

def download_movie(url, title):
    print("Downloading movie...")

    # Get movie url
    movie_id = get_movie_id(url)
    url_safe_title = get_url_safe_title(title)

    download_link = "https://media.watchsomuch.com/Torrents/" + url_safe_title + "." + movie_id + ".WatchSoMiuch.torrent"

    print (f"Download Link: {download_link}")

    # Download movie
    command = ["curl", download_link, "-o", MOVIE_DIR + title + ".torrent"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)

    output, error = process.communicate()
    if error:
        print(error.decode("utf-8"))
        exit(1)
    print(output.decode("utf-8"))

def get_driver():
    print("Getting driver...")
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    return webdriver.Firefox(options=options)

def close_popup(driver):
    print("Closing popup...")
    try:
        close_button_xpath = '//*[@id="UpgradePlans"]/div/div[1]/button[1]'
        close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, close_button_xpath))
        )
        close_button.click()
    except:
        driver.quit()

def search_movie(driver):
    title = input("Enter movie title: ")
    print(f"Searching for {title}...")
    search = driver.find_element(By.NAME, "Search")
    search.send_keys(title)
    search.send_keys(Keys.RETURN)

def get_movie_list(driver):
    print("Getting movie list...")
    WebDriverWait(driver, 40).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "MediumMovie"))
    )

    content = driver.find_element(By.ID, "Content")
    return content.find_elements(By.CLASS_NAME, "MediumMovie")

def get_movie_choice(movie_list):
    print("Getting movie choice...\n")

    for i, movie in enumerate(movie_list):
        title = movie.find_element(By.CLASS_NAME, "title")
        print(f"({i + 1}) {title.text}")

    print()
    movie_choice = input("Enter movie number: ")
    return movie_list[int(movie_choice) - 1].find_element(By.CLASS_NAME, "title").text

def choose_movie(movies, movie_choice):
    print(f"Choosing {movie_choice}...")
    for movie in movies:
        title = movie.find_element(By.CLASS_NAME, "title")
        if title.text == movie_choice:
            movie_middle = movie.find_element(By.CLASS_NAME, "middle")
            movie_middle.click()
            break

def get_download_list(driver):
    print("Getting download list...")
    download_button = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.ID, "btnDownload"))
    )
    download_button.click()

    download_parent = driver.find_element(By.ID, "downloadDropdown")
    return download_parent.find_elements(By.TAG_NAME, "a")

def get_download_choice(download_options):
    print("Getting download choice...\n")

    for i, option in enumerate(download_options):
        title = option.get_attribute("title")
        print(f"({i + 1}) {title}")

    print()
    download_choice = input("Enter download number: ")
    return download_options[int(download_choice) - 1].get_attribute("title")

def choose_download(download_options, download_choice):
    print(f"Choosing {download_choice}...")
    for option in download_options:
        title = option.get_attribute("title")
        if title == download_choice:
            option.click()
            break
    return download_choice

def search_sub(driver, movie_title):
    print("Searching for subtitles...")
    search = driver.find_element(By.ID, "query")
    search.send_keys(movie_title)
    search.send_keys(Keys.RETURN)

if __name__ == "__main__":
    main()
