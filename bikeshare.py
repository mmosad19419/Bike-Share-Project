# import libs
import numpy as np
import pandas as pd
import time as dt
from itertools import product



# City data
city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#ask for the required data city, month, day
def get_user_input():
    # ask for the required city
    city = ""
    city_list = ["chicago", "new york city", "washington"]
    while city not in city_list:
        city = input("Which city you wany to analyze its data, available(Chicago, New York City, Washington):\n").lower().strip()

    #ask for the required month (month to choose OR all for all months)
    month = ""
    months_list = ["january", "february", "march", "april", "may", "june", "july", "october", "novamber", "december", "all"]
    while month not in months_list:
        month = input("Do you want to filter the data by month? if yes enter the month (January, ..., December), No enter all:\n").lower().strip()

    # ask for the required day
    day = ""
    day_list = ["saturday", "sunday", "monday", "tuesday", "wenesday", "thursday", "friday", "all"]
    while day not in day_list:
        day = input("Do you want to filter the data by day? if yes enter the day(Saturday, ..., Friday), No enter all:\n").lower().strip()

    print("Registering ..............")
    print('-'*40)


    return city, month, day

# Upload the data and apply the required filter to it, return the data as DataFrame
def load_data(city, month, day):
    #Get the city File
    city_file = city_data[city]
    df = pd.read_csv(city_file)

    #Wrangling data frame data
    #delete unimportant columns
    #drop null values
    df.drop(["Unnamed: 0"], axis = 1, inplace = True)
    df.dropna(inplace = True)

    # Convert the start, End dates columns to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df["Start Time"] = df['Start Time'].dt.strftime("%A-%B-%Y-%H:%M")
    df["End Time"] = df["End Time"].dt.strftime("%A-%B-%Y-%H:%M")

    #Create new columns for year, month, day
    df[["Start Day", "Start Month", "Start Year", "Start Hour"]] = df["Start Time"].str.split("-", expand = True)
    df["End Hour"] = df["End Time"].str.split("-", expand = True)[3]
    df["End Day"] = df["End Time"].str.split("-", expand = True)[0]

    # reset the ndex after removing null/Nan values
    df.reset_index(inplace = True)
    df.drop(["index"], axis = 1, inplace =True)


    #Check for month filter
    if month != "all":
        df = df[df["Start Month"] == month.title()]

    #Check for day filter:
    if day != "all":
        df = df[df["Start Day"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = dt.time()
    # display the most common month
    common_month = df["Start Month"].mode()[0]
    print("\n The most Common Month is: {}".format(common_month))

    # display the most common day of week
    common_day = df["Start Day"].mode()[0]
    print("\n The most Common Day is: {}".format(common_day))

    # display the most common start hour
    df["Hour"] = df["Start Hour"].str.split(":", expand = True)[0]
    common_hour = df["Hour"].mode()[0]
    print("\n The most Common Start Hour is: {}".format(common_hour))


    print("\nThis took %s seconds." % (dt.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = dt.time()

    # display most commonly used start station
    start_stat = df["Start Station"].mode()[0]
    print("\n The most Common Start Station is: {}".format(start_stat))

    # display most commonly used end station
    end_stat = df["End Station"].mode()[0]
    print("\n The most Common End Station is: {}".format(end_stat))

    # display most frequent combination of start station and end station trip
    df["Start_End Stations"] = df["Start Station"].str.cat(df["End Station"], sep = " To ")
    common_stat_comb = df["Start_End Stations"].mode()[0]
    print("\n The most Common Commbination of Start Station and End Station is: {}".format(common_stat_comb))

    print("\nThis took %s seconds." % (dt.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = dt.time()

    # display total travel time
    trave_time = df["Trip Duration"].sum()
    print("\n The Total Travel Time is: {} Seconds Or {} mins Or {} hours".format(int(trave_time), int(trave_time/60), int(trave_time/(60*60))))

    # display mean travel time
    avg_travel_time = df["Trip Duration"].mean()
    print("\n The Average Travel Time is: {} seconds".format(int(avg_travel_time)))


    print("\nThis took %s seconds." % (dt.time() - start_time))
    print('-'*40)



def print_row_data(df):
    # Check for user valid input
    display_raw = ""
    answer = ["yes", "no"]

    while display_raw not in answer:
        display_raw = input("Do you want explore raw data(Please Enter yes or no): ").lower().strip()

    # print 5 lines of raw data  and make it available to print more 5 by 5 lines
    # lines_counter start from 5 as i will use it after printing firt 5 lines
    lines_counter = 5
    if display_raw == "yes":
        # print first 5 lines of raw data
        print("Here is 5 lines of raw data:\n {}".format(df.head(5)))
        more = input("\nWould you like to explore more data? Please Enter yes or no.\n").lower().strip()

        # Print more data for the user if he want.
        while more == "yes":
            # Print more data to th euser
            print("Here is more 5 lines of raw data:\n {}".format(df[lines_counter : lines_counter + 5]))
            # See if the user want to see more data
            more = input("\nWould you like to explore more data? Please Enter yes or no.\n").lower().strip()

            if more.lower() == 'no':
                break

    print('-'*40)



def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = dt.time()

    # Display counts of user types
    print("\nCounts of User Type: {}".format(df["User Type"].value_counts()))

    # Check if we are exploring Washington city or not, as the washington data does not have Gender or Birthday data
    if city == "washington":
        print("\n\nSorry for not reporting any Gender or Birthday data-related as washington dataset does not have these data\n")
    else:
        # Display counts of gender
        print("\nCounts of User Gender: {}".format(df["Gender"].value_counts()))

        # Display earliest, most recent, and most common year of birth
        print("\nEarliest Year of Birth: {}".format(int(df["Birth Year"].min())))
        print("\nMost Recent Year of Birth: {}".format(int(df["Birth Year"].max())))
        print("\nMost common Year of Birth: {}".format(int(df["Birth Year"].mode()[0])))


    print("\nThis took %s seconds." % (dt.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_user_input()
        df = load_data(city, month, day)

        print_row_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
