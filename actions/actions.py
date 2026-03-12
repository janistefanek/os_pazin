import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionCallLlama(Action):
    def name(self) -> Text:
        return "action_call_llama"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '')
        
        # Ovdje stavi svoj besplatni API ključ s console.groq.com
        API_KEY = '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'
        
        prompt = f"""Ti si asistent Osnovne škole Pazin (OŠ Pazin). 
        Odgovaraj na hrvatskom jeziku, budi pristojan, kratak i koristan.
        Ako ne znaš odgovor, reci korisniku da kontaktira tajništvo škole.
        Korisnik pita: {user_message}"""

        if API_KEY == "gsk_...wzRc":
            dispatcher.utter_message(text="Za pametne odgovore, molim administratora da unese Groq API ključ u actions.py! 😅")
            return []

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
            dispatcher.utter_message(text=llama_response)
        except Exception as e:
            dispatcher.utter_message(text="Nažalost, trenutno ne mogu provjeriti tu informaciju. Obratite se tajništvu.")

        return []