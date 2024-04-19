import sys
import csv
from icalendar import Calendar, Event, vRecur
from datetime import datetime


def convertToICS(csvFilePath, icsFilePath):
    cal = Calendar()
    with open(csvFilePath, "r", newline="", encoding="utf-8-sig") as csvFile:
        reader = csv.DictReader(csvFile)
        # next(reader)

        for row in reader:
            event = Event()

            event.add("summary", row["SUMMARY"])

            description = row["DESCRIPTION"]
            if description:
                event.add("description", row["DESCRIPTION"])
            dtstart = row["DTSTART"]

            if len(dtstart) == 10:
                dtstart = datetime.strptime(dtstart, "%Y-%m-%d").date()
            else:
                dtstart = datetime.strptime(dtstart, "%Y-%m-%d %H:%M:%S%z")
            event.add("dtstart", dtstart)

            if len(row["DTEND"]) == 10:
                event.add("dtend", datetime.strptime(row["DTEND"], "%Y-%m-%d").date())
            else:
                event.add(
                    "dtend", datetime.strptime(row["DTEND"], "%Y-%m-%d %H:%M:%S%z")
                )

            uid = row["UID"]
            if uid:
                event.add("uid", uid)

            if row["RRULE"]:
                event.add("rrule", vRecur.from_ical(row["RRULE"]))

            if row["EXDATE"]:
                for exdate in row["EXDATE"].split(","):
                    event.add("exdate", datetime.strptime(exdate, "%Y%m%dT%H%M%S"))

            cal.add_component(event)

        with open(icsFilePath, "wb") as icsFile:
            icsFile.write(cal.to_ical())


if len(sys.argv) != 2:
    csvFilePath = input("CSV | Path: ")
else:
    csvFilePath = sys.argv[1]

icsFilePath = csvFilePath.replace(".csv", ".ics")
convertToICS(csvFilePath, icsFilePath)
