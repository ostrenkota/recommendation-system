import pandas as pd
import math as math
import collections as collections


def sim(u, v):
    multiply = 0
    usquare = 0
    vsquare = 0
    for i in range(1, movie_names.shape[0] + 1):
        ui = int(data.iloc[u][i])
        vi = int(data.iloc[v][i])
        if ui == -1 or vi == -1:
            continue
        else:
            usquare += ui**2
            vsquare += vi**2
            multiply += vi * ui
    return multiply/(math.sqrt(usquare) * math.sqrt(vsquare))


def calculate_marks():
    marks = {}
    for i in range(marks_number):
        if i != variant:
            marks[i] = sim(i, variant)
    sorted_marks = sorted(marks.items(), key=lambda kv: kv[1], reverse=True)
    sorted_marks = sorted_marks[0:4]

    for i in range(len(sorted_marks)):
        average = calculate_average(sorted_marks[i][0])
        sorted_marks[i] = (sorted_marks[i][0], sorted_marks[i][1], average)
    variant_average = calculate_average(variant)

    expected_marks = {}
    for i in range(movies_number):
        if data.iloc[variant][i] == -1:
            expected_marks[i] = calculate_expected_mark(i, sorted_marks, variant_average)
    return expected_marks


def calculate_average(v):
    sum = 0
    number = 0
    for i in range(1, movies_number):
        if data.iloc[v][i] != "-1":
            sum += int(data.iloc[v][i])
            number += 1
    return sum/number


def calculate_expected_mark(film_index, similar_users_array, variant_average):
    numerator = 0
    norm = 0
    for v in range(len(similar_users_array)):
        if data.iloc[v][film_index] == "-1":
            continue
        numerator += similar_users_array[v][1] * (data.iloc[v][film_index] - similar_users_array[v][2])
        norm += similar_users_array[v][1]
    return variant_average + (numerator/norm)


if __name__ == '__main__':
    variant = 24
    context_day = pd.read_csv('context_day.csv')
    context_place = pd.read_csv('context_place.csv')
    data = pd.read_csv('data.csv')
    movie_names = pd.read_csv('movie_names.csv')
    marks_number = data.shape[0]
    movies_number = data.shape[1]
    a = calculate_marks()
    print(a)
    print(data.iloc[variant])