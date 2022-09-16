import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Would you like to explore Chicago, New York, or Washington?\n').lower()
            if city in ['chicago','new york','washington']:
                break
            else:
                print('Invalid Input. Please try again. Use the name of the city as listed')
        except KeyboardInterrupt:
            print('Program interrupted. Please try again.')
    # get user input for month (all, january, february, ... , june)    
    while True:
        try:
            month = input('Which month would you like to explore?\nJanuary, February, March, April, May, June, or all?\n').lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june','all']:
                break
            else:
                print('Invalid input. Please try again. Use the name of the month as listed.')
        except KeyboardInterrupt:
            print('Program interrupted. Please try again.')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Which day would you like to explore?\nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, or all?\n').lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']:
                break
            else:
                print('Invalid input. Please try again. Use the name of the day as listed.')
        except KeyboardInterrupt:
            print('Program interrupted. Please try again.')
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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    pd.set_option('display.max_columns', None)
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] =  pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month+1]
    # filter by day of week if applicable
    if day != 'all':
        print(day)
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]
    return df

def display_rows(df,i):
    while True:
        try:
            answer=input('Would you like to see the rows {} to {} of data? Y/N\n'.format(i,i+5)).lower()
            if answer == 'y':
                print(df[i:i+5])
                i+=5
            elif answer == 'n':
                break
            else:
                print('Invalid Answer. please select either Y or N')
        except KeyboardInterrupt:
            print('Program Interrupted. Please Try Again')
            
def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        populer_month = df['month'].mode()[0]
        print('The most popular month is: {}'.format(populer_month))
        # display the most common day of week
    if day == 'all':
        populer_day = df['day_of_week'].mode()[0]
        print('The most popular day is: {}'.format(populer_day))
        # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour is: {}'.format(popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station','End Station']).size().idxmax() #from stackoverflow https://stackoverflow.com/questions/53037698/how-can-i-find-the-most-frequent-two-column-combination-in-a-dataframe-in-python
    print('The most popular start station is: {}'.format(popular_start_station))
    print('The most popular end station is: {}'.format(popular_end_station))
    print('The most popular combination of start and end stations is: {}'.format(popular_combination))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The total travel time is: {}'.format(total_travel_time))
    print('The average travel time is: {}'.format(mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    # Display counts of gender
    if 'Gender' in df.columns:
        user_types = df['Gender'].value_counts()
        print('The counts of Genders are as follows: {}'.format(user_types))
    else:
        print("This city doesn't have data on gender")
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()#[0]
        print('The earliest birth year is: {}'.format(earliest_birth))
        print('The most recent birth year is: {}'.format(recent_birth))
        print('The most common year of birth is: {}'.format(common_year))
    else:
        print("This city doesn't have data on users' birth years")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_rows(df,0)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        try:
            restart = input('\nWould you like to restart? Enter yes or enter any key to exit.\n')
            if restart.lower() != 'yes' and restart.lower() != 'y':
                break
        except KeyboardInterrupt:
            print("Program Interrupted...Restarting")
            continue
            

if __name__ == "__main__":
	main()

#Speical thanks to my sister for helping me crash-proof this program
#Thanks to stackoverflow users for thir help.