from bs4 import BeautifulSoup
import requests
import csv
import schedule
import time

# a function that retrieves number of people at NUS's UTown gym and writes into csv
def get_pax():
    url = "https://reboks.nus.edu.sg/nus_public_web/public/index.php/facilities/capacity"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    date_time = doc.find(id="lastUpdate").get_text()
    words = date_time.split()
    date = words[-2]
    time = words[-1]

    current_hour = int(time[:2])
    # opens 7am (07) to 10pm (22)
    if current_hour not in range(7, 22):
        print("Gym is closed.")
        return
    
    utown_gym = doc.find_all(class_ = "gymbox")[-1]
    utown_pax = utown_gym.find("b")
    slash_index = utown_pax.string.index("/")
    utown_people = utown_pax.string[:slash_index]
    new = [date, time, utown_people]
    print(new)

    # header of csv
    header = ['Date', 'Time', 'Pax']
    with open('gym_pax.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        file.seek(0, 2) # move file pointer to end of file
        if not file.tell(): #check file position. if empty, write the header
            writer.writerow(header)
        writer.writerow(new)
    return new

# execute function every 3 minutes
schedule.every(3).minutes.do(get_pax)

while True:
    schedule.run_pending()
    time.sleep(1)