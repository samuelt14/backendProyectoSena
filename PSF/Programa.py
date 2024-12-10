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
class Programa (BaseModel):
    idPrograma: int
    Nombre: str
    Tipo: str

@app.get("/Programa", status_code=status.HTTP_302_FOUND)
def select_users():
    select_query = "SELECT * FROM Programa"
    cursor.execute(select_query)
    results = cursor.fetchall()
    return results

@app.get("/Programa/{idPrograma}", status_code=status.HTTP_200_OK)
def get_user_by_id(idPrograma: int):
    select_query = "SELECT * FROM Programa WHERE idPrograma = %s"
    cursor.execute(select_query, (idPrograma,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Programa not found")
    
@app.post("/Programa", status_code=status.HTTP_201_CREATED)
def insert_user(Programa: Programa):

    insert_query = """
    INSERT INTO Programa (idPrograma, Nombre, Tipo)
    VALUES (%s, %s, %s)
    """
    values = (Programa.idPrograma, Programa.Nombre, Programa.Tipo)

    try:
        cursor.execute(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "Programa inserted successfully"}

@app.put("/Programa/{idPrograma}", status_code=status.HTTP_200_OK)
def update_user(idPrograma: int, Programa: Programa):

    update_query = """
    UPDATE Programa
    SET Nombre = %s, Tipo = %s
    WHERE idPrograma = %s
    """
    values = (Programa.Nombre, Programa.Tipo, Programa.idPrograma)

    cursor.execute(update_query, values)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Programa not found")
    return {"message": "Programa updated successfully"}

@app.delete("/Programa/{idPrograma}", status_code=status.HTTP_200_OK)
def delete_user(idPrograma: int):
    delete_query = "DELETE FROM Programa WHERE idPrograma = %s"
    cursor.execute(delete_query, (idPrograma,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Programa not found")
    return {"message": "Programa deleted successfully"}