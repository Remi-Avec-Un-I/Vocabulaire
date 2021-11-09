from randomdict import RandomDict #https://github.com/robtandy/randomdict
from googletrans import Translator
import PySimpleGUI as sg
import json, os, random, webbrowser, googletrans

from os import system, walk
from PySimpleGUI.PySimpleGUI import P

try:        #trying to load theme string
    with open(r"./parametres/theme.json", 'r') as file:
        settings = json.load(file)
    theme = settings['themejson']
except:
    theme = 'BluePurple'

try:        #trying to load icon string
    with open(r"./parametres/icon.json", 'r') as file:
        settings = json.load(file)
    icon = settings['icon']
except:
    icon = 'default'

try:        # try if google trans as the good version that work, if not download it
    translator = Translator()
    translated_text = translator.translate("test", src='fr', dest ='en')
except:
    system("pip3 uninstall  --yes googletrans")
    system("pip3 install googletrans==4.0.0rc1")
    
def create_json(name):
    open(f"./parametres/{name}.json", "a+").close() # pour creer le json s'il existe pas
#

def text_over_input(text, input_size, inputText, key=None):
    return sg.Column([[sg.Text(text, pad=(0,3), key=key)], [sg.Input(inputText, size=(input_size,1), pad=(0,0))]], pad=(0,3))
#

def translate(text, src="auto", dest="fr"):
    return translator.translate(text, src=src, dest=dest).text
#

def main(path: str, theme: str, icon: str):
    
    def exemple(theme: str, icon: str):
        print("yes")
        sg.theme(f"{theme}")
        layout=[
            [sg.Text(f"Voici un exemple du theme : {theme}")],
            [sg.Button("Quitter")]
        ]
        window = sg.Window("Exemple", layout, size=(360, 200), icon=icon)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Quitter":
                break
        window.close()
#
        
    def settings(theme: str, icon: str):

        print(theme)                      
        sg.theme(f"{theme}")
        
        ico = []
        for root, directories, file in walk(r"./parametres"):
            for file in file:
                if file.endswith('.ico'):
                    ico.append(file[:-4])
        
        layout = [
            [sg.Text("Theme :"), sg.Combo(values = sg.theme_list(), key="-List-", enable_events=True), sg.Button("Essayer")],
            [sg.T("Changer l'icône :"), sg.Combo(ico, enable_events=True, key="-Combo-"), sg.B("Aide"), sg.I(enable_events=True, visible=False, key='-Fe-'), sg.FileBrowse("Ajouter", target='-Fe-', initial_folder=(r"./parametres"))],
            [sg.Text("Il faut telecharger un fichier en .ico trouvable sur https://icon-icons.com par exemple.\nPuis les mettres dans le dossier parametres, et le selectionner avec le déroulé au dessus.", enable_events=True, key="-URL-", visible=False)],
            [sg.Button("Appliquer")]
        ]
        
        window = sg.Window("Parametres", layout, size=(720, 400), icon=icon)
        while True:
                
            event, values = window.read()
            
            if event == sg.WIN_CLOSED or event == "Fermer":
                break
            
            elif event == 'Essayer':
                if len(values["-Combo-"]):
                    print('no')
                    break
                else:
                    print("yes")
                    exemple(values["-List-"], icon)
            
            elif event == "Appliquer":
                actualiser = 0
                if len(values["-List-"]) == 0:
                    pass
                else:
                    create_json(name="theme")
                    actualiser += 1
                    dict = {"themejson" : values['-List-']}
                    with open("./parametres/theme.json", 'w') as file:
                        json.dump(dict, file, indent=4)

                if len(values["-Combo-"]) == 0:
                    pass
                else:
                    actualiser += 1
                    create_json(name="icon")
                    dict = {"icon" : f"./parametres/{values['-Combo-']}.ico"}
                    with open("./parametres/icon.json", 'w') as file:
                        json.dump(dict, file, indent=4)
                
                if actualiser != 0:
                    try:
                        system("py " + os.path.basename(__file__))
                    except:
                        system(os.path.basename(__file__))
                    system("taskkill /F /im python.exe")
                    
            elif event == "Aide":
                window["-URL-"].update(visible=True)
            
            elif event == "-URL-":
                webbrowser.open("https://icon-icons.com")
                
            elif event == "-Combo-":
                icon = {"icon" : values["-Combo-"] + ".ico"}
