import json
from reactpy import component, html
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
app = FastAPI()
with open("./content.json") as content: #Leer las preguntas desde el archivo JSON
    questions = json.load(content)

@component #Componente principal
def App():
    return html.div({"style":{"font-family":"Segoe UI"}}, #Contenedor general (body)
        html.main({"style":{"margin-left":"15vw","width":"65vw"}}, #Contenedor de la encuesta
            html.header( #Encabezado de la página
            {"style":{"display":"flex","justify-content":"center", "background-color":"#212121","color":"white","margin-top": "-8px", "height":"10vh"}},
            html.h1("Encuesta de satisfacción del usuario")
        ),
        html.p({"style":{"color":"#454545"}},"Tu opinión es muy importante para nosotros, por lo tanto nos gustaría que respondas la siguiente encuesta de satisfacción. Gracias por usar nuestros servicios, usamos tus opiniones para mejorar cada día y ofrecer un mejor servicio."),
        html.h2("Selecciona la cantidad de estrellas en una calificación de 1 a 5"),
        html.div( #Contenedor de las preguntas
            Star_Question(0),
            Star_Question(1),
            Star_Question(2),
            Radio_Question(3),
            Radio_Question(4),
            Radio_Question(5),
            Open_Question(6),
            Open_Question(7)
            

        )
        ),
    )

@component
def Star_Question(idx): #Componente de pregunta de estrellas
    not_selected = "https://i.ibb.co/RptMG5X/Tabler-Star-Uns.png"
    selected = "https://i.ibb.co/MPfkd9c/Tabler-Star.png"
    return html.section( #Contenedor principal de la pregunta
        html.h3(f"{questions[idx]["id"]} - {questions[idx]["text"]}"), html.br(), #Número y texto de la pregunta
        html.div({"style":{"display":"flex", "gap":"20px"}}, #Contenedor de las estrellas
            html.img({"src":not_selected, "style":{"width":"30px", "margin-left":"28px", "cursor":"pointer"}}),
            html.img({"src":not_selected, "style":{"width":"30px", "cursor":"pointer"}}),
            html.img({"src":not_selected, "style":{"width":"30px", "cursor":"pointer"}}),
            html.img({"src":not_selected, "style":{"width":"30px", "cursor":"pointer"}}),
            html.img({"src":not_selected, "style":{"width":"30px", "cursor":"pointer"}})
        ), html.br(), html.br()
    )



@component
def Radio_Question(idx): #Componente de preguntas Sí/No
    def Opinion_Text(): #Función que genera el texto y el input de la opinión libre según el índice de la pregunta (Próximamente esto solo saldrá cuando se responda de forma negativa a la pregunta)
        a = 0
        if idx == 3:
            return html.section(
                html.h6({"style":{"margin-bottom":"10px"}},"¿Podría describirnos su inconformidad?"),
                html.textarea({"placeholder":"Ingrese aquí sus comentarios.", "style":{"width":"70%", "height":"100px", "resize":"none"}}), html.br(), html.br()
            )
        
        elif idx == 4:
            return html.section(
                html.h6({"style":{"margin-bottom":"10px"}},"¿Por qué?"),
                html.textarea({"placeholder":"Ingrese aquí sus comentarios.", "style":{"width":"70%", "height":"100px", "resize":"none"}}), html.br(), html.br()
            )
        elif idx == 5:
            return html.section(
                html.h6({"style":{"margin-bottom":"10px"}},"¿En qué podríamos mejorar?"),
                html.textarea({"placeholder":"Ingrese aquí sus comentarios.", "style":{"width":"70%", "height":"100px", "resize":"none"}}), html.br(), html.br()
            )
        else:
            return html.br() #Retornar un salto de línea en caso de no haber necesidad de mostrar el cuadro de texto
    
    return html.section(
        html.h3(f"{questions[idx]["id"]} - {questions[idx]["text"]}"), html.br(),
        html.div({"style":{"font-size":"25px", "margin-left":"28px"}},
            html.label({"style":{"width":"30px"}},
                html.input({"type":"radio", "name":str(idx+1)}), "Sí"), html.br(), html.br(),
            html.label({"style":{"width":"30px"}},
                html.input({"type":"radio", "name":str(idx+1), "style":{"color":""}}), "No"), html.br(),
                Opinion_Text()
            
        )
    )

@component
def Open_Question(idx):
    return html.section(
                html.h3(f"{questions[idx]["id"]} - {questions[idx]["text"]}"), html.br(),
                html.textarea({"placeholder":"Ingrese aquí sus opiniones.", "style":{"width":"70%", "height":"100px", "margin-left":"28px", "resize":"none"}}), html.br(), html.br()
            )

configure(app, App)