import fastapi
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

class Data(BaseModel):
    user_id : Optional[str]
    location : Optional[str]
    looking_for : Optional[str]
    approx_rent: Optional[str]
    occupancy : Optional[str]
    who_you_are: Optional[str]
    highlight_for_property : Optional[str]
    
def get_cursor():
    '''
    Function to get a cursor object for database operations
    '''
#connecting with database   
    try:
        """
        connection with database roommate_db in postgresql
        """
        conn = psycopg2.connect(host= 'localhost', database ='roommate_DB',user = 'postgres', password = 'Abhishek@2399', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        # print("Database connection successfull")
        logging.info("Database connection successfull")   
    except Exception as error:
        # print("Connection failed")
        logging.error("Connection failed : %s", error)
        
        # print("Error:" , error)


  
@app.post("/add_listing")
def add_listing(data: Data):
    '''
    post method to add listing on the portal 
    '''
    try:
        cursor.execute("""INSERT INTO person_roommate(user_id, location, looking_for, approx_rent, occupancy, who_you_are, highlight_for_property) VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING *""", (str(data.user_id), data.location, data.looking_for, str(data.approx_rent), data.occupancy, data.who_you_are, data.highlight_for_property))
        new_listing = cursor.fetchone()
        conn.commit()
        logging.info("new listing added successfully : %s", new_listing)
        return {"data": new_listing}
    except Exception as error:
        logging.error("Error occurred during adding listing : %s", error)
        return {"error": error}


@app.put("/edit_listing/{user_id}")
def edit_listing(user_id: int, data: Data):
    '''
    put method to update the details about a particular listing
    '''
    try:
        fields_to_update = []
        query_values = []
        if data.location:
            fields_to_update.append("location = %s")
            query_values.append(data.location)
        if data.looking_for:
            fields_to_update.append("looking_for = %s")
            query_values.append(data.looking_for)
        if data.approx_rent:
            fields_to_update.append("approx_rent = %s")
            query_values.append(data.approx_rent)
        if data.occupancy:
            fields_to_update.append("occupancy = %s")
            query_values.append(data.occupancy)
        if data.who_you_are:
            fields_to_update.append("who_you_are = %s")
            query_values.append(data.who_you_are)
        if data.highlight_for_property:
            fields_to_update.append("highlight_for_property = %s")
            query_values.append(data.highlight_for_property)

        query_values.append(user_id)
        set_clause = ", ".join(fields_to_update)
        sql_query = f"UPDATE person_roommate SET {set_clause} WHERE user_id = %s RETURNING *"
        cursor.execute(sql_query, query_values)
        conn.commit()
        updated_listing = cursor.fetchone()
        logging.info("listing updated successfully : %s", updated_listing)
        return {"data": updated_listing}
    except Exception as e:
        logging.error("error occurred during updating a listing : %s", e)
        return {"error": str(e)}


@app.get("/get_listing")
def get_listing():
    '''
    get method to get the details about a particular listing
    '''
    try:
        cursor.execute("""SELECT Users.name, Users.gender, Users.contact_number, person_roommate.location, person_roommate.looking_for, person_roommate.who_you_are FROM Users 
                       INNER JOIN person_roommate on Users.user_id = person_roommate.user_id""")
        listings = cursor.fetchall()
        logging.info("listing fetched successfully: %s", listings)
        return {"data": listings}
    except Exception as e:
        logging.error("error occurrred during fetching a listing : %s", e)
        return {"error": str(e)}


@app.get("/get_listing_by_city")
def get_listing_by_city(data: Data):
    '''
    get method to get the details about a particular listing by city
    '''
    try:
        cursor.execute("""SELECT Users.name, Users.gender, Users.contact_number, person_roommate.location, person_roommate.looking_for, person_roommate.who_you_are FROM Users 
                       INNER JOIN person_roommate ON Users.user_id = person_roommate.user_id WHERE person_roommate.location = %s""", (data.location,))
        listings = cursor.fetchall()
        logging.info("listing by city fetched successfully : %s", listings)
        return {"data": listings}
    except Exception as e:
        logging.error("error occurred during fetching a listing by city : %s", e)
        return {"error": str(e)}