#


    def supprLangue(theme: str, icon: str):
        
        sg.theme(f"{theme}")
        
        layout = [[sg.Text("Choissisez la langue a supprimer :", justification='center', size=(100,1))]]
        for jsonLangue in langue:
            layout = [layout, [sg.Button(jsonLangue)]]
        layout = [layout, [sg.Button("Fermer", button_color='red')]]
        
        window = sg.Window("Supprimer une langue", layout, element_justification='c' ,size=(720, 400), icon=icon)
        
        while True:
            
            event, values = window.read()
            
            if event == sg.WIN_CLOSED or event == "Fermer":
                break
        
            elif event in langue:
                demande(event, theme, icon)
        window.close()
#
    
    def demande(langue, theme: str, icon: str):
        sg.theme(f"{theme}")
        layout = [[sg.T(f"Es-tu sûr  de vouloir surrpimer '{langue}' ?")], [sg.B("Oui", button_color='green'), sg.B("Non", button_color='red')]]
        window = sg.Window("Supprimer une langue", layout, element_justification='c' ,size=(360, 200), icon=icon)
        while True:  
            event, values = window.read()
            
            if event == sg.WIN_CLOSED or event == "Non":
                break
            elif event == "Oui":
                os.remove(f"./langue/{langue}.json")
                break
        window.close()
#
        
    def wndLangue(langue: list, theme: str, icon: str):
        
        sg.theme(f"{theme}")
            
        layout = [
            [sg.Button("Réviser")],
            [sg.Button("Commencer le test !")],
            [sg.Button("Ajouter du vocabulaire")]
        ]
        
        window = sg.Window(langue, layout, element_justification='c' ,size=(720, 400), icon=icon)
        
        while True:
            
            event, values = window.read()
            
            if event == sg.WIN_CLOSED:
                break
            
            elif event == "Commencer le test !":
                test(langue, theme, point=0, old=(), icon=icon)
            
            elif event == "Ajouter du vocabulaire":
                vocabulaire(langue, theme, icon)
            
            elif event == "Réviser":
                reviser(langue, theme, old=(), icon=icon)
# 
    
    def reviser(langue, theme: str, old: tuple, icon: str):
        sg.theme(f"{theme}")
        with open(f"./langue/{langue}.json", "r") as file:
            data = json.load(file)
    
        data = RandomDict(data)
        D = data.random_item()
        print(D, old)
        while D[0] in old:
            D = data.random_item()
        old = ()
        cols = (("En français" ,40 , D[0]), (f"En {langue}",40 , D[1]))
        layout = [
            [*[text_over_input(*col) for col in cols],sg.Column([[sg.Text(pad=(0,0))],[sg.B('Continuer', pad=(0,0))]])]
        ]
        window = sg.Window("Réviser", layout, size=(720, 400), icon=icon)
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == "Quitter":
                break

            elif event == "Continuer":
                window.close()
                reviser(langue, theme, old=old+D, icon=icon)
#
        
    def test(langue, theme: str, old: tuple, point: int, icon: str):
        
        sg.theme(f"{theme}")
        
        with open(f"./langue/{langue}.json", "r") as file:
            data = json.load(file)
        
        data = RandomDict(data)
        D = data.random_item()
        while D[0] in old:
            D = data.random_item()
        old = ()
        if random.randint(0, 2) == 0:
            cols = (("En français" ,40 , D[0] ), (f"En {langue}",40 , ""))
        else:
            cols = (("En français" ,40 , "" ), (f"En {langue}",40 , D[1]))
        
        layout = [
            [*[text_over_input(*col) for col in cols],sg.Column([[sg.Text(pad=(0,0))],[sg.B('Valider', pad=(0,0)), sg.B("Quitter", pad=(3,0))]])],
            [sg.Button("J'avais juste !", visible=False), sg.Text("Juste", key="-Reponse-", text_color='green', visible=False)],
            [sg.Text(f"Vous avez {point} point(s)", key='-point-', visible=False), sg.Button("Continuer", key='-continuer-', visible=False)]
        ]
        window = sg.Window("Test", layout, size=(720, 400), icon=icon)
        while True:
            event, values = window.read()
            
            if event == sg.WIN_CLOSED or event == "Quitter":
                break
            
            elif event == "Valider":
                window['-continuer-'].update(visible=True)
                if f"('{values[0]}', '{values[1]}')" == str(D):
                    point += 1
                    window['-Reponse-'].update(visible=True)
                    window['-point-'].update(f"Vous avez {point} point(s)", visible=True)
                else:
                    window['-Reponse-'].update(f"Faux ! La réponses était {D[0]} -> {D[1]}", visible=True)
                    window["J'avais juste !"].update(visible=True)
                    window['-point-'].update(visible=True)
                while True:
                    event, values = window.read()
                    if event == sg.WIN_CLOSED or event == "Quitter":
                        break
                    elif event == "J'avais juste !":
                        point+=1
                        window["J'avais juste !"].update(visible=False)
                        window['-point-'].update(f"Vous avez {point} point(s)")
                    elif event == '-continuer-':
                        window.close()
                        test(langue, theme, old=old+D, point=point, icon=icon)
        window.close()
