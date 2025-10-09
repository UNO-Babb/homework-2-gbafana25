#BusSchedule.py
#Name: Gareth Moodley
#Date: 10-7-2025
#Assignment: Bus Schedule

import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pytz


def loadURL(url):
  """
  This function loads a given URL and returns the text
  that is displayed on the site. It does not return the
  raw HTML code but only the code that is visible on the page.
  """
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--headless");
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  content=driver.find_element(By.XPATH, "/html/body").text
  driver.quit()

  return content

def loadTestPage():
  """
  This function returns the contents of our test page.
  This is done to avoid unnecessary calls to the site
  for our testing.
  """
  page = open("testPage.txt", 'r')
  contents = page.read()
  page.close()

  return contents

def getHours(timestr):
  t = timestr[:-2]
  hours = t.split(":")[0]
  day = timestr[-2:]
  if day == "AM":
    if hours == "12":
      return 0
    return int(hours)
  else:
    if hours == "12":
      return 12
    return int(hours)+12
  
def getMinutes(timestr):
  t = timestr[:-2]
  minutes = t.split(":")[1]
  return int(minutes)

def isLater(time1, time2):
  h1 = getHours(time1)
  h2 = getHours(time2)
  m1 = getMinutes(time1)
  m2 = getMinutes(time2)

  if h1 > h2:
    return True
  else:
    if h1 == h2 and m1 > m2:
      return True
    else:
      return False

def main():
  now = datetime.datetime.now()
  tz = pytz.timezone("America/Chicago")
  now_cst = tz.localize(now)
  now_str = now_cst.strftime("%I:%M%p")
  print("Current Time: "+now_str)
  stop_num = "2269"
  route_num = "11"
  direction = "EAST"
  url = "https://myride.ometro.com/Schedule?stopCode="+stop_num+"&routeNumber="+route_num+"&directionName="+direction
  #c1 = loadURL(url) #loads the web page
  c1 = loadTestPage() #loads the test page
  times = []
  for line in c1.split("\n"):
    if len(times) == 2:
      break
    if line[-2:] == "AM" or line[-2:] == "PM":
      if isLater(line, now_str):
        times.append(line)

  first_time_diff = 0
  if getHours(times[0]) == getHours(now_str) and getMinutes(times[0]) > getMinutes(now_str):
    first_time_diff = getMinutes(times[0])-getMinutes(now_str)
  elif getHours(times[0]) > getHours(now_str):
    first_time_diff = getMinutes(now_str)-getMinutes(times[0])
  print("The next bus will arrive in "+str(first_time_diff)+" minutes")
  print("The following bus will arrive in "+str(getMinutes(times[1])-getMinutes(now_str))+" minutes")


main()
