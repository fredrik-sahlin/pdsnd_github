import time
import pandas as pd
import numpy as np

# dictionary for city_data
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Global lists containing filter values for months, days
MONTHS_FILTER = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAY_FILTER = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
months = ['january', 'february', 'march', 'april', 'may', 'june']

# Global output string variables
start_message = 'Most common '
count_message = 'Count:'

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
       city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()

       if city in CITY_DATA:
            break
       else:
            print('\nThe name of the city you entered does not exist. Please try again.')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWould you like to filter for any perticular month or get data for all months?\nType \"all\" for all months or the name of the perticular month of interest\n(january, february, march, april, may or june).\n').lower()

        if month in MONTHS_FILTER:
            break
        else:
            print('\nThe month you entered does not exist. Please try again.')


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nWould you like to filter for any perticular weekday or for all days?\nType \"all\" for all days or the name of the perticular day of interest\n(monday, tuesday, wednesday, thursday, friday, saturday or sunday).\n').lower()

        if day in DAY_FILTER:
            break
        else:
            print('\nThe day you entered does not exist. Please try again.')

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column do datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    if day != 'all':
        # filter by day of the week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def find_values(df, column):
    """
    Find the most common value in a dataframe column and its count

    Args:
        (DataFrame) df - the dataframe to analyze
        (str) column - name of the column to find value from
    Returns:
        df - Pandas DataFrame containing most common value in the column
        df - Pandas DataFrame containing the count of most common value in the column

    """
    return df[column].mode()[0], df[column].value_counts().tolist()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Column variables: month, day_of_week, hour
    month = 'month'
    day_of_week = 'day_of_week'
    hour = 'hour'

    # TO DO: display the most common month

    # get the most common month index and its count
    most_common_month_index, most_common_month_count = find_values(df, month)
    # find the most common months name
    most_common_month_name = months[most_common_month_index - 1]
    # print result
    print(start_message + month + ':', most_common_month_name.title() + ',',  count_message, most_common_month_count[0])


    # TO DO: display the most common day of week

    # get the most common day and its count
    most_common_day, most_common_day_count = find_values(df, day_of_week)
    # Print result
    print(start_message + day_of_week + ':', most_common_day.title() + ',', count_message, most_common_day_count[0])

    # TO DO: display the most common start hour

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most commmon start hour and its count
    most_common_start_hour, most_common_start_hour_count = find_values(df, hour)
    # print result
    print(start_message + hour + ':', str(most_common_start_hour) + ',', count_message, most_common_start_hour_count[0])

    # print the time of how long it took to calculate
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Column variables: start_station, end_station
    start_station = 'Start Station'
    end_station = 'End Station'
    trip = 'trip'

    # TO DO: display most commonly used start station

    # get the most common start station and its count
    most_common_start_station, most_common_start_station_count = find_values(df, start_station)
    # print result
    print(start_message + start_station + ':', most_common_start_station + ',', count_message, most_common_start_station_count[0])


    # TO DO: display most commonly used end station

    # get the most common end station and its count
    most_common_end_station, most_common_end_station_count = find_values(df, end_station)
    # print result
    print(start_message + end_station + ':', most_common_end_station + ',', count_message, most_common_end_station_count[0])


    # TO DO: display most frequent combination of start station and end station trip

    # group DataFrame and select largets frequency number and reset the index
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().nlargest(1).reset_index()

    # get column names
    column_start_station = most_common_trip.columns[0] # gets column name "Start Station"
    column_end_station = most_common_trip.columns[1] # gets column name "End Station"
    column_trip_count = most_common_trip.columns[2] # gets colmn name for frequency

    # get column values
    start_station_value = most_common_trip[column_start_station].values[0]
    end_station_value = most_common_trip[column_end_station].values[0]
    most_common_trip_count = most_common_trip[column_trip_count].values[0]

    # print result
    print(start_message + trip + ':\n',
          '\t\t' + start_station + ':', start_station_value + '\n',
          '\t\t' + end_station + ':', end_station_value + '\n',
          '\t\t' + count_message, most_common_trip_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    # Sum all seconds in "Trip Duration" column and convert id to Hours, minutes and seconds
    # Found the solution at https://www.geeksforgeeks.org/python-program-to-convert-seconds-into-hours-minutes-and-seconds/
    total_travel_time = time.strftime("%H:%M:%S", time.gmtime(df['Trip Duration'].sum()))

    # print result
    print('Total travel time in hours, minutes and seconds:', total_travel_time)

    # TO DO: display mean travel time

    # Calculate the mean of all seconds in "Trip Duration" column and convert id to Hours, minutes and seconds
    mean_travel_time = time.strftime("%H:%M:%S", time.gmtime(df['Trip Duration'].mean()))
    # print result
    print('Total average travel time in hours, minutes and seconds:', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def count_user_info(df, column, value):
    """
    Counts from the DataFrame the frequency of the value in a column

    Args:
        (DataFrame) df - the dataframe to analyze
        (str) column - name of the column to count value from
        (str) value - name of the value count
    Returns:
        df - Pandas DataFrame containing the count of the value in the column
    """
    return df[df[column] == value].count()

def find_max_min_values(df, column):
    """
    Finds the max and min value from a column in a DataFrame

    Args:
        (DataFrame) df - the dataframe to analyze
        (str) column - name of the column to find values from
    Returns:
        df(int) - Pandas DataFrame containing the max value
        df(int) - Pandas DataFrame containing the min value
    """
    return int(df[column].min()), int(df[column].max())

def user_stats(city, df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Column variables: user_type, gender, bith_year
    user_type = 'User Type'
    gender = 'Gender'
    birth_year = 'Birth Year'

    # TO DO: Display counts of user types


    # calculate amount of user types
    user_customer = count_user_info(df, user_type, 'Customer')
    user_subscriber = count_user_info(df, user_type, 'Subscriber')

    # print result
    print('Amount of ' + user_type + ':',
          '\nCustomer: ' + str(user_customer[0]),
          '\nSubscriber: ' + str(user_subscriber[0]) + '\n')


    # TO DO: Display counts of gender


    # check if city is Washington, if yes, do not calculate gender or birth date
    # this because data is missing from citys csv file
    if city != 'washington':
        # calculate amount of gender types
        male_gender = count_user_info(df, gender, 'Male')
        female_gender = count_user_info(df, gender, 'Female')
        # count NaN values for gender types
        gender_missing = df[gender].isnull().sum().sum()

        # print result
        print('Amount of ' + gender + ':',
              '\nMale: ' + str(male_gender[0]),
              '\nFemale: ' + str(female_gender[0]),
              '\nGender info missing: ' + str(gender_missing) + '\n')

        # TO DO: Display earliest, most recent, and most common year of birth

        # get the most recent and earliest birth year
        most_recent, earliest = find_max_min_values(df, birth_year)

        # get the most common birth year and its count
        most_common_birth_year, most_common_birth_year_count = find_values(df, birth_year)

        # print result
        print('Most recent ' + birth_year + ':', str(most_recent),
              '\nEearlist ' + birth_year + ':', str(earliest),
              '\n' + start_message + birth_year + ':', str(int(most_common_birth_year)) + ',', count_message + str(most_common_birth_year_count[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_trip_data(df):
    """Displays DataFrame rows of bikeshare users."""

    print('\nShowing individual trip data...\n')
    start_time = time.time()

    # variables: row_count, stop_count, dataFrameLength
    row_count = 0
    stop_count = 5
    dataFrameLength = len(df)

    # iterate over dataFrame
    for row in df.iterrows():

        # check if the whole dataFrame have been printed out or not
        if stop_count > dataFrameLength and (stop_count - dataFrameLength) > 4:
            print('\nNo more individual data avaiable.\n')
            break

        # print out five new rows
        if row_count < stop_count:
            print(row)
            print('-'*40)
            row_count += 1

        # after 5 rows have been printed out. As if user whant to see more data or not
        elif row_count == stop_count:

            see_more_bool = True
            end_function = False

            while see_more_bool:
                see_more = input('\nWould you like to see more data? Enter yes or no.\n').lower()
                if see_more == 'no':
                    see_more_bool = False
                    end_function = True
                elif see_more == 'yes':
                    see_more_bool = False
                    stop_count += 5
                else:
                    print('\nI didn\'t understand. Please try again.')

            # check if end function
            if end_function:
                print("\nThis took %s seconds." % (time.time() - start_time))
                print('-'*40)
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city, df)

        # Check if user want to se individual trip data
        trip_data_bool = True
        while trip_data_bool:
            see_trip_data = input('\nWould you like to see individual trip data? Enter yes or no.\n').lower()
            if see_trip_data == 'no':
                trip_data_bool = False
            elif see_trip_data == 'yes':
                trip_data_bool = False # this to not repeat the question again
                individual_trip_data(df)
            else:
                print('\nI didn\'t understand. Please try again.')

        # Check if user want to restart or end program
        restart_bool = True
        while restart_bool:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if restart == 'no':
                restart_bool = False
            elif restart == 'yes':
                main()
            else:
                print('\nI didn\'t understand. Please try again.')

        # end program
        break

if __name__ == "__main__":
	main()
