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
class Aprendiz (BaseModel):
    idAprendiz: int
    Nombre: str
    Correo: str
    Idententificacion: str
    NumeroIdentificacion: int
    #Ficha_idFicha: int


@app.get("/Aprendiz", status_code=status.HTTP_200_OK)
def get_user_by_credentials(idAprendiz: int, password: str):
    select_query = "SELECT * FROM Aprendiz WHERE idAprendiz = %s AND password = %s"
    cursor.execute(select_query, (idAprendiz, password))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Aprendiz not found")

@app.get("/Aprendiz/{idAprendiz}", status_code=status.HTTP_200_OK)
def get_user_by_id(idAprendiz: int):
    select_query = "SELECT * FROM Aprendiz WHERE idAprendiz = %s"
    cursor.execute(select_query, (idAprendiz,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Aprendiz not found")
    
@app.post("/Aprendiz", status_code=status.HTTP_201_CREATED)
def insert_user(Aprendiz: Aprendiz):

    insert_query = """
    INSERT INTO Aprendiz (idAprendiz, Nombre, Correo, Idententificacion, NumeroIdentificacion)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (Aprendiz.idAprendiz, Aprendiz.Nombre, Aprendiz.Correo, Aprendiz.Idententificacion, Aprendiz.NumeroIdentificacion)

    try:
        cursor.execute(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "Aprendiz inserted successfully"}

@app.put("/Aprendiz/{idAprendiz}", status_code=status.HTTP_200_OK)
def update_user(idAprendiz: int, Aprendiz: Aprendiz):

    update_query = """
    UPDATE Aprendiz
    SET Nombre = %s, Correo = %s, Idententificacion = %s, NumeroIdentificacion = %s
    WHERE idAprendiz = %s
    """
    values = (Aprendiz.Nombre, Aprendiz.Correo, Aprendiz.Idententificacion, Aprendiz.NumeroIdentificacion, Aprendiz.idAprendiz)

    cursor.execute(update_query, values)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Aprendiz not found")
    return {"message": "Aprendiz updated successfully"}

@app.delete("/Aprendiz/{idAprendiz}", status_code=status.HTTP_200_OK)
def delete_user(idAprendiz: int):
    delete_query = "DELETE FROM Aprendiz WHERE idAprendiz = %s"
    cursor.execute(delete_query, (idAprendiz,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Aprendiz not found")
    return {"message": "Aprendiz deleted successfully"}