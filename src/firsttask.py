import pandas as pd
import math as math
from src import config


data = pd.read_csv('resources/data.csv')
marks_number = data.shape[0]
movies_number = data.shape[1]


def sim(u, v):
    multiply = 0
    usquare = 0
    vsquare = 0
    for i in range(1, data.shape[1]):
        ui = int(data.iloc[u][i])
        vi = int(data.iloc[v][i])
        if ui == config.minusOneInt or vi == config.minusOneInt:
            continue
        else:
            usquare += ui ** 2
            vsquare += vi ** 2
            multiply += vi * ui
    return multiply / (math.sqrt(usquare) * math.sqrt(vsquare))


def calculate_marks():
    marks = {}
    for i in range(marks_number):
        if i != config.variant:
            marks[i] = sim(i, config.variant)
    sorted_marks = sorted(marks.items(), key=lambda kv: kv[1], reverse=True)
    sorted_marks = sorted_marks[0:4]

    for i in range(len(sorted_marks)):
        average = calculate_average(sorted_marks[i][0])
        sorted_marks[i] = (sorted_marks[i][0], sorted_marks[i][1], average)
    variant_average = calculate_average(config.variant)

    expected_marks = {}
    for i in range(1, movies_number):
        if data.iloc[config.variant][i] == config.minusOneInt:
            expected_marks[i] = calculate_expected_mark(i, sorted_marks, variant_average)
    return expected_marks


def calculate_average(v):
    sum = 0
    number = 0
    for i in range(1, data.shape[1]):
        if data.iloc[v][i] != config.minusOneInt:
            sum += int(data.iloc[v][i])
            number += 1
    return round(sum / number, 3)


def calculate_expected_mark(film_index, similar_users_array, variant_average):
    numerator = 0
    norm = 0
    for v in range(len(similar_users_array)):
        user = similar_users_array[v][0]
        if data.iloc[user][film_index] == config.minusOneInt:
            continue
        numerator += round(similar_users_array[v][1] * (data.iloc[user][film_index] - similar_users_array[v][2]), 3)
        norm += round(similar_users_array[v][1], 3)
    return round(variant_average + (numerator / abs(norm)), 3)
