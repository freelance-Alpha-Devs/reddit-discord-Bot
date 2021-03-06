import requests
import time
import scraperV2
import multiprocessing

def checkServer(waitTime = 0):
    try:
        r = requests.get("http://serverv3.hopto.org", timeout = 1)
        return True
    except requests.Timeout:
        return False
    except Exception as error:
        print("There was an error. Please restart the program.")
        time.sleep(waitTime)
        checkServer((waitTime + 1) * 2)

scraperThread = multiprocessing.Process(target=scraperV2.main)

def isTrue():
    state = checkServer()
    if not state:
        print("Starting thread... Done.")
        scraperThread.start()
    else:
        file = requests.get("http://serverv3.hopto.org:6969/files/seen.txt")
        print("Connection found!")
        open("seen.txt", "wb").write(file.content)
        if scraperThread.is_alive():
            print("Terminating thread... Done.")
            scraperThread.terminate()

if __name__ == "__main__":
    print("Program started. Waiting for response...")
    while True:
        isTrue()
        time.sleep(1800)