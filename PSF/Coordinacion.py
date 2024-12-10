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
class Coordinacion (BaseModel):
    idCoordinacion: int
    Nombre: str
    Correo: str
    #Administrador_idAdministrador: int
    #Centro_idCentro: int


@app.get("/Coordinacion", status_code=status.HTTP_302_FOUND)
def select_users():
    select_query = "SELECT * FROM Coordinacion"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results

@app.get("/Coordinacion/{idCoordinacion}", status_code=status.HTTP_200_OK)
def get_user_by_id(idCoordinacion: int):
    select_query = "SELECT * FROM Coordinacion WHERE idCoordinacion = %s"
    cursor.execute(select_query, (idCoordinacion,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Coordinacion not found")
    
@app.post("/Coordinacion", status_code=status.HTTP_201_CREATED)
def insert_user(Coordinacion: Coordinacion):

    insert_query = """
    INSERT INTO Coordinacion (Nombre)
    VALUES (%s)
    """
    values = (Coordinacion.idCoordinacion, Coordinacion.Nombre)

    try:
        cursor.execute(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "Coordinacion inserted successfully"}

@app.put("/Coordinacion/{idCoordinacion}", status_code=status.HTTP_200_OK)
def update_user(idCoordinacion: int, Coordinacion: Coordinacion):

    update_query = """
    UPDATE Coordinacion
    SET Nombre = %s
    WHERE idCoordinacion = %s
    """
    values = (Coordinacion.Nombre, Coordinacion.idCoordinacion)

    cursor.execute(update_query, values)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Coordinacion not found")
    return {"message": "Coordinacion updated successfully"}

@app.delete("/Coordinacion/{idCoordinacion}", status_code=status.HTTP_200_OK)
def delete_user(idCoordinacion: int):
    delete_query = "DELETE FROM Coordinacion WHERE idCoordinacion = %s"
    cursor.execute(delete_query, (idCoordinacion,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Coordinacion not found")
    return {"message": "Coordinacion deleted successfully"}