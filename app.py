import json
import streamlit as st
from openai import OpenAI


st.set_page_config(
    page_title="Générateur TikTok & Shorts",
    page_icon="🎬",
    layout="wide"
)


st.title("🎬 Générateur de scripts TikTok & YouTube Shorts")
st.caption("Scripts verticaux 9:16 avec accroche, rétention et instructions de montage")


# Récupération sécurisée de la clé API
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    api_key = ""

if not api_key:
    st.error("La clé OPENAI_API_KEY n'est pas encore configurée dans Streamlit.")
    st.stop()

client = OpenAI(api_key=api_key)


with st.sidebar:
    st.header("Paramètres")

    plateforme = st.selectbox(
        "Plateforme",
        [
            "TikTok",
            "YouTube Shorts",
            "TikTok et YouTube Shorts"
        ]
    )

    durée = st.selectbox(
        "Durée",
        [
            "15 secondes",
            "30 secondes",
            "45 secondes",
            "60 secondes"
        ]
    )

    ton = st.selectbox(
        "Ton",
        [
            "Dynamique",
            "Provocateur",
            "Éducatif",
            "Storytelling",
            "Humoristique",
            "Inspirant",
            "Expert"
        ]
    )

    nombre = st.slider(
        "Nombre de scripts",
        min_value=1,
        max_value=5,
        value=3
    )


sujet = st.text_area(
    "Sujet de la vidéo",
    placeholder="Exemple : 5 erreurs qui empêchent de réussir sur TikTok",
    height=100
)

audience = st.text_input(
    "Audience cible",
    placeholder="Exemple : entrepreneurs débutants de 18 à 35 ans"
)

objectif = st.selectbox(
    "Objectif principal",
    [
        "Obtenir des commentaires",
        "Augmenter les abonnements",
        "Faire découvrir une information",
        "Vendre un produit",
        "Créer une vidéo virale",
        "Construire de l'autorité"
    ]
)

style_montage = st.selectbox(
    "Style de montage",
    [
        "Face caméra rapide",
        "Voix off avec images B-roll",
        "Storytelling cinématique",
        "Montage très dynamique",
        "Écran partagé",
        "Style podcast vertical"
    ]
)

instructions = st.text_area(
    "Instructions supplémentaires",
    placeholder="Exemple : utilise un langage simple et ajoute une fin surprenante.",
    height=100
)


def generer_scripts():
    prompt = f"""
Tu es un expert en écriture virale pour TikTok et YouTube Shorts.

Génère {nombre} scripts originaux sur le sujet suivant :

SUJET :
{sujet}

AUDIENCE :
{audience}

PLATEFORME :
{plateforme}

DURÉE :
{durée}

TON :
{ton}

OBJECTIF :
{objectif}

STYLE DE MONTAGE :
{style_montage}

INSTRUCTIONS SUPPLÉMENTAIRES :
{instructions}

Contraintes obligatoires :

- Format exclusivement vertical 9:16.
- Le script doit être adapté à TikTok et YouTube Shorts.
- L'accroche doit être très forte dans les 2 premières secondes.
- Aucune introduction lente ou formule de politesse.
- Utilise des phrases courtes et naturelles.
- Prévois une relance de curiosité toutes les 3 à 5 secondes.
- Le contenu doit être compréhensible même sans le son.
- Ajoute des sous-titres courts et lisibles.
- Prévois des changements visuels fréquents.
- Les textes importants doivent rester dans la zone centrale de l'écran.
- La conclusion doit contenir un appel à l'action.
- Les scripts doivent être originaux et ne pas copier de créateurs existants.

Retourne uniquement un JSON valide avec cette structure :

{{
  "scripts": [
    {{
      "titre": "",
      "angle": "",
      "accroche": "",
      "promesse": "",
      "score_accroche": 0,
      "score_retention": 0,
      "voix_off_complete": "",
      "mecanismes_retention": [],
      "plan_montage": [
        {{
          "timecode": "",
          "voix_off": "",
          "visuel": "",
          "cadrage": "",
          "texte_ecran": "",
          "sous_titres": "",
          "transition": "",
          "son": ""
        }}
      ],
      "appel_action": "",
      "description": "",
      "hashtags": []
    }}
  ]
}}
"""

    réponse = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.9,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "Tu réponds uniquement avec un JSON valide."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return json.loads(réponse.choices[0].message.content)


if st.button("🚀 Générer les scripts", type="primary", use_container_width=True):
    if not sujet.strip():
        st.warning("Indique d'abord le sujet de la vidéo.")
        st.stop()

    with st.spinner("Création des scripts verticaux..."):
        résultat = generer_scripts()

    for index, script in enumerate(résultat["scripts"], start=1):
        st.divider()

        st.header(f"Script {index} — {script['titre']}")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Force de l'accroche",
                f"{script['score_accroche']}/100"
            )

        with col2:
            st.metric(
                "Potentiel de rétention",
                f"{script['score_retention']}/100"
            )

        st.subheader("🎯 Accroche")
        st.success(script["accroche"])

        st.subheader("💡 Promesse")
        st.write(script["promesse"])

        st.subheader("🎙️ Voix off complète")
        st.text_area(
            "Script",
            script["voix_off_complete"],
            height=220,
            key=f"voix_off_{index}"
        )

        st.subheader("🧠 Mécanismes de rétention")
        for élément in script["mecanismes_retention"]:
            st.write(f"• {élément}")

        st.subheader("✂️ Plan de montage vertical")

        for scène in script["plan_montage"]:
            with st.expander(
                f"{scène['timecode']} — {scène['visuel']}"
            ):
                st.write(f"**Voix off :** {scène['voix_off']}")
                st.write(f"**Cadrage :** {scène['cadrage']}")
                st.write(f"**Texte à l'écran :** {scène['texte_ecran']}")
                st.write(f"**Sous-titres :** {scène['sous_titres']}")
                st.write(f"**Transition :** {scène['transition']}")
                st.write(f"**Son :** {scène['son']}")

        st.subheader("📢 Appel à l'action")
        st.info(script["appel_action"])

        st.subheader("🏷️ Description et hashtags")
        st.write(script["description"])
        st.write(" ".join(script["hashtags"]))

    st.download_button(
        "⬇️ Télécharger les scripts en JSON",
        data=json.dumps(résultat, ensure_ascii=False, indent=2),
        file_name="scripts_tiktok_shorts.json",
        mime="application/json",
        use_container_width=True
    )
