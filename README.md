# openim-e2eTest
This repository contains the end-to-end (e2e) automation tests for the OpenIM project. Below you'll find the steps to run the entire test suite or individual test cases, as well as the setup required for running tests in environments without a graphical user interface, such as a Git testing environment, by using a headless browser.

## Running Tests

### Run the Entire Test Suite
To run all test cases in the suite:
1. Open your Git testing environment.
2. Execute the following command:
   ```
   pytest main.py
   ```

### Run a Single Test Case
To run an individual test case:
1. Open your Git testing environment.
2. Execute the command below, replacing `test_single_test_file` with the name of your test file:
   ```
   pytest script/test_single_test_file
   ```

## Setting Up a Headless Browser
In environments without a graphical user interface, like Git's testing environment, it's possible to run the entire test project using a headless browser. Here's how to set it up:

### Configuring the Environment
#### 1. Install Google Chrome
   - Update your package list:
     ```
     sudo apt-get update
     ```
   - Install Google Chrome Stable:
     ```
     sudo apt-get install -y google-chrome-stable
     ```
   - If you encounter the error "Unable to locate package google-chrome-stable":
     a. Download and add the official Google Chrome public key:
        ```
        wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
        ```
     b. Add the Google Chrome repository to your software sources list:
        ```
        echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
        ```
     c. Update the package list and install Google Chrome:
        ```
        sudo apt-get update
        sudo apt-get install -y google-chrome-stable
        ```

#### 2. Install ChromeDriver
   - Ensure the ChromeDriver version matches the installed Chrome version.
   - Download ChromeDriver:
     ```bash
     wget https://storage.googleapis.com/chrome-for-testing-public/version/linux64/chromedriver-linux64.zip
     ```
   - Extract and move ChromeDriver to `$HOME/bin` (Create the directory if it doesn't exist):
     ```bash
     mkdir -p $HOME/bin
     unzip chromedriver-linux64.zip -d $HOME/bin
     mv $HOME/bin/chromedriver-linux64/chromedriver $HOME/bin
     ```
   - Make ChromeDriver executable:
     ```bash
     chmod +x $HOME/bin/chromedriver
     ```
   - Verify that ChromeDriver is executable:
     ```bash
     $HOME/bin/chromedriver --version
     ```

#### 3. Configure the Environment Variable
   - Add ChromeDriver to your PATH:
     ```
     export PATH="$HOME/bin:$PATH"
     ```
   - Make the environment variable changes take effect:
     ```
     source ~/.bashrc
     ```

#### 4. Verify Installation
   - Check ChromeDriver version to ensure it's correctly installed:
     ```
     chromedriver --version
     ```

#### 5. Install selenium

   - pip install selenium is required：
     ```
     pip install selenium
     ```

#### 4. Install OpenIM Server Test

Clone openim-server, use docker install:
```bash
git clone https://github.com/openimsdk/openim-docker
cd openim-docker
```

init config:
```
make init
```

start docker:
```
docker compose up -d
```

start test-e2e:
```
cd ..
cd test-e2e
pytest main.py
```

### Using the Headless Browser in Code
When initiating the `driver()` function in your code, include the following options to enable headless mode and avoid common issues:

```python
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import os

chrome_options = Options()
chrome_options.add_argument("--headless")  # Enable headless mode
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--enable-logging")
chrome_options.add_argument("--v=1")
chrome_options.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues

# Optional: Specify the path to chromedriver if not in PATH
driver_path = os.path.join(os.environ['HOME'], 'bin', 'chromedriver')  
service = Service(executable_path=driver_path)
# Instantiate WebDriver with Service object and options
driver = webdriver.Chrome(service=service, options=chrome_options)
```

This setup ensures your e2e tests can run in environments lacking a GUI, using Selenium WebDriver with Chrome in headless mode.
