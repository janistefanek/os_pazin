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
        
        # --- 1. KVIZ LOGIKA ---
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

        if "kviz" in user_message:
            pitanje = random.choice(kviz_pitanja)
            dispatcher.utter_message(text=f"Ajmo provjeriti znanje! 🧠\n\n{pitanje['pitanje']}", buttons=pitanje['opcije'])
            return []

        # --- 2. ZANIMLJIVOSTI ---
        zanimljivosti = [
            "Jesi li znao da je Jules Verne smjestio radnju svog romana 'Mathias Sandorf' baš u Pazin?",
            "Pazinska jama je duboka oko 100 metara, prava prirodna katedrala!",
            "Pazinski cukerančić je zaštićena nematerijalna kulturna baština.",
            "Naša škola ima čak 8 područnih škola po cijeloj središnjoj Istri!"
        ]
        
        if any(word in user_message for word in ["zanimljivo", "zanimljivost", "besida"]):
            fact = random.choice(zanimljivosti)
            dispatcher.utter_message(text=f"Evo jedna zanimljivost: {fact}")
            return []

        # --- 3. LLM DIO (Llama) ---
        API_KEY = os.getenv("GROQ_API_KEY", "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")
        
        school_knowledge = """
        Ti si asistent OŠ Pazin. Povremeno ubaci istarske riječi: 'hiža', 'besida', 'ca delaš', 'forši'.
        Ravnatelj je Ivan Štefanić. Imamo 8 područnih škola i 1289 učenika.
        """

        prompt = f"{school_knowledge}\nKorisnik pita: {user_message}\nOdgovori kratko i srdačno."

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
            
            # Dinamičke slike
            msg_lower = llama_response.lower()
            if "pazin" in msg_lower and "škola" in msg_lower:
                dispatcher.utter_message(text=llama_response, image="https://os-vnazora-pazin.skole.hr/images/skola_naslovna.jpg")
            else:
                dispatcher.utter_message(text=llama_response)

        except Exception:
            dispatcher.utter_message(text="Ma nemoj mi zamirit, nešto me smelo. Probaj forši kasnije?")

        return []