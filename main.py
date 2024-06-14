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
    name: Optional[str]
    gender : Optional[str]
    city: Optional[str]
    contact_number : Optional[str]
    email : Optional[str] 
 
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
    

@app.post("/profile")
def user_reg(data:Data):
    try:
        '''
        post method for registration of user
        '''
        cursor.execute("INSERT INTO Users (name,gender,city,contact_number,email) VALUES(%s,%s,%s,%s,%s) RETURNING*",(data.name,data.gender,data.city,data.contact_number,data.email))
        new_user = cursor.fetchone()
        conn.commit()
        logging.info("User registered successfully: %s", new_user)  
        return {"data": new_user}
    except Exception as e:
        logging.error("Error occurred during user registration: %s", e) 
        return {"error":str(e)}
    
    
@app.put("/profile/{id}")
def user_update(id: int, data: Data):
    '''
    put method for updating details about particular id
    '''
    try:
        fields_to_update = []
        query_values = []

        if data.name:
            fields_to_update.append("name = %s")
            query_values.append(data.name)
        if data.gender:
            fields_to_update.append("gender = %s")
            query_values.append(data.gender)
        if data.city:
            fields_to_update.append("city = %s")
            query_values.append(data.city)
        if data.contact_number:
            fields_to_update.append("contact_number = %s")
            query_values.append(data.contact_number)
        if data.email:
            fields_to_update.append("email = %s")
            query_values.append(data.email)

        query_values.append(id)

        set_clause = ", ".join(fields_to_update)
        sql_query = f"UPDATE Users SET {set_clause} WHERE user_id = %s RETURNING *"

        cursor.execute(sql_query, query_values)
        updated_user = cursor.fetchone()
        conn.commit()
        logging.info("User details updated successfully: %s", updated_user)  
        return {"data": updated_user}
    except Exception as error:
        logging.error("Error occurred during user update: %s", error) 
        return {"error": str(error)}



@app.get("/profile/{id}")
def get_user(id: int):
    '''
    get method for getting details about id
    '''
    try:
        cursor.execute("SELECT * FROM Users WHERE user_id = %s", (id,))
        user = cursor.fetchone()
        logging.info("User details fetched successfully: %s", user)  
        return {"data": user}
    except Exception as e:
        logging.error("Error occurred during user update: %s", error) 
        return {"error": str(error)}

    

