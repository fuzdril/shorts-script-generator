import json
import streamlit as st
from openai import OpenAI


# =========================
# Configuration de la page
# =========================

st.set_page_config(
    page_title="Générateur TikTok & Shorts",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Générateur de scripts TikTok & YouTube Shorts")
st.caption(
    "Scripts verticaux 9:16 avec accroche, rétention et instructions de montage"
)


# =========================
# Clé API OpenAI
# =========================

try:
    api_key = st.secrets["OPENAI_API_KEY"].strip()
except Exception:
    api_key = ""

if not api_key:
    st.error(
        "La clé OPENAI_API_KEY n'est pas configurée dans les secrets Streamlit."
    )
    st.stop()

client = OpenAI(api_key=api_key)


# =========================
# Paramètres
# =========================

with st.sidebar:
    st.header("⚙️ Paramètres")

    plateforme = st.selectbox(
        "Plateforme",
        [
            "TikTok",
            "YouTube Shorts",
            "TikTok et YouTube Shorts"
        ]
    )

    duree = st.selectbox(
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
        "Plus de commentaires",
        "Plus d'abonnement",
        "Plus de like",
        "Plus de vue",
        "Plus de follow sur Twitch",
        "Vidéo qui perce"
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


# =========================
# Consignes selon l'objectif
# =========================

CONSIGNES_OBJECTIF = {
    "Plus de commentaires": """
- Termine par une question ouverte.
- Encourage les opinions, débats et expériences personnelles.
- Utilise une phrase comme : "Tu en penses quoi ?".
- Le CTA principal doit demander de commenter.
""",

    "Plus d'abonnement": """
- Donne une raison claire de s'abonner.
- Crée une promesse de contenu futur.
- Termine par un CTA demandant de s'abonner.
- Fais comprendre que d'autres vidéos similaires vont suivre.
""",

    "Plus de like": """
- Utilise une émotion forte : surprise, humour, inspiration ou identification.
- Ajoute un moment mémorable ou facilement partageable.
- Termine par un CTA demandant de liker la vidéo.
""",

    "Plus de vue": """
- Utilise une accroche très forte dans les 2 premières secondes.
- Crée de la curiosité dès le début.
- Maintiens un rythme rapide.
- Révèle l'information principale vers la fin.
""",

    "Plus de follow sur Twitch": """
- Oriente clairement le contenu vers Twitch.
- Donne une raison concrète de suivre la chaîne Twitch.
- Mets en avant les lives, moments exclusifs ou interactions en direct.
- Termine par un CTA demandant de follow sur Twitch.
""",

    "Vidéo qui perce": """
- Combine curiosité, émotion, rythme rapide et surprise.
- Utilise une structure facilement partageable.
- Prévois plusieurs changements visuels.
- Crée une révélation ou un retournement final.
- Optimise l'accroche, la rétention et le CTA.
"""
}


# =========================
# Génération des scripts
# =========================

def generer_scripts():
    consignes_objectif = CONSIGNES_OBJECTIF[objectif]

    prompt = f"""
Tu es un expert en écriture virale pour TikTok et YouTube Shorts.

Génère exactement {nombre} scripts originaux sur le sujet suivant.

SUJET :
{sujet}

AUDIENCE :
{audience or "Grand public"}

PLATEFORME :
{plateforme}

DURÉE :
{duree}

TON :
{ton}

OBJECTIF PRINCIPAL :
{objectif}

CONSIGNES SPÉCIFIQUES À L'OBJECTIF :
{consignes_objectif}

STYLE DE MONTAGE :
{style_montage}

INSTRUCTIONS SUPPLÉMENTAIRES :
{instructions or "Aucune"}

Le script doit être entièrement construit pour atteindre l'objectif sélectionné.
L'accroche, la structure, le rythme, les visuels et l'appel à l'action
doivent tous servir cet objectif.

Contraintes obligatoires :

- Format vertical 9:16.
- Adapté à TikTok et YouTube Shorts.
- Accroche forte dans les 2 premières secondes.
- Aucune introduction lente.
- Phrases courtes et naturelles.
- Relance de curiosité toutes les 3 à 5 secondes.
- Compréhensible même sans le son.
- Sous-titres courts et lisibles.
- Changements visuels fréquents.
- Textes importants placés dans la zone centrale.
- Appel à l'action cohérent avec l'objectif.
- Scripts originaux.
- Ne copie aucun créateur existant.

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

    try:
        reponse = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.9,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es un expert en scripts courts. "
                        "Tu réponds uniquement avec un JSON valide."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        contenu = reponse.choices[0].message.content

        if not contenu:
            raise ValueError("La réponse de l'API est vide.")

        resultat = json.loads(contenu)

        if "scripts" not in resultat:
            raise ValueError("Le JSON ne contient pas la clé 'scripts'.")

        return resultat

    except json.JSONDecodeError:
        st.error("L'IA n'a pas retourné un JSON valide.")
        st.stop()

    except Exception as erreur:
        st.error(f"Erreur lors de la génération : {erreur}")
        st.stop()


# =========================
# Affichage des résultats
# =========================

if st.button(
    "🚀 Générer les scripts",
    type="primary",
    use_container_width=True
):

    if not sujet.strip():
        st.warning("Indique d'abord le sujet de la vidéo.")
        st.stop()

    with st.spinner("Création des scripts verticaux..."):
        resultat = generer_scripts()

    for index, script in enumerate(resultat["scripts"], start=1):
        st.divider()

        titre = script.get("titre", f"Script {index}")

        st.header(f"Script {index} — {titre}")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Force de l'accroche",
                f"{script.get('score_accroche', 0)}/100"
            )

        with col2:
            st.metric(
                "Potentiel de rétention",
                f"{script.get('score_retention', 0)}/100"
            )

        st.subheader("🎯 Accroche")
        st.success(script.get("accroche", ""))

        st.subheader("💡 Promesse")
        st.write(script.get("promesse", ""))

        st.subheader("🎙️ Voix off complète")
        st.text_area(
            "Script",
            script.get("voix_off_complete", ""),
            height=220,
            key=f"voix_off_{index}"
        )

        st.subheader("🧠 Mécanismes de rétention")

        for element in script.get("mecanismes_retention", []):
            st.write(f"• {element}")

        st.subheader("✂️ Plan de montage vertical")

        for scene in script.get("plan_montage", []):
            with st.expander(
                f"{scene.get('timecode', '')} — {scene.get('visuel', '')}"
            ):
                st.write(f"**Voix off :** {scene.get('voix_off', '')}")
                st.write(f"**Cadrage :** {scene.get('cadrage', '')}")
                st.write(
                    f"**Texte à l'écran :** "
                    f"{scene.get('texte_ecran', '')}"
                )
                st.write(
                    f"**Sous-titres :** "
                    f"{scene.get('sous_titres', '')}"
                )
                st.write(
                    f"**Transition :** "
                    f"{scene.get('transition', '')}"
                )
                st.write(f"**Son :** {scene.get('son', '')}")

        st.subheader("📢 Appel à l'action")
        st.info(script.get("appel_action", ""))

        st.subheader("🏷️ Description et hashtags")
        st.write(script.get("description", ""))

        hashtags = script.get("hashtags", [])
        st.write(" ".join(hashtags))

    st.download_button(
        "⬇️ Télécharger les scripts en JSON",
        data=json.dumps(
            resultat,
            ensure_ascii=False,
            indent=2
        ),
        file_name="scripts_tiktok_shorts.json",
        mime="application/json",
        use_container_width=True
    )
