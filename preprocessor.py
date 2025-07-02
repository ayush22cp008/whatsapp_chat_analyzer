import re
import pandas as pd

def preproces(data):
    # Correct timestamp pattern: matches full "MM/DD/YY, HH:MM AM/PM - "
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*[APMapm]{2}\s*-\s*'

    # Split & extract
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Clean trailing " - "
    dates = [re.sub(r'\s*-\s*$', '', d.strip()) for d in dates]

    # ✅ Fix narrow non-breaking space in AM/PM if needed
    # (Sometimes WhatsApp uses U+202F narrow space)
    dates = [d.replace('\u202f', ' ').strip() for d in dates]

    # Build DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # ✅ Use US format (month/day/year)
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p')

    # Rename
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df