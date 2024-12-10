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
class Alerta (BaseModel):
    idAlerta: int
    mensaje: str
    fecha_Alerta: date


@app.get("/Alerta", status_code=status.HTTP_302_FOUND)
def select_users():
    select_query = "SELECT * FROM Alerta"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results

@app.get("/Alerta/{idAlerta}", status_code=status.HTTP_200_OK)
def get_user_by_id(idAlerta: int):
    select_query = "SELECT * FROM Alerta WHERE idAlerta = %s"
    cursor.execute(select_query, (idAlerta,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Alerta not found")
    
@app.post("/Alerta", status_code=status.HTTP_201_CREATED)
def insert_user(Alerta: Alerta):

    insert_query = """
    INSERT INTO Alerta (idAlerta, mensaje, fecha_Aleta)
    VALUES (%s, %s)
    """
    values = (Alerta.idAlerta, Alerta.mensaje, Alerta.fecha_Alerta)

    try:
        cursor.execute(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "Alerta inserted successfully"}

@app.put("/Alerta/{idAlerta}", status_code=status.HTTP_200_OK)
def update_user(idAlerta: int, Alerta: Alerta):

    update_query = """
    UPDATE Alerta
    SET mensaje = %s, Fecha_Alerta=%s
    WHERE idAlerta = %s
    """
    values = (Alerta.mensaje, Alerta.idAlerta, Alerta.fecha_Alerta)

    cursor.execute(update_query, values)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Alerta not found")
    return {"message": "Alerta updated successfully"}

@app.delete("/Alerta/{idAlerta}", status_code=status.HTTP_200_OK)
def delete_user(idAlerta: int):
    delete_query = "DELETE FROM Alerta WHERE idAlerta = %s"
    cursor.execute(delete_query, (idAlerta,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Alerta not found")
    return {"message": "Alerta deleted successfully"}