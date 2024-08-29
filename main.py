import json
from copy import deepcopy
import statistics
from fastapi.staticfiles import StaticFiles
from reactpy import component, html, hooks
from reactpy.backend.fastapi import configure
from fastapi import FastAPI
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
with open("./content.json") as content: #Leer las preguntas desde el archivo JSON
    questions = json.load(content)

answers=[]
# current_answer={"id":1, "q1":0, "q2":0, "q3":0,"q4":0, "q4_comment":"", "q5":0, "q5_comment":"", "q6":0, "q6_comment":"", "q7":"","q8":""}

@component #Componente principal
def App():
    print(answers)
    current_answer, set_current_answer = hooks.use_state({"id":1})
    reset, set_reset = hooks.use_state(None)
    is_valid, set_is_valid = hooks.use_state(None)
    button_is_valid, set_button_is_valid = hooks.use_state(True)
    results, set_results = hooks.use_state(False)
    all_results, set_all_results = hooks.use_state(False)
    def handleRatingChange(idx, newRating): #Funciones que reciben y almacenan el valor de cada pregunta y lo almacenan en current_answer
        current_answer["q"+str((idx+1))] = int(newRating)


    def handleCommentChange(idx, newComment):
        current_answer["q"+str((idx+1))+"_comment"] = newComment


    def handleOpinionChange(idx, newOpinion):
        current_answer["q"+str((idx+1))] = newOpinion


    def formValidation(): #Validación para evitar que se envíe el formulario sin haber respondido las preguntas obligatorias
        sum = 0
        for i in range(len(questions)):
            v = list(current_answer.keys()).count("q"+str(i+1))
            sum += v
        if sum != 8:
            set_is_valid(False)
        else:
            set_is_valid(True)

    def handleSubmit(): #Función para guardar las respuestas en la lista answers y reiniciar el valor de current_answer
        formValidation()

        if is_valid:
            apply_answer = current_answer.copy()

            answers.append(apply_answer)
            
            
            set_current_answer({"id":current_answer["id"]+1})
            set_reset(True)
            set_button_is_valid(True)
        else:
            set_button_is_valid(False)
        return
    
    def handleGeneralReset(): #Función de reinicio general para volver a recoger respuestas
        set_reset(False)
        set_is_valid(None)
    def handleResultsPage(): #Función para salir de la página de resultados
        set_results(False)
        set_reset(False)
        set_is_valid(None)
    def handleAllResultsPage():
        if all_results == True:
            set_all_results(False)
            set_reset(None)
            set_is_valid(None)
            return
        set_results(False)
        set_all_results(True)
    
    
    if reset:
        if results:
            return ResultsPage(handleResultsPage, handleAllResultsPage)
        else:
            if all_results:
                return AllResultsPage(handleAllResultsPage)
            else:
                return html.div({}, #Contenedor general (body)
                    html.main ({ },
                        html.link({"rel": "stylesheet", "href": "/static/styles.css"}),
                        html.header( #Encabezado de la página
                        {},
                        html.h1("Encuesta de satisfacción del usuario")
                    ),
                    html.div({"class":"paragraph2"},
                    html.p({"class":"paragraph_item2"},"¡Felicidades! Has terminado de rellenar nuestra encuesta de satisfacción, tus opiniones son de gran importancia para nosotros. ¡Gracias! "),
                    html.img({"class":"imagen2","src":"/static/survey.png"})
                    ),
                    html.br(), html.br(),
                    html.h2("Decide si mirar los resultados de las encuestas o recoger otra respuesta: "),
                    html.br(), html.br(), html.br(), html.br(), html.br(),
                    html.section({"style":{"display":"flex", "flex-direction":"row"}},
                        html.button({"class":"button_1","on_click":lambda x: set_results(True)},"Mirar resultados 🔎"),
                        html.button({"class":"button_1","on_click":lambda x: handleGeneralReset()},"Recoger otra respuesta ✉"))
                    )
                    )
    else:
        return html.div({}, #Contenedor general (body)
            html.main({}, #Contenedor de la encuesta
                html.link({"rel": "stylesheet", "href": "/static/styles.css"}),
                html.header( #Encabezado de la página
                {},
                html.h1("Encuesta de satisfacción del usuario")
            ),
            html.div({"class":"paragraph"},
            html.p({"class":"paragraph_item"}, "Tu opinión es muy importante para nosotros, por lo tanto nos gustaría que respondas la siguiente encuesta de satisfacción. Gracias por usar nuestros servicios, usamos tus opiniones para mejorar cada día y ofrecer un mejor servicio."),
            html.img({"class":"tortica","src":"/static/tortica2.png"})
            ),
            html.h2("Selecciona la cantidad de estrellas en una calificación de 1 a 5"),
            html.nav( #Contenedor de las preguntas
                Star_Question(0, handleRatingChange, reset),
                Star_Question(1, handleRatingChange, reset),
                Star_Question(2, handleRatingChange, reset),
                Radio_Question(3, handleRatingChange, handleCommentChange, reset),
                Radio_Question(4, handleRatingChange, handleCommentChange, reset),
                Radio_Question(5, handleRatingChange, handleCommentChange, reset),
                Open_Question(6, handleOpinionChange, reset),
                Open_Question(7, handleOpinionChange, reset)
            ),
            html.button({"on_click":lambda x: handleSubmit()},"ENVIAR ✔" if button_is_valid else "¿ESTAS SEGURO?")
            ),
        )

