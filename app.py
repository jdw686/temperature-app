from flask import Flask, render_template, request
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
Base = declarative_base()

app = Flask(__name__)

connection = create_engine('postgres://localhost:5432/planetly', echo=True)

class global_land_temperatures_by_city_prod_2(Base):
    __tablename__ = 'global_land_temperatures_by_city_prod_2'
    extend_existing=True
    dt = Column(String, primary_key = True)
    AverageTemperature = Column(Float)
    AverageTemperatureUncertainty = Column(Float)
    City = Column(Integer)
    Country = Column(Integer)
    Latitude = Column(Integer)
    Longitude = Column(Integer)

    def __init__(self,
                dt,
                AverageTemperature,
                AverageTemperatureUncertainty,
                City,
                Country,
                Latitude,
                Longitude):

        self.dt = dt
        self.AverageTemperature = AverageTemperature
        self.AverageTemperatureUncertainty = AverageTemperatureUncertainty
        self.City = City
        self.Country = Country
        self.Latitude = Latitude
        self.Longitude = Longitude


Base.metadata.create_all(connection)
Session = sessionmaker(bind=connection)
Session.configure(bind = connection)
session = Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    return render_template('add.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    options = ['AverageTemperature', 'AverageTemperatureUncertainty']
    return render_template('update.html', options=options, len_options=len(options))

@app.route('/query', methods=['GET', 'POST'])
def query():
    return render_template('query.html')

@app.route('/query_results', methods=['GET', 'POST'])
def query_results():
    start_date = request.args['start_date']
    end_date = request.args['end_date']
    cities_amount = request.args['cities_amount']

    query = """
            SELECT
            "City",
            MAX("AverageTemperature") max_temperature
            FROM global_land_temperatures_by_city_prod_2
            WHERE dt BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY "City"
            ORDER BY MAX("AverageTemperature") DESC
            LIMIT {cities_amount}
            """.format(start_date = start_date,
            end_date = end_date,
            cities_amount = cities_amount)

    results = pd.read_sql_query(query, con=connection)

    top_x_cities = list(results.City)

    top_x_temps = list(round(results.max_temperature, 1))

    return render_template('query_results.html',
    start_date = start_date,
    end_date = end_date,
    top_x_cities = top_x_cities,
    top_x_temps = top_x_temps,
    cities_amount = len(top_x_cities))

@app.route('/update_confirmation', methods=['GET', 'POST'])
def update_confirmation():
    selected_option = request.args['options']
    selected_input = request.args['selection_input']
    selected_city = request.args['city']
    selected_date = request.args['dt']

    update_statement = """
        UPDATE  global_land_temperatures_by_city_prod_2
        SET "{selected_option}"={selected_input}
        WHERE "City"='{selected_city}'
        AND "dt"='{selected_date}'"""

    connection.execute(update_statement.format(selected_option=selected_option,
    selected_input=selected_input,
    selected_city=selected_city,
    selected_date=selected_date))


    return render_template('update_confirmation.html',
    selected_date=selected_date,
    selected_city=selected_city,
    selected_option=selected_option,
    selected_input=selected_input)

@app.route('/add_confirmation', methods=['GET', 'POST'])
def add_confirmation():
    dt = request.args['dt']
    avg_temp = request.args['avg_temp']
    avg_temp_unc = request.args['avg_temp_unc']
    city = request.args['city']
    country = request.args['country']
    latitude = request.args['latitude']
    longitude = request.args['longitude']

    new_entry = global_land_temperatures_by_city_prod_2(
                dt=dt,
                AverageTemperature=avg_temp,
                AverageTemperatureUncertainty=avg_temp_unc,
                City=city,
                Country=country,
                Latitude=latitude,
                Longitude=longitude
            )

    session.add(new_entry)  # Add the user
    session.commit()  # Commit the change



    return render_template('add_confirmation.html',
    dt=dt,
    avg_temp=avg_temp,
    avg_temp_unc=avg_temp_unc,
    city=city,
    country=country,
    latitude=latitude,
    longitude=longitude)
