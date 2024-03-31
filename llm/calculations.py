def calculate_bmr(weight_lbs, height_cm, age, sex):
    weight_kg = weight_lbs * 0.454

    if sex == "male":
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    return bmr


def calculate_daily_calories(bmr, body_goal):
    # Assume a fixed activity level for moderate exercise
    activity_level = 1.0  # This corresponds to moderate exercise/activity
    print("Your body goal is: ", body_goal)

    if body_goal == "Trim Excess Fat":
        print("Trim excesdfs ")
        calorie_factor = 0.8
    elif body_goal == "Build Lean Mass":
        print("elena muscle mass")
        calorie_factor = 1.2
    elif body_goal == "Increase Strength":
        print("Incr stre")
        calorie_factor = 1.1
    elif body_goal == "Improve Endurance":
        print("Endureacn")
        calorie_factor = 1.0
    else:  # "boost overall fitness"
        print("Else !!!")
        calorie_factor = 1.0

    daily_calories = bmr * activity_level * calorie_factor
    return daily_calories


def calculate_daily_macros(daily_calories, body_goal):
    if body_goal == "Trim Excess Fat":
        print("Trim excesdfs ")
        protein_percentage = 0.35
        carbs_percentage = 0.4
        fats_percentage = 0.25
    elif body_goal == "Build Lean Mass":
        print("lean musc")
        protein_percentage = 0.3
        carbs_percentage = 0.5
        fats_percentage = 0.2
    elif body_goal == "Increase Strength":
        print("INC STR")
        protein_percentage = 0.35
        carbs_percentage = 0.45
        fats_percentage = 0.2
    elif body_goal == "Improve Endurance":
        print("IMPR END")
        protein_percentage = 0.2
        carbs_percentage = 0.6
        fats_percentage = 0.2
    else:  # "boost overall fitness"
        print("ELSE sc")
        protein_percentage = 0.25
        carbs_percentage = 0.5
        fats_percentage = 0.25

    daily_protein_grams = (daily_calories * protein_percentage) / 4
    daily_carbs_grams = (daily_calories * carbs_percentage) / 4
    daily_fats_grams = (daily_calories * fats_percentage) / 9

    return daily_protein_grams, daily_carbs_grams, daily_fats_grams


def calculate_daily_recommendations(session):
    current_weight_lbs = float(session.get("current_weight"))
    height_cm = float(session.get("height"))
    age = int(session.get("age"))
    sex = session.get("sex")
    body_goal = session.get("body_goal")

    # Calculate BMR
    bmr = calculate_bmr(current_weight_lbs, height_cm, age, sex)
    print("------------------- BMR is", bmr)

    # Calculate daily calorie intake
    daily_calories = calculate_daily_calories(bmr, body_goal)

    # Calculate daily macronutrient requirements in grams
    daily_protein_grams, daily_carbs_grams, daily_fats_grams = calculate_daily_macros(
        daily_calories, body_goal
    )

    # Store the calculated values in session variables
    session["daily_calories"] = round(daily_calories)
    session["daily_protein_grams"] = round(daily_protein_grams)
    session["daily_carbs_grams"] = round(daily_carbs_grams)
    session["daily_fats_grams"] = round(daily_fats_grams)