@component
def Star_Question(idx, onRatingChange, isReset): #Componente de pregunta de estrellas
    rating, set_rating = hooks.use_state(0)
    not_selected = "https://i.ibb.co/RptMG5X/Tabler-Star-Uns.png"
    selected = "https://i.ibb.co/MPfkd9c/Tabler-Star.png"
    if isReset:
        set_rating(0)
    
    def handleStarClick(rating): #Función para establecer la calificación de la actual pregunta y pasarle el valor al componente App
        set_rating(rating)
        onRatingChange(idx, rating)
        
    return html.section( #Contenedor principal de la pregunta
        html.h3(f"{questions[idx]["id"]} - {questions[idx]["text"]}"), html.br(), #Número y texto de la pregunta
        html.article({}, #Contenedor de las estrellas
            html.div({"class":"estrellas"},
                html.img({"on_click":lambda x: handleStarClick(1),"src":not_selected if rating < 1 else selected, }),
                html.img({"src":"/static/muytriste.png"})    
            ),
            html.div({"class":"estrellas"},
                html.img({"on_click":lambda x: handleStarClick(2),"src":not_selected if rating < 2 else selected, }),
                html.img({"src":"/static/triste.png"}), 
            ),
            html.div({"class":"estrellas"},
                html.img({"on_click":lambda x: handleStarClick(3),"src":not_selected if rating < 3 else selected, }),
                html.img({"src":"/static/serio.png"}),
            ), 
            html.div({"class":"estrellas"},   
                html.img({"on_click":lambda x: handleStarClick(4),"src":not_selected if rating < 4 else selected, }),
                html.img({"src":"/static/feliz.png"}),
            ),
            html.div({"class":"estrellas"},    
                html.img({"on_click":lambda x: handleStarClick(5),"src":not_selected if rating < 5 else selected, }),
                html.img({"src":"/static/muyfeliz.png"}), 
            ),  
        ), html.br()
    )



