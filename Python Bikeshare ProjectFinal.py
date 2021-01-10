import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
citynames = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all', 'none']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) username - name of the person exploring bikeshare data
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    username = input("Hi There! What is your name? \n")
    print('Hello ', username,'! Let\'s explore some US bikeshare data!', sep='')


    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = str(input("Would you like to see data for Chicago, New York City or Washington?\n"))
        city = city.lower()
        if city not in citynames:
            print("Sorry", username, "I didn\'t recognise that. Please choose from Chicago, New York City or Washington.\n")
            continue
        else:
            print("Thanks", username, "we\'ll look at", city.title())
            break


    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("Which month would you like to filter by? You can also choose all.\n"))
        month = month.lower()
        if month not in months:
            print("Sorry", username, "I didn\'t recognise that. Please choose a month or all. \n")
            continue
        else:
            print("Thanks", username, "we\'ll look at", month.title())
            break


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input("Which day would you like to filter by? You can choose Monday, Tuesday etc, or all. \n"))
        day = day.lower()
        if day not in days:
            print("Sorry", username, "I didn\'t recognise that. Please choose a day. You can chose from Monday, Tuesday etc.\n")
            continue
        else:
            print("Thanks", username, "we\'ll filter by", day.title())
            break
    print("The city you have chosen is:", city)
    print("The month you have chosen is:", month)
    print("The day you have chosen is:", day)
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print("The most common month is:", common_month)

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("The most common day is:", common_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common hour is:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    station_start = df['Start Station'].value_counts().idxmax()
    print("The most common start station is:", station_start)

    # TO DO: display most commonly used end station
    station_end = df['End Station'].value_counts().idxmax()
    print("The most common end station is:", station_end)

    # TO DO: display most frequent combination of start station and end station trip
    df['Combination'] = df['Start Station'] + df['End Station']
    station_combination = df['Combination'].mode()[0]
    print("The most common combination of start and end station is:", station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    Total_Time = sum(df['Trip Duration'])
    total_time_hours = Total_Time/3600
    total_time_days = Total_Time/86400
    print("The total travel time is:", Total_Time, "seconds")
    print(f"This is {total_time_hours:.4f} hours or {total_time_days:.4f} days, rounded to 4 decimal places.")

    # TO DO: display mean travel time
    Mean_Time = df['Trip Duration'].mean()
    mean_time_minutes = Mean_Time/60
    print("The mean average travel time is:", Mean_Time, "seconds")
    print(f"This is {mean_time_minutes:.4f} minutes, rounded to 4 decimal places.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print("The user types are:\n", user_type_count)

    # TO DO: Display counts of gender
    try:
        gender_type_count = df['Gender'].value_counts()
        print('Gender Types:\n', gender_type_count)
    except KeyError:
        print("Sorry, there is no gender information for the selected filter.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        print('The earliest year of birth recorded is:', earliest_year)
    except KeyError:
        print("Sorry, there is no year of birth information for the selected filter.")

    try:
        recent_year = df['Birth Year'].max()
        print('The latest year of birth recorded is:', recent_year)
    except KeyError:
        print("Sorry, there is no year of birth information for the selected filter.")

    try:
        common_year = df['Birth Year'].value_counts().idxmax()
        print('The most common year recorded is:', common_year)
    except KeyError:
        print("Sorry, there is no year of birth information for the selected filter.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Asking the user if they would like to see the raw data.
    provides raw data to user 5 lines at a time"""

    raw_data_count = 0
    while True:
        answer = input("Would you like to see the raw data? Please type Yes or No: ").lower()
        if answer not in ['yes', 'no']:
            answer = input("Sorry, I didn\'t recognise that. Please type Yes or No: ")
        elif answer == 'yes':
            print(df.iloc[raw_data_count : raw_data_count + 5])
            raw_data_count += 5
            next_answer = input("Do you want to see more? Yes or No: ").lower()
            if next_answer == 'no':
                break
        elif answer == 'no':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        #
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
