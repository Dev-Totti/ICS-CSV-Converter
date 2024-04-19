import sys
import csv
from icalendar import Calendar


def convertToCSV(icsFilePath, csvFilePath):
    with open(icsFilePath, "r", encoding="utf-8") as icsFile:
        calendar = Calendar.from_ical(icsFile.read())

        with open(csvFilePath, "w", newline="", encoding="utf-8") as csvFile:
            writer = csv.DictWriter(
                csvFile,
                fieldnames=[
                    "SUMMARY",
                    "DESCRIPTION",
                    "DTSTART",
                    "DTEND",
                    "RRULE",
                    "EXDATE",
                    "UID",
                ],
            )
            writer.writeheader()

            for component in calendar.walk():
                if component.name == "VEVENT":
                    writer.writerow(
                        {
                            "SUMMARY": component.get("SUMMARY"),
                            "DESCRIPTION": component.get("DESCRIPTION"),
                            "DTSTART": component.get("DTSTART").dt,
                            "DTEND": component.get("DTEND").dt,
                            "RRULE": (
                                component.get("RRULE").to_ical().decode("utf-8")
                                if component.get("RRULE")
                                else None
                            ),
                            "EXDATE": (
                                ",".join(
                                    [
                                        date.to_ical().decode("utf-8")
                                        for date in component.get("EXDATE")
                                    ]
                                )
                                if isinstance(component.get("EXDATE"), list)
                                else (
                                    component.get("EXDATE").to_ical().decode("utf-8")
                                    if component.get("EXDATE")
                                    else None
                                )
                            ),
                            "UID": component.get("UID"),
                        }
                    )


if len(sys.argv) != 2:
    icsFilePath = input("ICS | Path: ")
else:
    icsFilePath = sys.argv[1]

csvFilePath = icsFilePath.replace(".ics", ".csv")
convertToCSV(icsFilePath, csvFilePath)
