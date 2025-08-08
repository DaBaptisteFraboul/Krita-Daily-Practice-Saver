import os
import  re

from pathlib import Path
from datetime import datetime, date
import calendar

ROOT = r"D:\_ART\{current_year}\practice\{month}"
FILENAME = r"{iso_date}__practice__w{file_number}.kra"
FILE_NUMBER_PATTERN = r"__w(?P<number>\d{3}).kra"


def format_current_isodate(today:date) -> str:
    return today.isoformat().replace("-", "_")


def get_latest_available_number(practice_directory:str)-> int:
    if not os.path.exists(practice_directory):
        return 1
    else :
        sorting = [1]
        for filename in os.listdir(practice_directory):
            number_match = re.search(
                pattern=FILE_NUMBER_PATTERN,
                string=filename
            ) 
            if number_match : 
                sorting.append(int(number_match.group("number")))
               
        return max(sorting) + 1

          
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
    a = generate_available_filepath()
    print(a)