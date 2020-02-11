import requests
from bs4 import BeautifulSoup
import json


# nepali calendar data scrap using python  @V.1
# @itsbohara

# @model -> calendar day
class cDay:
    def __init__(self, enDate, npDate, event, tithi):
        self.enDate = enDate
        self.npDate = npDate
        self.event = event
        self.tithi = tithi


# @model -> calendar day - event
class Event:
    def __init__(self, title, npDay, enDay, holiday):
        self.title = title
        self.npDay = npDay
        self.enDay = enDay
        self.holiday = holiday


def obj_to_dict(obj):
    return obj.__dict__


calendarData = []
print('starting ...')
# @url -> using hamro patro
page = requests.get('https://www.hamropatro.com/calendar/2076/12')
npCalendar = BeautifulSoup(page.content, 'html.parser')

print('getting year and month name')
# split year and month from title
npcData = npCalendar.find('title')
# Nepali Calendar 2076 Baishakh | २०७६ वैशाख  | Hamro Nepali Patro
npcData = npcData.get_text().split("|")
year = npcData[0][16:20]
month = npcData[0][21:-1]

print('getting data for year => ' + year + ' ; month => ' + month)
npCalendarDates = npCalendar.find(class_='dates')
dates = npCalendarDates.findAll('li')

# main scrap loop;
for date in dates:
    if not (date['class']) or date['class'][0] != 'disable':
        npDate = date.findAll('span')
        encDate = date['id']
        npcDate = npDate[0]['id'][:-4]
        tithi = npDate[3].get_text()
        eventTitle = npDate[1].get_text()
        eventNpDay = npDate[2].get_text()
        eventEnDay = npDate[5].get_text()
        holiday = 'false'
        if date['class']:
            if date['class'][0] == 'holiday':
                holiday = 'true'

        npEvent = Event(eventTitle, eventNpDay, eventEnDay, holiday)
        eDay = cDay(encDate, npcDate, npEvent, tithi)
        # eDayData = json.dumps(eDay.__dict__)
        calendarData.append(eDay)

print('converting data to json')
# save data to file -> year-month.json
file_path = year + "-" + month + ".json"
f = open('data/' + file_path, "w")
finalMonthData = {
    "month": month,
    "data": calendarData
}
print('saving to file => ' + file_path)
f.write(json.dumps(finalMonthData, default=obj_to_dict))
f.close()
