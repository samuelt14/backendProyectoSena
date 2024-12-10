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
class Ficha (BaseModel):
    idFicha: int
    Numero: int


@app.get("/Ficha", status_code=status.HTTP_302_FOUND)
def select_users():
    select_query = "SELECT * FROM Ficha"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results

@app.get("/Ficha/{idFicha}", status_code=status.HTTP_200_OK)
def get_user_by_id(idFicha: int):
    select_query = "SELECT * FROM Ficha WHERE idFicha = %s"
    cursor.execute(select_query, (idFicha,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Ficha not found")
    
@app.post("/Ficha", status_code=status.HTTP_201_CREATED)
def insert_user(Ficha: Ficha):

    insert_query = """
    INSERT INTO Ficha (idFicha, Numero)
    VALUES (%s, %s)
    """
    values = (Ficha.idFicha, Ficha.Numero)

    try:
        cursor.execute(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "Ficha inserted successfully"}

@app.put("/Ficha/{idFicha}", status_code=status.HTTP_200_OK)
def update_user(idFicha: int, Ficha: Ficha):

    update_query = """
    UPDATE Ficha
    SET Numero = %s
    WHERE idFicha = %s
    """
    values = (Ficha.Numero, Ficha.idFicha)

    cursor.execute(update_query, values)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Ficha not found")
    return {"message": "Ficha updated successfully"}

@app.delete("/Ficha/{idFicha}", status_code=status.HTTP_200_OK)
def delete_user(idFicha: int):
    delete_query = "DELETE FROM Ficha WHERE idFicha = %s"
    cursor.execute(delete_query, (idFicha,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Ficha not found")
    return {"message": "Ficha deleted successfully"}