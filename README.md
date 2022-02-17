Notes on the Temperature Database

1. Introduction
My experience is based primarily in Python and Pandas. Our current Flask application framework at idealo presently relies on Python and the AWS Python SDK (Boto3, specifically the Athena Query module). In the absence of working in the AWS, I chose to work primarily in Python and a mix of Pandas and SQL Alchemy ORM (Object Relational Mapping). 

2. Challenges
Uploading the data to a local PostgreSQL database was surprisingly a challenge. With 8,5 million entries, and the file size of about 530 MB, I was not sure how long it would take to fully upload the data into my local database. To track this, I used the to_sql method in Pandas in a for loop to monitor the progress of the upload. I iterated based on the amount of cities in the data set. See code below:

for i in range(len(df.City.unique())):
    print(i)
    df[df.City == df.City.unique()[i]].to_sql('global_land_temperatures_by_city_prod', connection, if_exists='append')
    
This took about 45-50 minutes to fully upload. At first I thought this would be unreasonable but I also recalled a manual upload that my current time did of some historical data, and with the file size much larger and uploading into the Cloud, it still took a couple of hours with a very fast internet upload speed.
    
    

X. Answers to the Challenge Questions
    a. Tie between Masjed E Soleyman and Ahvaz (at 39.156C). I chose Ahvaz to add and update the temperature.
    b. A maximum average temperature for Ahvaz was added at 39.256C for the current calendar month (let's suspend belief for a moment).
    c. With the input of the date and city mentioned above, I updated the entry to be 2.5 degrees lower, at 36.756C.
    
    d. Other notes: the language used in the coding challenge was somewhat unclear about whether I should use AVG or MAX as the aggregate in the challenge. If MAX was incorrect, it would be a simple fix to change in the query, and do the exercise over again.
