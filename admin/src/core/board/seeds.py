from src.core.models.Institutional_Services.services import Service
from datetime import datetime
from src.core.board.database import db
import random


    
list_Names = ["Servicio1","Servicio2","Servicio3","Servicio4","Servicio5","Servicio6",
              "Servicio1","Servicio1","Servicio4","Servicio10"]
    
list_Desp = ["Descripción del servicio1","Descripción del servicio2","Descripción del servicio3",
                "Descripción del servicio4","Descripción del servicio5","Descripción del servicio6",
                "Descripción del servicio","Descripción del servicio1","Descripción del servicio4",
                "Descripción del servicio10"]

list_kEY = [["UNO","I"],
                ["DOS","II"],
                ["TRES","III"],
                ["CUATRO","IV"],
                ["CINCO","V"],
                ["SEIS","VI"],
                ["SIETE","VII"],
                ["OCHO","VIII"],
                ["NUEVE","IX"],
                ["DIES","X"]]

def create_Service(nam,des,key):
     
    new_service = Service(
    name=nam,
    description=des,
    search_keywords=key,
    type_of_service=random.choice([Service.TypeService.Análisis, Service.TypeService.Consultoría, Service.TypeService.Desarrollo]),  # Otra opción: Service.TypeService.Consultoría
    enabled=random.choice([True, False]),
    updated_at=datetime.utcnow(),
    inserted_at=datetime.utcnow(),
    institutions_id=random.randint(1, 4) )# ID de la institución relacionada
    
    return new_service

def run():

    for numero in range(10):
        new_service = create_Service(list_Names[numero],list_Desp[numero],list_kEY[numero])
        # Agregar el nuevo servicio a la base de datos
        db.session.add(new_service)
        db.session.commit()



