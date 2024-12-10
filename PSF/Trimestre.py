from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import date
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
class Trimestre (BaseModel):
    idTrimestre: int
    FechaInicio: date
    FechaFin: date

@app.get("/Trimestre", status_code=status.HTTP_302_FOUND)
def select_users():
    select_query = "SELECT * FROM Trimestre"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results

@app.get("/Trimestre/{idTrimestre}", status_code=status.HTTP_200_OK)
def get_user_by_id(idTrimestre: int):
    select_query = "SELECT * FROM Trimestre WHERE idTrimestre = %s"
    cursor.execute(select_query, (idTrimestre,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Trimestre not found")
    
@app.post("/Trimestre", status_code=status.HTTP_201_CREATED)
def insert_user(Trimestre: Trimestre):

    insert_query = """
    INSERT INTO Trimestre (idTrimestre, FechaInicio, FechaFin)
    VALUES (%s, %s, %s)
    """
    values = (Trimestre.idTrimestre, Trimestre.FechaInicio, Trimestre.FechaFin)

    try:
        cursor.execute(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "Trimestre inserted successfully"}

@app.put("/Trimestre/{idTrimestre}", status_code=status.HTTP_200_OK)
def update_user(idTrimestre: int, Trimestre: Trimestre):

    update_query = """
    UPDATE Trimestre
    SET FechaInicio = %s, FechaFin = %s
    WHERE idTrimestre = %s
    """
    values = (Trimestre.FechaInicio, Trimestre.FechaFin, Trimestre.idTrimestre)

    cursor.execute(update_query, values)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Trimestre not found")
    return {"message": "Trimestre updated successfully"}

@app.delete("/Trimestre/{idTrimestre}", status_code=status.HTTP_200_OK)
def delete_user(idTrimestre: int):
    delete_query = "DELETE FROM Trimestre WHERE idTrimestre = %s"
    cursor.execute(delete_query, (idTrimestre,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Trimestre not found")
    return {"message": "Trimestre deleted successfully"}