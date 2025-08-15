import os
import  re

from pathlib import Path
from datetime import datetime, date
import calendar

ROOT = r"D:\_ART\{current_year}\practice\{month}"
FILENAME = r"{iso_date}__practice__w{file_number}.kra"
FILE_NUMBER_PATTERN = r"__w(?P<number>\d{3}).kra"
DATE_PATTERN = r"^(?P<iso_date>((?P<year>\d{4})_(?P<month>\d{2})_(?P<day>\d{2})))__practice__w(?P<number>\d{3})"


def format_current_isodate(today:date) -> str:
    return today.isoformat().replace("-", "_")

def get_get_practice_directory() -> str:
    today=date.today()
    practice_directory = Path(
        ROOT.format(
            current_year=today.year,
            month=calendar.month_name[today.month].lower()
        )
    ).as_posix()
    
    return practice_directory
    


def get_latest_available_number(practice_directory:str)-> int:
    today=date.today()
    if not os.path.exists(practice_directory):
        return 1
    else :
        sort_by_day = {} #files are sorted by month, get_only the day
        for filename in os.listdir(practice_directory):
            number_match = re.search(
                pattern=DATE_PATTERN,
                string=filename
            ) 
            if number_match :
                fileday = number_match.group("day")
                sort_by_day.setdefault(fileday, set())
                
                sort_by_day[fileday].add(int(number_match.group("number")))
        
        current_day = str(today.day)

        current_number= max(sort_by_day.get(current_day, [0])) 

        return current_number + 1

          
def generate_available_filepath(number_padding:int) -> str :
    today = date.today()
    practice_directory = Path(
        ROOT.format(
            current_year=today.year,
            month=calendar.month_name[today.month].lower()
        )
    ).as_posix()
    increment_number = get_latest_available_number(
        practice_directory=practice_directory
    )

    filepath = os.path.join(
        practice_directory,
        FILENAME.format(
            iso_date=format_current_isodate(today),
            file_number=str(increment_number).zfill(number_padding)
        )
    )
    return filepath

        
if __name__ == "__main__":
    today = date.today()
    practice_directory = Path(
        ROOT.format(
            current_year=today.year,
            month=calendar.month_name[today.month].lower()
        )
    ).as_posix()
    a = get_latest_available_number(practice_directory=practice_directory)
    print(a)