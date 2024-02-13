# sqlalchemy-challenge
module 10 challenge vbu bootcamp
Used this repo to guide me through the flask process https://github.com/bennetyousuf/sqlalchemy-challenge/blob/main/app.py
I mostly used this to get the start and end dates to work because they needed to be an element in the app route.

![Alt](https://github.com/comfyben/sqlalchemy-challenge/blob/main/screen_shot.png)


I knew the end date and start date from the climate_starter notebook so I was able to kind of copy the code but I didn't use the physical date bc I don't feel comfortable using the datetime library. I found the start_date in the csv file and used the [-5] to select that date from limiting the data. almost just used the .limit(365) to get the date I ran into errors that showed me the wrong date.