from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import speech_recognition as sr
from pydub import AudioSegment
import io


def solve_recaptcha(url, headless=True):
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

    if headless:
        chrome_options.add_argument("--headless")

    # Sesuaikan path chromedriver jika menggunakan Termux Android
    service = Service("/usr/bin/chromedriver")   
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # Beralih ke iframe reCAPTCHA
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src,'recaptcha')]")))
        driver.switch_to.frame(iframe)

        # Klik checkbox reCAPTCHA
        checkbox = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))
        checkbox.click()
        driver.switch_to.default_content()
        time.sleep(3)

        # Beralih ke iframe audio challenge
        audio_iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src,'bframe')]")))
        driver.switch_to.frame(audio_iframe)

        # Klik tombol audio challenge
        audio_button = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-audio-button")))
        audio_button.click()
        time.sleep(2)

        # Ambil link audio
        audio_link = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rc-audiochallenge-tdownload-link"))).get_attribute("href")
        response = requests.get(audio_link)
        audio_content = response.content

        # Konversi audio ke format WAV
        audio_bytes = io.BytesIO(audio_content)
        audio = AudioSegment.from_mp3(audio_bytes)
        audio = audio.set_frame_rate(16000).set_channels(1)
        wav_bytes = io.BytesIO()
        audio.export(wav_bytes, format="wav")
        wav_bytes.seek(0)

        # Proses audio dengan speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_bytes) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        # Input hasil audio ke form reCAPTCHA
        response_input = wait.until(EC.presence_of_element_located((By.ID, "audio-response")))
        response_input.send_keys(text)
        verify_button = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-verify-button")))
        verify_button.click()

        # Ambil token reCAPTCHA
        driver.switch_to.default_content()
        token = driver.execute_script("return document.querySelector('[name=\"g-recaptcha-response\"]').value;")
        return token

    except Exception as e:
        with open("error_page.html", "w") as f:
            f.write(driver.page_source)
        return f"Error: {str(e)}"

    finally:
        driver.quit()
      
