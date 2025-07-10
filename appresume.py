import os
from flask import Flask, request, jsonify
from google import genai
from google.genai import types
import base64

app = Flask(__name__)

# Initialize the GenAI client once globally to avoid re-initializing on every request
client = genai.Client(
    vertexai=True,
    project="caramel-park-464411-n6",
    location="global",
)

@app.route('/analyze_financial_data', methods=['POST'])
def analyze_financial_data():
    """
    API endpoint to receive financial data via POST request and analyze it using GenAI.
    """
    try:
        # Get JSON data from the POST request
        data = request.get_json()

        if not data or 'inputText' not in data:
            return jsonify({"error": "Missing 'inputText' in request body"}), 400

        input_text = data['inputText']

        si_text1 = f"""En tant qu'analyste long short sur les marchés financiers, base toi sur tout l'information actuelle a partir d'aujourd'hui disponible à ta portée. Pondère celle ci à 40% dans le modèle. Base toi en suite sur le texte à analyser ci dessous suivant basé sur les nouvelles de hier que tu vas pondéré à 60% en poids de celle ci dans ton résultat

Texte à analyser :

{input_text}

Sur base de ce contenu, peux tu me faire un résumé global en 15 lignes maximum des marchés financier US et EU et conseille moi de manière très rigoureuse pour du trading intraday/Hebdomadaire (comme si t'as vie en dépendait) un turbo long existant aujourd'hui et emis par BNP ainsi qu'un turbo short aujourd'hui et emis par BNP. Explique moi de manières détaillés et précise (en moins de deux lignes) tes convictions qui poussent à ce résultat. 


Formate ta réponse :
---
🧠 Résumé macro (4 lignes max) :

 
💥 Achat Turbo 

Une position Turbo long (produits fournis par BNP Paribas) selectionné par ton choix: Code isin et description
Une position short (produits fournis par BNP Paribas) déterminé par ton choix: Code isin et description"""

        model = "gemini-2.5-flash"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text="si_text1")
                ]
            )
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=1,
            seed=0,
            max_output_tokens=65535,
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")
            ],
            system_instruction=[types.Part.from_text(text=si_text1)],
            thinking_config=types.ThinkingConfig(
                thinking_budget=-1,
            ),
        )

        full_response = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            full_response += chunk.text

        return jsonify({"analysis": full_response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    # Récupère le port de l'environnement, par défaut 8080 si non défini (pour les tests locaux)
    port = int(os.environ.get("PORT", 8080))
    # Démarre l'application Flask
    app.run(host="0.0.0.0", port=port, debug=False)
