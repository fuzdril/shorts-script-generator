import json
import random
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Générateur TikTok & Shorts",
    page_icon="🎬",
    layout="wide"
)


# ============================================================
# INTERFACE
# ============================================================

st.title("🎬 Générateur TikTok & YouTube Shorts")
st.caption(
    "Génération gratuite de scripts verticaux 9:16 sans clé API"
)


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
        "Durée de la vidéo",
        [
            "15 secondes",
            "30 secondes",
            "45 secondes",
            "60 secondes"
        ]
    )

    ton = st.selectbox(
        "Ton du script",
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
        "Obtenir plus de likes",
        "Obtenir plus de vues",
        "Faire découvrir une information",
        "Vendre un produit",
        "Construire de l'autorité",
        "Créer une vidéo virale"
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


# ============================================================
# DONNÉES DE GÉNÉRATION
# ============================================================

ACCROCHES = [
    "Personne ne te dit la vérité sur {sujet}.",
    "Voici pourquoi tu n'obtiens pas de résultats avec {sujet}.",
    "Arrête de faire cette erreur avec {sujet}.",
    "En moins d'une minute, tu vas comprendre {sujet}.",
    "La plupart des gens se trompent complètement sur {sujet}.",
    "Si tu débutes dans ce domaine, écoute bien.",
    "Cette erreur peut te faire perdre énormément de temps.",
    "Voici la méthode la plus simple pour progresser.",
    "Tu fais probablement cette erreur sans t'en rendre compte.",
    "Regarde cette vidéo avant de commencer."
]

PROMESSES = [
    "Tu vas découvrir une méthode simple, rapide et directement applicable.",
    "Tu vas comprendre l'erreur principale et savoir comment l'éviter.",
    "Tu vas repartir avec une action concrète à appliquer aujourd'hui.",
    "Tu vas apprendre une méthode adaptée aux débutants.",
    "Tu vas comprendre comment obtenir de meilleurs résultats."
]

MECANISMES = [
    "Accroche forte dans les deux premières secondes",
    "Phrases courtes et faciles à comprendre",
    "Relance de curiosité régulière",
    "Changements visuels fréquents",
    "Texte important placé au centre de l'écran",
    "Démonstration concrète",
    "Suspense avant la révélation finale",
    "Appel à l'action directement lié à l'objectif"
]


# ============================================================
# FONCTIONS
# ============================================================

def obtenir_appel_action(objectif):
    appels = {
        "Obtenir des commentaires":
            "Écris ton avis en commentaire.",
        "Augmenter les abonnements":
            "Abonne-toi pour recevoir d'autres conseils.",
        "Obtenir plus de likes":
            "Like cette vidéo si elle t'a été utile.",
        "Obtenir plus de vues":
            "Partage cette vidéo à quelqu'un qui en a besoin.",
        "Faire découvrir une information":
            "Enregistre cette vidéo pour la revoir plus tard.",
        "Vendre un produit":
            "Clique sur le lien pour découvrir l'offre.",
        "Construire de l'autorité":
            "Suis le compte pour apprendre d'autres méthodes.",
        "Créer une vidéo virale":
            "Commente « PARTIE 2 » si tu veux la suite."
    }

    return appels.get(
        objectif,
        "Abonne-toi pour découvrir la suite."
    )


def obtenir_duree_secondes(duree):
    correspondance = {
        "15 secondes": 15,
        "30 secondes": 30,
        "45 secondes": 45,
        "60 secondes": 60
    }

    return correspondance.get(duree, 30)


def creer_plan_montage(
    sujet,
    accroche,
    appel_action,
    duree,
    style_montage
):
    duree_secondes = obtenir_duree_secondes(duree)

    premier_temps = min(3, duree_secondes)
    deuxieme_temps = min(8, duree_secondes)
    troisieme_temps = min(15, duree_secondes)
    quatrieme_temps = min(max(20, duree_secondes - 5), duree_secondes)

    plan = [
        {
            "timecode": f"00:00 - 00:0{premier_temps}",
            "voix_off": accroche,
            "visuel": (
                f"{style_montage} avec mouvement rapide "
                "vers la caméra"
            ),
            "cadrage": "Plan poitrine vertical 9:16",
            "texte_ecran": accroche,
            "sous_titres": accroche,
            "transition": "Cut rapide",
            "son": "Impact sonore court"
        },
        {
            "timecode": f"00:0{premier_temps} - 00:{deuxieme_temps:02d}",
            "voix_off": (
                f"Le problème avec {sujet}, c'est que beaucoup "
                "de personnes commencent sans méthode."
            ),
            "visuel": (
                "Illustration de l'erreur avec texte animé "
                "et élément visuel contrasté"
            ),
            "cadrage": "Plan rapproché",
            "texte_ecran": "L'erreur principale",
            "sous_titres": (
                "Beaucoup de personnes font cette erreur"
            ),
            "transition": "Zoom avant léger",
            "son": "Musique rythmée"
        },
        {
            "timecode": f"00:{deuxieme_temps:02d} - 00:{troisieme_temps:02d}",
            "voix_off": (
                "La solution consiste à commencer par une action "
                "simple et à la répéter régulièrement."
            ),
            "visuel": (
                "Démonstration étape par étape avec flèches "
                "et mots-clés à l'écran"
            ),
            "cadrage": "Plan vertical centré",
            "texte_ecran": "La méthode simple",
            "sous_titres": (
                "Commence simplement et reste régulier"
            ),
            "transition": "Swipe vertical",
            "son": "Whoosh léger"
        },
        {
            "timecode": f"00:{troisieme_temps:02d} - 00:{quatrieme_temps:02d}",
            "voix_off": (
                "Teste cette méthode aujourd'hui et compare "
                "tes résultats après quelques jours."
            ),
            "visuel": (
                "Résultat concret, comparaison avant/après "
                "ou exemple pratique"
            ),
            "cadrage": "Plan dynamique",
            "texte_ecran": "À tester aujourd'hui",
            "sous_titres": (
                "Passe à l'action dès maintenant"
            ),
            "transition": "Cut synchronisé avec la musique",
            "son": "Montée musicale"
        },
        {
            "timecode": f"00:{quatrieme_temps:02d} - 00:{duree_secondes:02d}",
            "voix_off": appel_action,
            "visuel": (
                "Retour face caméra avec geste vers "
                "le bouton d'action"
            ),
            "cadrage": "Gros plan vertical",
            "texte_ecran": appel_action,
            "sous_titres": appel_action,
            "transition": "Arrêt sur image",
            "son": "Impact final"
        }
    ]

    return plan


def generer_un_script(
    numero,
    sujet,
    audience,
    plateforme,
    duree,
    ton,
    objectif,
    style_montage,
    instructions
):
    accroche = random.choice(ACCROCHES).format(sujet=sujet)
    promesse = random.choice(PROMESSES)
    appel_action = obtenir_appel_action(objectif)

    if audience.strip():
        audience_phrase = (
            f"Cette vidéo s'adresse particulièrement à {audience}."
        )
    else:
        audience_phrase = (
            "Cette vidéo s'adresse aux personnes qui veulent progresser."
        )

    voix_off = (
        f"{accroche} "
        f"{audience_phrase} "
        f"{promesse} "
        f"Le problème, c'est que beaucoup de personnes "
        f"font la même erreur au début. "
        f"Au lieu de vouloir tout faire en même temps, "
        f"commence par une seule action claire. "
        f"Applique-la régulièrement et observe tes résultats. "
        f"Teste cette méthode dès aujourd'hui. "
        f"{appel_action}"
    )

    plan_montage = creer_plan_montage(
        sujet=sujet,
        accroche=accroche,
        appel_action=appel_action,
        duree=duree,
        style_montage=style_montage
    )

    mecanismes = MECANISMES.copy()

    if instructions.strip():
        mecanismes.append(
            f"Instruction spéciale respectée : {instructions}"
        )

    return {
        "titre": f"{sujet} - variante {numero}",
        "angle": (
            f"Approche {ton.lower()} pour {plateforme}, "
            f"avec l'objectif : {objectif}"
        ),
        "accroche": accroche,
        "promesse": promesse,
        "score_accroche": random.randint(82, 96),
        "score_retention": random.randint(80, 94),
        "voix_off_complete": voix_off,
        "mecanismes_retention": mecanismes,
        "plan_montage": plan_montage,
        "appel_action": appel_action,
        "description": (
            f"{sujet} : découvre une méthode simple et applicable "
            f"pour progresser. Objectif : {objectif}."
        ),
        "hashtags": [
            "#TikTok",
            "#YouTubeShorts",
            "#CreationDeContenu",
            "#Conseils",
            "#VideoVerticale",
            "#Viral"
        ]
    }


def generer_scripts():
    resultat = []

    for numero in range(1, nombre + 1):
        script = generer_un_script(
            numero=numero,
            sujet=sujet.strip(),
            audience=audience.strip(),
            plateforme=plateforme,
            duree=duree,
            ton=ton,
            objectif=objectif,
            style_montage=style_montage,
            instructions=instructions.strip()
        )

        resultat.append(script)

    return {"scripts": resultat}


# ============================================================
# AFFICHAGE DES SCRIPTS
# ============================================================

def afficher_script(script, index):
    st.divider()

    st.header(
        f"Script {index} — {script.get('titre', 'Sans titre')}"
    )

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
        "Script voix off",
        script.get("voix_off_complete", ""),
        height=220,
        key=f"voix_off_{index}"
    )

    st.subheader("🧠 Mécanismes de rétention")

    for element in script.get("mecanismes_retention", []):
        st.write(f"• {element}")

    st.subheader("✂️ Plan de montage vertical")

    for scene_index, scene in enumerate(
        script.get("plan_montage", []),
        start=1
    ):
        timecode = scene.get("timecode", "")
        visuel = scene.get("visuel", "")

        with st.expander(
            f"Scène {scene_index} — {timecode} — {visuel}"
        ):
            st.write(
                f"**Voix off :** {scene.get('voix_off', '')}"
            )
            st.write(
                f"**Cadrage :** {scene.get('cadrage', '')}"
            )
            st.write(
                f"**Visuel :** {scene.get('visuel', '')}"
            )
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
            st.write(
                f"**Son :** {scene.get('son', '')}"
            )

    st.subheader("📢 Appel à l'action")
    st.info(script.get("appel_action", ""))

    st.subheader("🏷️ Description et hashtags")
    st.write(script.get("description", ""))

    hashtags = script.get("hashtags", [])
    st.write(" ".join(hashtags))


# ============================================================
# BOUTON DE GÉNÉRATION
# ============================================================

if st.button(
    "🚀 Générer les scripts",
    type="primary",
    use_container_width=True
):
    if not sujet.strip():
        st.warning("Indique d'abord le sujet de la vidéo.")
        st.stop()

    with st.spinner("Génération gratuite des scripts..."):
        resultat = generer_scripts()

    for index, script in enumerate(
        resultat["scripts"],
        start=1
    ):
        afficher_script(script, index)

    st.divider()

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
