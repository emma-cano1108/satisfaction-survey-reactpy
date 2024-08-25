import json
from reactpy import component, html, hooks
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
app = FastAPI()
with open("./content.json") as content: #Leer las preguntas desde el archivo JSON
    questions = json.load(content)

answers=[]
# current_answer={"id":1, "q1":0, "q2":0, "q3":0,"q4":0, "q4_comment":"", "q5":0, "q5_comment":"", "q6":0, "q6_comment":"", "q7":"","q8":""}

@component #Componente principal
def App():
    current_answer={"id":1}
    def handleRatingChange(idx, newRating): #Función que recibe y almacena el valor de cada StarQuestion y RadioQuestion en el diccionario current_answer
        current_answer["q"+str((idx+1))] = int(newRating)
        print(current_answer)

    def handleCommentChange(idx, newComment):
        current_answer["q"+str((idx+1))+"_comment"] = newComment
        print(current_answer)

    def handleOpinionChange(idx, newOpinion):
        current_answer["q"+str((idx+1))] = newOpinion
        print(current_answer)
    
        
    

    def handleSubmit():
        apply_answer = current_answer.copy()
        
        answers.append(apply_answer)
        print(answers)
        
        return
        
        

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
            Radio_Question(3, handleRatingChange, handleCommentChange),
            Radio_Question(4, handleRatingChange, handleCommentChange),
            Radio_Question(5, handleRatingChange, handleCommentChange),
            Open_Question(6, handleOpinionChange),
            Open_Question(7, handleOpinionChange)
        ),
        html.button({"on_click":lambda x: handleSubmit(),"style":{"height":"50px","width":"20%", "margin-left":"28px","font-size":"20px"}},"ENVIAR")
        ),
    )

@component
def Star_Question(idx, onRatingChange): #Componente de pregunta de estrellas
    rating, set_rating = hooks.use_state(0)
    not_selected = "https://i.ibb.co/RptMG5X/Tabler-Star-Uns.png"
    selected = "https://i.ibb.co/MPfkd9c/Tabler-Star.png"

    def handleStarClick(rating): #Función para establecer la calificación de la actual pregunta y pasarle el valor al componente App
        set_rating(rating)
        onRatingChange(idx, rating)
        
    return html.section( #Contenedor principal de la pregunta
        html.h3(f"{questions[idx]["id"]} - {questions[idx]["text"]}"), html.br(), #Número y texto de la pregunta
        html.div({"style":{"display":"flex", "gap":"20px"}}, #Contenedor de las estrellas
            html.img({"on_click":lambda x: handleStarClick(1),"src":not_selected if rating < 1 else selected, "style":{"width":"30px", "margin-left":"28px", "cursor":"pointer"}}),
            html.img({"on_click":lambda x: handleStarClick(2),"src":not_selected if rating < 2 else selected, "style":{"width":"30px", "cursor":"pointer"}}),
            html.img({"on_click":lambda x: handleStarClick(3),"src":not_selected if rating < 3 else selected, "style":{"width":"30px", "cursor":"pointer"}}),
            html.img({"on_click":lambda x: handleStarClick(4),"src":not_selected if rating < 4 else selected, "style":{"width":"30px", "cursor":"pointer"}}),
            html.img({"on_click":lambda x: handleStarClick(5),"src":not_selected if rating < 5 else selected, "style":{"width":"30px", "cursor":"pointer"}})
        ), html.br(), html.br()
    )



@component
def Radio_Question(idx, onRadioChange, onCommentChange): #Componente de preguntas Sí/No
    radio_option, set_radio_option = hooks.use_state(None)
    def radioHandleChange(e):#Callback para pasar valor al componente App
        set_radio_option(e["target"]["value"])
        onRadioChange(idx, e["target"]["value"])

    def commentHandleChange(e): #Callback para pasar cadena del comentario en caso de existir
        onCommentChange(idx, e["target"]["value"])

    def Opinion_Text(): #Función que genera el texto y el input de la opinión libre según el índice de la pregunta y la opción seleccionada
        

        if radio_option == 0:
            return html.section(
                html.h6({"style":{"margin-bottom":"10px"}}, questions[idx]["opt-text"]),
                html.textarea({"onchange":commentHandleChange,"placeholder":"Ingrese aquí sus comentarios.", "style":{"width":"70%", "height":"100px", "resize":"none"}}), html.br(), html.br(),
            )
        else:
            return html.br() #Retornar un salto de línea en caso de no haber necesidad de mostrar el cuadro de texto
    
        

    return html.section(
        html.h3(f"{questions[idx]["id"]} - {questions[idx]["text"]}"), html.br(),
        html.div({"style":{"font-size":"25px", "margin-left":"28px"}},
            html.label({"style":{"width":"30px"}},
                html.input({"value":1 if idx != 3 else 0,"onchange":radioHandleChange,"type":"radio", "name":str(idx+1)}), "Sí"), html.br(), html.br(),
            html.label({"style":{"width":"30px"}},
                html.input({"value":0 if idx != 3 else 1,"onchange":radioHandleChange,"type":"radio", "name":str(idx+1), "style":{"color":""}}), "No"), html.br(),
                Opinion_Text()
            
        )
    )

@component
def Open_Question(idx, onOpinionChange): #Componente de preguntas abiertas

    def opinionHandleChange(e):
        onOpinionChange(idx, e["target"]["value"])

    return html.section(
                html.h3(f"{questions[idx]["id"]} - {questions[idx]["text"]}"), html.br(),
                html.textarea({"onchange":opinionHandleChange,"placeholder":"Ingrese aquí sus opiniones.", "style":{"width":"70%", "height":"100px", "margin-left":"28px", "resize":"none"}}), html.br(), html.br()
            )

configure(app, App)