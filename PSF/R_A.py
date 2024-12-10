from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import mysql.connector

#Connect to the database
mydb = mysql.connector.connect (
    host = "bq96ldxibxxeubxnxzpa-mysql.services.clever-cloud.com",
    user = "usiv06zwsjtem3rd",
    password = "KYfpMEsmyeqDaoxzP7jH",
    database = "bq96ldxibxxeubxnxzpa",
    port = 3306
)

#Create a cursor object
cursor = mydb.cursor ()

app = FastAPI()

#Class
class R_A (BaseModel):
    idR_A: int
    NumeroR_A: int
    #Competencia_idCompetencia: int

@app.get("/R_A", status_code=status.HTTP_302_FOUND)
def select_users():
    select_query = "SELECT * FROM R_A"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results

@app.get("/R_A/{idR_A}", status_code=status.HTTP_200_OK)
def get_user_by_id(idR_A: int):
    select_query = "SELECT * FROM R_A WHERE idR_A = %s"
    cursor.execute(select_query, (idR_A,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="R_A not found")
    
@app.post("/R_A", status_code=status.HTTP_201_CREATED)
def insert_user(R_A: R_A):

    insert_query = """
    INSERT INTO R_A (idR_A, NumeroR_A)
    VALUES (%s, %s)
    """
    values = (R_A.idR_A, R_A.NumeroR_A)

    try:
        cursor.execute(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "R_A inserted successfully"}

@app.put("/R_A/{idR_A}", status_code=status.HTTP_200_OK)
def update_user(idR_A: int, R_A: R_A):

    update_query = """
    UPDATE R_A
    SET NumeroR_A = %s
    WHERE idR_A = %s
    """
    values = (R_A.NumeroR_A, R_A.idR_A)

    cursor.execute(update_query, values)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="R_A not found")
    return {"message": "R_A updated successfully"}

@app.delete("/R_A/{idR_A}", status_code=status.HTTP_200_OK)
def delete_user(idR_A: int):
    delete_query = "DELETE FROM R_A WHERE idR_A = %s"
    cursor.execute(delete_query, (idR_A,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="R_A not found")
    return {"message": "R_A deleted successfully"}