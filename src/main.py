import json as json
from src import config
from src import firsttask
from src import secondtask


if __name__ == '__main__':
    calculated_marks = firsttask.calculate_marks()
    expected_place = secondtask.calculate_expected_data("place")
    expected_day = secondtask.calculate_expected_data("day")

    res = {
        "user": config.variant,
        "1": {

        }
    }

    recommend = {}
    marks = {}
    for i in expected_place:
        if expected_place[i] == "h" and (expected_day[i] == "Sun" or expected_day[i] == "Sat"):
            key = "movie " + str(i)
            recommend[key] = calculated_marks[i]
        key = "movie " + str(i)
        marks[key] = calculated_marks[i]
    result = {"user": config.variant + 1, "1": marks, "2": recommend}
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)