#
        
    def vocabulaire(langue: list, theme: str, icon: str):
        
        sg.theme(f"{theme}")
        cols = (("En français" ,40 , "" ), (f"En {langue}",40 , ""))
        layout = [
            [*[text_over_input(*col) for col in cols],sg.Column([[sg.Text(pad=(0,0))]])],
            [sg.Button("Ajouter"), sg.Button("Aide")],
            [sg.Text("Il faut mettre dans la case 'Terme en Français' le mots ou expression en français, et dans l'autre la traduction.\n Si vous mettez une expression qui est deja defini elle va etre remplacé.", text_color='red', key='-aide-', visible=False)]
        ]
        
        window = sg.Window("Vocabulaire", layout, element_justification='c',size=(720, 400), icon=icon)
        
        while True:
            event, values = window.read()
            
            if event == sg.WIN_CLOSED:
                break
            
            elif event == "Ajouter":
                
                with open(f"./langue/{langue}.json", "r") as file:
                    try:
                        data = json.load(file)
                    except:
                        data = {}
                    entry = {values[0] : values[1]}
                    data.update(entry)
                    
                with open(f"./langue/{langue}.json", "w") as file:
                    json.dump(data, file, indent=4)
            
            elif event == "Aide":
                window['-aide-'].update(visible=True)
#        
    def googleTrad(theme: str, icon: str):
        sg.theme(f"{theme}")
        
        cols = (("En français" ,40 , "", "-fr-"), ("En _____",40 , "", "-lang-"))
        languages = list(googletrans.LANGUAGES.values())
        layout = [
            [sg.Combo(languages, key="-Clang-")],
            [*[text_over_input(*col) for col in cols],sg.Column([[sg.Text(pad=(0,0))]])],
            [sg.Button("Traduire")]
        ]
        
        window = sg.Window("Vocabulaire", layout, element_justification='c', size=(720, 400), icon=icon)

        while True:
            
            event, values = window.read()
            
            if event == sg.WIN_CLOSED:
                break
                
            elif event == "Traduire":
                if len(values["-Clang-"]) != 0:
                    newLangue = values["-Clang-"]
                    window["-lang-"].update(f"En {newLangue}")
                    try:
                        for key,value in googletrans.LANGUAGES.items():
                            if value == newLangue:
                                toInput = translator.translate(values[0], src='fr', dest=key)
                        toInput = toInput.text
                        window[1].update(toInput)
                    except:
                        pass
                else:
                    pass

            
        window.close()
    
    #########################        
    langue = []
        
    for root, directories, file in walk(path):
        for file in file:
            if file.endswith('.json'):
                langue.append(file[:-5])
                
    
    layoutLangue = [[sg.Text("Choissisez la langue :", justification='center', size=(100,1))]]
    for jsonLangue in langue:
        layoutLangue = [layoutLangue, [sg.Button(jsonLangue)]]
    jsonLangue = langue
    
    layout = layoutLangue + [
        [sg.Text("Ajouter une langue (pas de guillet ou la langue ne marchera plus) :", justification='center',size=(100,1))], [sg.Input()],
        [sg.Button("Ajouter"), sg.Button("Actualiser"), sg.Button("Fermer")],
        [sg.Button("Google traduction")],
        [sg.Button("Supprimer une langue")],
        [sg.Button("Parametres")]
    ]
    
    sg.theme(f"{theme}")
    window = sg.Window("Vocabulaire", layout, element_justification='c', size=(720, 400), icon=icon)


    while True:
        
        event, values = window.read()
        
        if event in langue:
            wndLangue(event, theme, icon)
            
        if event == "Fermer" or event == sg.WIN_CLOSED:
            system("taskkill /im python.exe")
            break
        
        elif event == "Actualiser":
            window.close()
            try:
                system("py " + os.path.basename(__file__))
            except:
                system(os.path.basename(__file__))
        
        elif event == "Ajouter":
            try:
                os.mkdir("langue")
            except:
                pass
            file = path + "/" + values[0] + ".json"
            open(file, "a+").close()
            print("Création de", file)
        
        elif event == "Supprimer une langue":
            supprLangue(theme, icon)
        
        elif event == "Parametres":
            settings(theme, icon)
            
        elif event == "Google traduction":
            googleTrad(theme, icon)
            
    window.close()

main(path=r'./langue', theme=str(theme), icon=icon)