@component
def Radio_Question(idx, onRadioChange, onCommentChange, isReset): #Componente de preguntas Sí/No
    radio_option, set_radio_option = hooks.use_state(None)
    comment, set_comment = hooks.use_state("")
    def radioHandleChange(e):#Callback para pasar valor al componente App
        set_radio_option(e["target"]["value"])
        onRadioChange(idx, e["target"]["value"])

    def commentHandleChange(e): #Callback para pasar cadena del comentario en caso de existir
        set_comment(e["target"]["value"])
        onCommentChange(idx, e["target"]["value"])

    def Opinion_Text(): #Función que genera el texto y el input de la opinión libre según el índice de la pregunta y la opción seleccionada
        

        if radio_option == "0" and not isReset:
            return html.section(
                html.h3({}, questions[idx]["opt-text"]), html.br(),
                html.textarea({"value":comment,"onchange":commentHandleChange,"placeholder":"Ingrese aquí sus comentarios.", }), html.br(), html.br(),
            )
        else:
            return html.br() #Retornar un salto de línea en caso de no haber necesidad de mostrar el cuadro de texto
    
        

    return html.section(
        html.h3(f"{questions[idx]["id"]} - {questions[idx]["text"]}"), html.br(),
        html.div({},
            html.label({},
                html.input({"value":5 if idx != 3 else 0,"onchange":radioHandleChange,"type":"radio", "name":str(idx+1), "checked":False if isReset else None}), "Sí"), html.br(), html.br(),
            html.label({},
                html.input({"value":0 if idx != 3 else 5,"onchange":radioHandleChange,"type":"radio", "name":str(idx+1), "checked":False if isReset else None}), "No"), html.br(),
                Opinion_Text()
            
        )
    )

@component
def Open_Question(idx, onOpinionChange, isReset): #Componente de preguntas abiertas
    opinion, set_opinion = hooks.use_state("")
    def opinionHandleChange(e):
        set_opinion(e["target"]["value"])
        onOpinionChange(idx, e["target"]["value"])

    return html.section(
                html.h3(f"{questions[idx]["id"]} - {questions[idx]["text"]}"), html.br(),
                html.textarea({"value":opinion if not isReset else "","onchange":opinionHandleChange,"placeholder":"Ingrese aquí sus opiniones.", }), html.br(), html.br()
            )

