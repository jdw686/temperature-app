Notes on the Temperature Database

1. Introduction
My experience is based primarily in Python and Pandas. Our current Flask application framework at idealo presently relies on Python and the AWS Python SDK (Boto3, specifically the Athena Query module). In the absence of working in the AWS, I chose to work primarily in Python and a mix of Pandas and SQL Alchemy ORM (Object Relational Mapping). 

2. Challenges
Uploading the data to a local PostgreSQL database was surprisingly a challenge. With 8,5 million entries, and the file size of about 530 MB, I was not sure how long it would take to fully upload the data into my local database. To track this, I used the to_sql method in Pandas in a for loop to monitor the progress of the upload. I iterated based on the amount of cities in the data set. See code below:

for i in range(len(df.City.unique()[12:])):
    print(i)
    df[df.City == df.City.unique()[i]].to_sql('global_land_temperatures_by_city_prod', connection, if_exists='append')
