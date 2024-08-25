import json
from reactpy import component, html, hooks
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
app = FastAPI()
with open("./content.json") as content: #Leer las preguntas desde el archivo JSON
    questions = json.load(content)



@component #Componente principal
def App():

    def handleRatingChange(idx, newRating):
        print(idx, newRating)

    return html.div({"style":{"font-family":"Segoe UI"}}, #Contenedor general (body)
        html.main({"style":{"margin-left":"15vw","width":"65vw"}}, #Contenedor de la encuesta
            html.header( #Encabezado de la página
            {"style":{"display":"flex","justify-content":"center", "background-color":"#212121","color":"white","margin-top": "-8px", "height":"10vh"}},
            html.h1("Encuesta de satisfacción del usuario")
        ),
        html.p({"style":{"color":"#454545"}},"Tu opinión es muy importante para nosotros, por lo tanto nos gustaría que respondas la siguiente encuesta de satisfacción. Gracias por usar nuestros servicios, usamos tus opiniones para mejorar cada día y ofrecer un mejor servicio."),
        html.h2("Selecciona la cantidad de estrellas en una calificación de 1 a 5"),
        html.div( #Contenedor de las preguntas
            Star_Question(0, handleRatingChange),
            Star_Question(1, handleRatingChange),
            Star_Question(2, handleRatingChange),
            Radio_Question(3),
            Radio_Question(4),
            Radio_Question(5),
            Open_Question(6),
            Open_Question(7)
            

        )
        
        ),
    )

@component
def Star_Question(idx, onRatingChange): #Componente de pregunta de estrellas
    rating, set_rating = hooks.use_state(0)
    not_selected = "https://i.ibb.co/RptMG5X/Tabler-Star-Uns.png"
    selected = "https://i.ibb.co/MPfkd9c/Tabler-Star.png"

    def handleStarClick(rating): #Función para establecer la calificación de l actual pregunta y pasarle el valor al componente App
        set_rating(rating)
        onRatingChange(idx, rating)
        
    return html.section( #Contenedor principal de la pregunta
        html.h3(f"{questions[idx]["id"]} - {questions[idx]["text"]}"), html.br(), #Número y texto de la pregunta
        html.div({"style":{"display":"flex", "gap":"20px"}}, #Contenedor de las estrellas
            html.img({"on_click":lambda x: handleStarClick(1),"src":not_selected, "style":{"width":"30px", "margin-left":"28px", "cursor":"pointer"}}),
            html.img({"on_click":lambda x: handleStarClick(2),"src":not_selected, "style":{"width":"30px", "cursor":"pointer"}}),
            html.img({"on_click":lambda x: handleStarClick(3),"src":not_selected, "style":{"width":"30px", "cursor":"pointer"}}),
            html.img({"on_click":lambda x: handleStarClick(4),"src":not_selected, "style":{"width":"30px", "cursor":"pointer"}}),
            html.img({"on_click":lambda x: handleStarClick(5),"src":not_selected, "style":{"width":"30px", "cursor":"pointer"}})
        ), html.br(), html.br()
    )



@component
def Radio_Question(idx): #Componente de preguntas Sí/No
    def Opinion_Text(): #Función que genera el texto y el input de la opinión libre según el índice de la pregunta (Próximamente esto solo saldrá cuando se responda de forma negativa a la pregunta)
        a = 0
        if a == 0:
            return html.section(
                html.h6({"style":{"margin-bottom":"10px"}}, questions[idx]["opt-text"]),
                html.textarea({"placeholder":"Ingrese aquí sus comentarios.", "style":{"width":"70%", "height":"100px", "resize":"none"}}), html.br(), html.br(),
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