recommend_list = []
positive_experience_list = []
@component
def ResultsPage(onResultsChange, onAllResultsChange): #Componente de Página de resultados
    
    quality_answers = deepcopy(answers)
    quality_list = []
    for i in range(len(answers)): #Bucle para seleccionar únicamente las respuestas con valor para calificación de calidad y guardarlas en una lista
        if "id" in quality_answers[i].keys():
            del quality_answers[i]["id"]
        if "q2" in quality_answers[i].keys():
            del quality_answers[i]["q2"]
        if "q3" in quality_answers[i].keys():
            del quality_answers[i]["q3"]
        if "q7" in quality_answers[i].keys():
            del quality_answers[i]["q7"]
        if "q8" in quality_answers[i].keys():
            del quality_answers[i]["q8"]
        for j in list(quality_answers[i].values()):
            if type(j) != str:
                quality_list.append(j)
        
    quality_average = round(statistics.mean(quality_list), 2)

    recommend_answers = deepcopy(answers)
    recommend_list_element = []
    for i in range(len(answers)): #Bucle para seleccionar únicamente las respuestas con valor para calificación de calidad y guardarlas en una lista
        if "id" in recommend_answers[i].keys():
            del recommend_answers[i]["id"]
        if "q1" in recommend_answers[i].keys():
            del recommend_answers[i]["q1"]
        if "q3" in recommend_answers[i].keys():
            del recommend_answers[i]["q3"]
        if "q4" in recommend_answers[i].keys():
            del recommend_answers[i]["q4"]
        if "q7" in recommend_answers[i].keys():
            del recommend_answers[i]["q7"]
        if "q8" in recommend_answers[i].keys():
            del recommend_answers[i]["q8"]
    for j in list(recommend_answers[i].values()):
        if type(j) != str and j >= 3:
            recommend_list_element.append(j)
    if recommend_list_element and len(recommend_list_element) >= 2:
        recommend_list.append(recommend_list_element)
    

    recommends_percentage = round((len(recommend_list)/len(answers))*100, 1)
    
    #Experiencia general: Respuestas totales__. Experiencia general: Positiva: __ encuestados. Negativa: ___ encuestados.
    experience_answers = deepcopy(answers)
    positive_experience_list_element = []
    for i in range(len(answers)):
        if "id" in experience_answers[i].keys():
            del experience_answers[i]["id"]
        if "q7" in experience_answers[i].keys():
            del experience_answers[i]["q7"]
        if "q8" in experience_answers[i].keys():
            del experience_answers[i]["q8"]
    for j in list(experience_answers[i].values()):
        if type(j) != str and j >= 3:
            positive_experience_list_element.append(j)
    if positive_experience_list_element and len(positive_experience_list_element) >= 4:
        positive_experience_list.append(positive_experience_list_element)
    print(positive_experience_list)
    experience_percentage = round((len(positive_experience_list)/len(answers))*100,1)
        

            
    print(answers[0])
    


    
    return html.div({}, #Contenedor general (body)
                html.main({},
                    html.link({"rel": "stylesheet", "href": "/static/styles.css"}),
                    html.header( #Encabezado de la página
                    html.h1("Encuesta de satisfacción del usuario"),
                    
                ),
                html.div({"class":"paragraph3"},
                html.p({"class":"paragraph_item3"},"En esta sección podrás consultar el promedio de los resultados recogidos y mirar todas las respuestas recopiladas"),
                html.img({"class":"imagen3","src":"/static/analisis.png"})
                ),
                html.br(), html.br(),
                html.div({"class":"tabla"},
                    html.h5("Calificación de calidad del producto: "),
                    html.h6(f"Promedio: {quality_average}"),
                    html.br({"class":"raya"}),
                    html.h5("Índice de recomendación del producto: "),
                    html.h6(f"Porcentaje: {recommends_percentage}%"),
                    html.h6({}, f"{len(recommend_list)}/{len(answers)} encuestados recomiendan el producto"),
                    html.br({"class":"raya"}),
                    html.h5("Calificación de experiencia general de los usuarios con el producto: "),
                    html.h6(f"Cantidad total de encuestados: {len(answers)}"),
                    html.br({"class":"raya"}),
                    html.h5("Experiencia general:"),
                    html.h6(f"Positiva: {len(positive_experience_list)} encuestado/s"),
                    html.h6(f"Negativa {len(answers)-len(positive_experience_list)} encuestado/s"),
                    html.br({"class":"raya"}),
                    html.h5("Porcentaje general de satisfacción de los encuestados: "),
                    html.h6(f"{experience_percentage}%"),
                ),
                html.br(), html.br(), html.br(), html.br(),
                html.section({"style":{"display":"flex", "flex-direction":"row"}},
                    html.button({"class":"button_1", "on_click":lambda x: onResultsChange(), },"Recoger otra respuesta ✉"),
                    html.button({"class":"button_1", "on_click":lambda x: onAllResultsChange(), },"Ver todas las respuestas ↗")
                )
                
                )
                )
    

comments_list = []
@component
def QuestionsAndAnswers(answers_for_user):
    return html.section(
        *map(lambda question: html.div(
            html.h3(f"{question["id"]}. {question["text"]}"),
            html.h4(f"Calificación: {answers_for_user["q"+str(question["id"])]}")
            ), questions)
        
    )



def AllResultsPage(onAllResultsChange):
    return html.div({}, #Contenedor general (body)
                html.main({},
                    html.link({"rel": "stylesheet", "href": "/static/styles.css"}),
                    html.header( #Encabezado de la página
                    html.h1("Encuesta de satisfacción del usuario"),
                   #coso 
                ),
                html.p(),
                html.ul({},
                *map(lambda answer: html.li({"key":answer["id"]},
                    html.h2(f"ENCUESTADO #{answer["id"]}"),
                    QuestionsAndAnswers(answer),
                    
                    *(html.h4(comment) for comment in [
                    "Comentarios:",
                    answer.get('q4_comment'), 
                    answer.get('q5_comment'), 
                    answer.get('q6_comment')
                    ] if comment),
                    html.br(), html.br()
                ), answers)),
                html.button({"on_click":lambda x: onAllResultsChange(), },"Recoger otra respuesta ✉")
                )
                )
configure(app, App)