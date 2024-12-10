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
class Competencia (BaseModel):
    idCompetencia: int
    Nombre: int
    Tipo: str
    Trimestre: int


@app.get("/Competencia", status_code=status.HTTP_302_FOUND)
def select_users():
    select_query = "SELECT * FROM Competencia"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results

@app.get("/Competencia/{idCompetencia}", status_code=status.HTTP_200_OK)
def get_user_by_id(idCompetencia: int):
    select_query = "SELECT * FROM Competencia WHERE idCompetencia = %s"
    cursor.execute(select_query, (idCompetencia,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Competencia not found")
    
@app.post("/Competencia", status_code=status.HTTP_201_CREATED)
def insert_user(Competencia: Competencia):

    insert_query = """
    INSERT INTO Competencia (idCompetencia, Nombre, Tipo, Trimestre)
    VALUES (%s, %s, %s, %s)
    """
    values = (Competencia.idCompetencia, Competencia.Nombre, Competencia.Tipo, Competencia.Trimestre)

    try:
        cursor.execute(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "Competencia inserted successfully"}

@app.put("/Competencia/{idCompetencia}", status_code=status.HTTP_200_OK)
def update_user(idCompetencia: int, Competencia: Competencia):

    update_query = """
    UPDATE Competencia
    SET Nombre = %s, Tipo = %s, Trimestre =%s
    WHERE idCompetencia = %s
    """
    values = (Competencia.Nombre, Competencia.Tipo, Competencia.Trimestre, Competencia.idCompetencia)

    cursor.execute(update_query, values)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Competencia not found")
    return {"message": "Competencia updated successfully"}

@app.delete("/Competencia/{idCompetencia}", status_code=status.HTTP_200_OK)
def delete_user(idCompetencia: int):
    delete_query = "DELETE FROM Competencia WHERE idCompetencia = %s"
    cursor.execute(delete_query, (idCompetencia,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Competencia not found")
    return {"message": "Competencia deleted successfully"}