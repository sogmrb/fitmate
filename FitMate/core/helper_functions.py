import math

from django.utils import timezone
from datetime import timedelta


def calculate_daily_needed_calories(profile):
    weight = profile.weight
    goal_weight = profile.goal_weight
    height = profile.height
    age = profile.age
    sex = profile.sex
    gain_or_loss_goal = profile.weekly_weight_gain_or_loss_goal
    activity_level = profile.activity_level

    tdee_factors = {'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55, 'active': 1.725, 'very_active': 1.9}
    factor = tdee_factors[activity_level]

    if sex == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif sex == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 78  # average of both

    tdee = math.ceil(bmr * factor)

    if goal_weight < weight:
        weekly_deficit = gain_or_loss_goal * 7716
        daily_deficit = math.ceil(weekly_deficit / 7)
        print(tdee)
        print(daily_deficit)
        print(tdee - daily_deficit)
        daily_intake = max(1200, tdee - daily_deficit)
        number_of_days_until_goal = math.ceil((weight - goal_weight) / gain_or_loss_goal)
        print(daily_intake)
        return daily_intake, number_of_days_until_goal
    if goal_weight > weight:
        weekly_surplus = gain_or_loss_goal * 7716
        daily_surplus = math.ceil(weekly_surplus / 7)
        daily_intake = tdee + daily_surplus
        number_of_days_until_goal = math.ceil((goal_weight - weight) / gain_or_loss_goal)
        print(daily_intake)
        return daily_intake, number_of_days_until_goal
    else:
        return tdee, 0


def total_daily_stats(user_entries):
    total_daily_calories = 0
    total_daily_carbs = 0
    total_daily_proteins = 0.0
    total_daily_fats = 0.0
    total_daily_saturated_fat = 0.0
    total_daily_polyunsaturated_fat = 0.0
    total_daily_monounsaturated_fat = 0.0
    total_daily_cholesterol = 0.0
    total_daily_sodium = 0.0
    total_daily_potassium = 0.0
    total_daily_fibers = 0.0
    total_daily_sugar = 0.0
    total_daily_vitamin_a = 0.0
    total_daily_vitamin_c = 0.0
    total_daily_calcium = 0.0
    total_daily_iron = 0.0

    for entry in user_entries:
        total_daily_calories += int(entry.total_calories)
        total_daily_carbs += float(entry.total_carbs)
        total_daily_proteins += float(entry.total_proteins)
        total_daily_fats += float(entry.total_fats)
        total_daily_saturated_fat += float(entry.total_saturated_fat)
        total_daily_polyunsaturated_fat += float(entry.total_polyunsaturated_fat)
        total_daily_monounsaturated_fat += float(entry.total_monounsaturated_fat)
        total_daily_cholesterol += float(entry.total_cholesterol)
        total_daily_sodium += float(entry.total_sodium)
        total_daily_potassium += float(entry.total_potassium)
        total_daily_fibers += float(entry.total_fibers)
        total_daily_sugar += float(entry.total_sugar)
        total_daily_vitamin_a += float(entry.total_vitamin_a)
        total_daily_vitamin_c += float(entry.total_vitamin_c)
        total_daily_calcium += float(entry.total_calcium)
        total_daily_iron += float(entry.total_iron)

    stats = {'total_daily_calories': int(total_daily_calories),
             'total_daily_carbs': int(total_daily_carbs),
             'total_daily_proteins': int(total_daily_proteins),
             'total_daily_fats': int(total_daily_fats),
             'total_daily_saturated_fat': round(total_daily_saturated_fat, 3),
             'total_daily_polyunsaturated_fat': round(total_daily_polyunsaturated_fat, 3),
             'total_daily_monounsaturated_fat': round(total_daily_monounsaturated_fat, 3),
             'total_daily_cholesterol': round(total_daily_cholesterol, 3),
             'total_daily_sodium': round(total_daily_sodium, 3),
             'total_daily_potassium': round(total_daily_potassium, 3),
             'total_daily_fibers': round(total_daily_fibers, 3),
             'total_daily_sugar': round(total_daily_sugar, 3),
             'total_daily_vitamin_a': round(total_daily_vitamin_a, 3),
             'total_daily_vitamin_c': round(total_daily_vitamin_c, 3),
             'total_daily_calcium': round(total_daily_calcium, 3),
             'total_daily_iron': round(total_daily_iron, 3)}

    return stats


def carb_fat_protein_ratio(total_calories, goal, activity_level):
    if goal == 'weight_loss' and activity_level == 'sedentary':
        protein_ratio = 0.3
        fat_ratio = 0.3
        carb_ratio = 0.4

    elif goal == 'muscle_gain':
        protein_ratio = 0.4
        fat_ratio = 0.3
        carb_ratio = 0.3

    else:
        protein_ratio = 0.3
        fat_ratio = 0.25
        carb_ratio = 0.45

    calories_from_carbs = total_calories * carb_ratio
    calories_from_proteins = total_calories * protein_ratio
    calories_from_fat = total_calories * fat_ratio

    carbs_in_gram = round(calories_from_carbs / 4)
    protein_in_gram = round(calories_from_proteins / 4)
    fat_in_gram = round(calories_from_fat / 9)

    return carbs_in_gram, protein_in_gram, fat_in_gram


def streak_days(user_entries):
    if not user_entries:
        return 0
    current_day = timezone.now().date()
    if user_entries[0].date != current_day:
        return 0
    streak_days = 1
    prev_date = current_day - timedelta(days=1)
    for i in range(1, len(user_entries)):
        if user_entries[i].date == current_day:
            continue
        elif user_entries[i].date == prev_date:
            streak_days += 1
            current_day = prev_date
            prev_date = current_day - timedelta(days=1)
        else:
            break
    return streak_days
