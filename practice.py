from datetime import * 

## want to create streak counter so that if a user did a meditation yesterday and then logs another today, streak will increase by 1 - if a user skips a day, streak will return to 1 

user = User.query.get(user_id)
streak_count = 1

yesterday = {}
today = {}

for meditation in user3.meditations:
    if meditation.date.date() == date.today():
        if meditation.date.date() not in today:
            today['today'] = meditation.date.date()
    if meditation.date.date() == date.today() - timedelta(days = 1):
        if meditation.date.date() not in yesterday:
            yesterday['yesterday'] = meditation.date.date()
        if today['today'] > yesterday['yesterday']:
            streak_count += 1
    else:
        streak_count = 1

for meditation in user9.meditations:
    if meditation.date.date() == date.today():
        if meditation.date.date() == date.today() - timedelta(days = 1):
            streak_count += 1
        else:
            streak_count = 1


