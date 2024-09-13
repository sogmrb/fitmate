from meal.models import UserFoodEntry
from datetime import timedelta


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


def total_daily_burned(entries):
    burned = 0
    minutes = 0
    for entry in entries:
        burned += entry.burned_calories
        minutes += entry.duration

    return burned, minutes


def calculate_burned_calories(weight, MET_value, duration):
    return (duration * MET_value * weight) / 200


def streak_days(user, date):
    user_entries = UserFoodEntry.objects.filter(user=user, date__lte=date).order_by('-date')
    if not user_entries:
        return 0
    current_day = date
    if user_entries[0].date != current_day:
        return 0
    streakDays = 1
    prev_date = current_day - timedelta(days=1)
    for i in range(1, len(user_entries)):
        if user_entries[i].date == current_day:
            continue
        elif user_entries[i].date == prev_date:
            streakDays += 1
            current_day = prev_date
            prev_date = current_day - timedelta(days=1)
        else:
            break
    return streakDays
