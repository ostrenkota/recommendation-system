from src import config
import pandas as pd

context_place = pd.read_csv('resources/context_place.csv')
context_day = pd.read_csv('resources/context_day.csv')


def calculate_sim(u, context):
    numerator = 0
    denominator = 0
    for i in range(1, context.shape[1]):
        if context.iloc[u][i] == context.iloc[config.variant][i] and \
                context.iloc[u][i] != " -1" and \
                context.iloc[config.variant][i] != " -1":
            numerator += 1
        elif context.iloc[u][i] != " -1" and context.iloc[config.variant][i] != " -1":
            denominator += 1
    return round(numerator / denominator, 3)


def calculate_expected_data(day_or_place):
    context = context_day
    if day_or_place == "place":
        context = context_place
    sims = {}
    for i in range(context.shape[0]):
        if i != config.variant:
            sims[i] = calculate_sim(i, context)
    sorted_sims = sorted(sims.items(), key=lambda kv: kv[1], reverse=True)
    sorted_sims = sorted_sims[0:12]

    expected_days = {}

    for i in range(1, context.shape[1]):
        if context.iloc[config.variant][i] == " -1":
            if day_or_place == "place":
                expected_days[i] = calculate_probability_for_places(i, sorted_sims, context)
            elif day_or_place == "day":
                expected_days[i] = calculate_probability_for_days(i, sorted_sims, context)
    return expected_days


def calculate_probability_for_days(film_number, sorted_sims, context):
    days_sim = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0}
    for i in range(len(sorted_sims)):
        key = context.iloc[sorted_sims[i][0]][film_number].strip()
        if key != '-1':
            days_sim[key] += sorted_sims[i][1]
    return max(iter(days_sim), key=lambda k: days_sim[k])


def calculate_probability_for_places(film_number, sorted_sims, context):
    places_sim = {"c": 0, "h": 0, "v": 0}
    for i in range(len(sorted_sims)):
        key = context.iloc[sorted_sims[i][0]][film_number].strip()
        if key != '-1':
            places_sim[key] += sorted_sims[i][1]
    return max(iter(places_sim), key=lambda k: places_sim[k])