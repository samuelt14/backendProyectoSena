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
class Coordinador (BaseModel):
    idCoordinador: int
    Nombre: str
    Correo: str
    Contacto: int
    Cedula: int
    #Coordinacion_idCoordinacion: int
    #Coordinacion_Administrador_idAdministrador: int
    #`Coordinacion_Centro_idCentro: int


@app.get("/Coordinador", status_code=status.HTTP_302_FOUND)
def select_users():
    select_query = "SELECT * FROM Coordinador"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results

@app.get("/Coordinador/{idCoordinador}", status_code=status.HTTP_200_OK)
def get_user_by_id(idCoordinador: int):
    select_query = "SELECT * FROM Coordinador WHERE idCoordinador = %s"
    cursor.execute(select_query, (idCoordinador,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Coordinador not found")
    
@app.post("/Coordinador", status_code=status.HTTP_201_CREATED)
def insert_user(Coordinador: Coordinador):

    insert_query = """
    INSERT INTO Coordinador (idCoordinador, Nombre, Correo, Contacto, Cedula)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (Coordinador.idCoordinador, Coordinador.Nombre, Coordinador.Correo, Coordinador.Contacto, Coordinador.Cedula )

    try:
        cursor.execute(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "Coordinador inserted successfully"}

@app.put("/Coordinador/{idCoordinador}", status_code=status.HTTP_200_OK)
def update_user(idCoordinador: int, Coordinador: Coordinador):

    update_query = """
    UPDATE Coordinador
    SET Nombre = %s, Correo = %s, Contacto = %s, Cedula = %s
    WHERE idCoordinador = %s
    """
    values = (Coordinador.Nombre, Coordinador.Correo, Coordinador.Contacto, Coordinador.Cedula, Coordinador.idCoordinador)

    cursor.execute(update_query, values)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Coordinador not found")
    return {"message": "Coordinador updated successfully"}

@app.delete("/Coordinador/{idCoordinador}", status_code=status.HTTP_200_OK)
def delete_user(idCoordinador: int):
    delete_query = "DELETE FROM Coordinador WHERE idCoordinador = %s"
    cursor.execute(delete_query, (idCoordinador,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Coordinador not found")
    return {"message": "Coordinador deleted successfully"}