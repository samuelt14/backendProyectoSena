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
class Centro (BaseModel):
    idCentro: int
    Nombre: str
    Direccion: str
    Contacto: int

@app.get("/Centro", status_code=status.HTTP_302_FOUND)
def select_users():
    select_query = "SELECT * FROM Centro"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results

@app.get("/Centro/{idCentro}", status_code=status.HTTP_200_OK)
def get_user_by_id(idCentro: int):
    select_query = "SELECT * FROM Centro WHERE idCentro = %s"
    cursor.execute(select_query, (idCentro,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Centro not found")
    
@app.post("/Centro", status_code=status.HTTP_201_CREATED)
def insert_user(Centro: Centro):

    insert_query = """
    INSERT INTO Centro (idCentro, Nombre, Direccion, Contacto)
    VALUES (%s, %s, %s, %s)
    """
    values = (Centro.idCentro, Centro.Nombre, Centro.Direccion, Centro.Contacto)

    try:
        cursor.execute(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "Centro inserted successfully"}

@app.put("/Centro/{idCentro}", status_code=status.HTTP_200_OK)
def update_user(idCentro: int, Centro: Centro):

    update_query = """
    UPDATE Centro
    SET Nombre = %s, Direccion = %s, Contacto = %s
    WHERE idCentro = %s
    """
    values = (Centro.Nombre, Centro.Direccion, Centro.Contacto, Centro.idCentro)

    cursor.execute(update_query, values)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Centro not found")
    return {"message": "Centro updated successfully"}

@app.delete("/Centro/{idCentro}", status_code=status.HTTP_200_OK)
def delete_user(idCentro: int):
    delete_query = "DELETE FROM Centro WHERE idCentro = %s"
    cursor.execute(delete_query, (idCentro,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Centro not found")
    return {"message": "Centro deleted successfully"}