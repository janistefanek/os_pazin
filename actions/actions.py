import requests
import os
import random
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv

load_dotenv()

class ActionCallLlama(Action):
    def name(self) -> Text:
        return "action_call_llama"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '').lower()
        
        if "kviz" in user_message:
            kviz_pitanja = [
                {
                    "pitanje": "Tko je stvorio Pazinsku jamu prema legendi?",
                    "opcije": [{"title": "Div Dragonja", "payload": "Točno! Brao!"}, {"title": "Veli Jože", "payload": "Skoro, ali Dragonja je bio taj!"}]
                },
                {
                    "pitanje": "Koji je pisac opisao Pazin u romanu Mathias Sandorf?",
                    "opcije": [{"title": "Jules Verne", "payload": "Točno! On je naš počasni gost!"}, {"title": "August Šenoa", "payload": "On je pisao o drugima, ovdje je Verne glavni!"}]
                },
                {
                    "pitanje": "Koja je slastica zaštićeno dobro Pazina?",
                    "opcije": [{"title": "Pazinski cukerančić", "payload": "Tako je! Najslađa besida!"}, {"title": "Fritule", "payload": "Fritule su super, ali cukerančić je zaštićen!"}]
                }
            ]
            pitanje = random.choice(kviz_pitanja)
            dispatcher.utter_message(text=f"Ajmo provjeriti znanje! 🧠\n\n{pitanje['pitanje']}", buttons=pitanje['opcije'])
            return [] # Ovdje staje i NE IDE DALJE

        # --- 2. ZANIMLJIVOSTI (Samo ako NIJE kviz) ---
        elif any(word in user_message for word in ["zanimljivo", "zanimljivost", "besida"]):
            zanimljivosti = [
                {
                    "text": "Jesi li znao da je Jules Verne smjestio radnju svog romana 'Mathias Sandorf' baš u Pazin?",
                    "image": "https://thekhayal.com/wp-content/uploads/2023/09/Jules-Verne.webp"
                },
                {
                    "text": "Pazinska jama je duboka oko 100 metara, prava prirodna katedrala koju je po legendi stvorio div Dragonja!",
                    "image": "https://www.istra.hr/public/uploads/photos/articles/centralistria_8644-julienduval.jpg"
                },
                {
                    "text": "Pazinski cukerančić je zaštićena nematerijalna kulturna baština Istre i naš ponosan slatkiš!",
                    "image": "https://recepti-api.index.hr/img/preview/large/recipe/f9f29e85-7866-4434-86e7-76dcb50eb3ab/465368355_1084318740370945_8637085435809790018_n1.jpg"
                }
            ]
            izbor = random.choice(zanimljivosti)
            dispatcher.utter_message(text=f"Evo jedna besida: {izbor['text']}", image=izbor['image'])
            return []

        else:
            API_KEY = os.getenv("GROQ_API_KEY", "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")
            
            school_knowledge = """
                IDENTITET:
                Ti si službeni digitalni asistent Osnovne škole Pazin (OŠ Pazin). Tvoj zadatak je pomagati roditeljima, učenicima i posjetiteljima.
                
                OSOBNOST I STIL:
                - Budi srdačan, strpljiv i ponosan na našu školu i Pazin.
                - Govori na hrvatskom jeziku.
                - Na početku razgovora možeš reći 'Benvenuti' ili 'Dobar dan'.
                
                KLJUČNE ČINJENICE O ŠKOLI:
                - Ravnatelj: Ivan Štefanić.
                - Broj učenika: Ukupno 1289 (matična škola u Pazinu + 8 područnih škola).
                - Područne škole: Cerovlje, Gračišće, Karojba, Lupoglav, Motovun, Sv. Petar u Šumi, Tinjan i Trviž.
                - Glazbeni odjel: Nudimo poduku za klavir, harmoniku, violinu, gitaru, trubu, klarinet i udaraljke.
                
                UPUTE ZA ODGOVARANJE:
                - Ako te pitaju nešto općenito (npr. pomoć oko zadaće ili povijest), odgovaraj kao mudar školski asistent.
                - Ako ne znaš točan podatak o terminima ili ocjenama, uputi korisnika na tajništvo ili službenu web stranicu (www.os-vnazora-pazin.skole.hr).
                - Odgovori trebaju biti kratki (do 3 rečenice), osim ako korisnik ne traži duže objašnjenje.
                """

            prompt = f"{school_knowledge}\n\nKORISNIK PITA: {user_message}\n\nTVOJ ODGOVOR:"

            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    json={
                        "model": "llama-3.1-8b-instant",
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=10
                )
                response.raise_for_status()
                llama_response = response.json()['choices'][0]['message']['content']
                

                if any(x in llama_response.lower() for x in ["škola", "matična", "pazin"]):
                    dispatcher.utter_message(text=llama_response)
                else:
                    dispatcher.utter_message(text=llama_response)

            except Exception:
                dispatcher.utter_message(text="Ma nemoj mi zamirit, nešto me smelo. Probaj forši kasnije?")

            return []