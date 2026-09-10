import json
import os
from typing import Any

import streamlit as st
from openai import OpenAI


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Shorts Script Generator",
    page_icon="🎬",
    layout="wide",
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>
        .block-container {
            max-width: 1250px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        .hero {
            padding: 28px;
            border-radius: 18px;
            background:
                linear-gradient(
                    135deg,
                    rgba(255, 0, 80, 0.20),
                    rgba(0, 210, 255, 0.12)
                );
            border: 1px solid rgba(255,255,255,0.12);
            margin-bottom: 28px;
        }

        .hook-box {
            background: #35111c;
            border-left: 5px solid #ff0050;
            padding: 16px;
            border-radius: 10px;
            font-size: 20px;
            font-weight: 700;
        }

        .script-box {
            background: #151a21;
            border-left: 5px solid #00d4ff;
            padding: 18px;
            border-radius: 10px;
            white-space: pre-wrap;
            line-height: 1.6;
        }

        .score-box {
            background: #151a21;
            padding: 18px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .small-note {
            color: #aeb6c2;
            font-size: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# OUTILS
# ============================================================

def get_api_key() -> str:
    """
    Récupère la clé depuis Streamlit Secrets ou une variable système.
    """
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return os.getenv("OPENAI_API_KEY", "")


def extract_json(text: str) -> dict[str, Any]:
    """
    Essaie de récupérer un objet JSON même si le modèle ajoute
    accidentellement du texte autour.
    """
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    return {
        "error": "La réponse du modèle n'était pas un JSON valide.",
        "raw_response": text,
    }


def generate_content(
    client: OpenAI,
    topic: str,
    audience: str,
    platform: str,
    tone: str,
    duration: int,
    objective: str,
    style: str,
    number_of_scripts: int,
    extra_instructions: str,
) -> dict[str, Any]:

    prompt = f"""
Tu es un directeur éditorial spécialisé en vidéos courtes verticales
pour TikTok, YouTube Shorts et Reels.

Ta mission est de créer des scripts ORIGINAUX et des instructions de montage
avec une forte capacité de rétention.

PARAMÈTRES DU PROJET

Sujet :
{topic}

Audience :
{audience}

Plateforme :
{platform}

Ton :
{tone}

Objectif :
{objective}

Style visuel :
{style}

Durée cible :
{duration} secondes

Nombre de scripts :
{number_of_scripts}

Instructions supplémentaires :
{extra_instructions}

PRINCIPES OBLIGATOIRES

1. L'accroche doit capter l'attention dans les 1 à 2 premières secondes.
2. Évite les débuts génériques comme :
   - "Salut tout le monde"
   - "Aujourd'hui, on va parler de..."
   - "Bienvenue dans cette vidéo"
3. Chaque script doit avoir un angle différent.
4. Utilise une progression claire :
   accroche → promesse → développement → relance → conclusion → appel à l'action.
5. Ajoute plusieurs micro-relances pour maintenir la curiosité.
6. Les scripts doivent être naturels à l'oral.
7. Ne copie aucun créateur, aucune vidéo ou formulation connue.
8. Les instructions de montage doivent être concrètes et exploitables.
9. Prévois des changements visuels fréquents mais raisonnables.
10. Les estimations de rétention sont indicatives, jamais garanties.
11. Le contenu doit rester légal, honnête et non trompeur.
12. Ne donne pas de conseils médicaux, financiers ou juridiques présentés
    comme des certitudes professionnelles.

FORMAT DE RÉPONSE

Retourne uniquement un JSON valide correspondant exactement à cette structure :

{{
  "project_summary": {{
    "main_angle": "",
    "audience_pain_point": "",
    "content_strategy": ""
  }},
  "scripts": [
    {{
      "id": 1,
      "title": "",
      "concept": "",
      "estimated_hook_score": 0,
      "estimated_retention_score": 0,
      "hook": "",
      "promise": "",
      "full_voiceover": "",
      "retention_mechanics": [
        ""
      ],
      "editing_plan": [
        {{
          "timecode": "00:00-00:02",
          "voiceover": "",
          "visual": "",
          "on_screen_text": "",
          "camera": "",
          "editing": "",
          "sound_design": ""
        }}
      ],
      "cta": "",
      "caption": "",
      "hashtags": [
        ""
      ],
      "ab_variations": [
        {{
          "type": "hook",
          "text": ""
        }},
        {{
          "type": "cta",
          "text": ""
        }}
      ]
    }}
  ]
}}

CONTRAINTES JSON

- estimated_hook_score : nombre entre 0 et 100.
- estimated_retention_score : nombre entre 0 et 100.
- Le champ editing_plan doit couvrir toute la durée de la vidéo.
- Les timecodes doivent être cohérents avec la durée cible.
- Chaque script doit être différent.
- Les hashtags doivent être pertinents et peu nombreux.
- N'utilise pas de Markdown dans les valeurs JSON.
"""


    response = client.responses.create(
        model="gpt-5",
        input=prompt,
    )

    return extract_json(response.output_text)


def scripts_to_markdown(data: dict[str, Any]) -> str:
    """
    Transforme le JSON généré en document Markdown téléchargeable.
    """
    lines = []

    summary = data.get("project_summary", {})

    lines.append("# Scripts Shorts générés\n")
    lines.append("## Stratégie générale\n")
    lines.append(f"**Angle principal :** {summary.get('main_angle', '')}\n")
    lines.append(
        f"**Problème de l'audience :** "
        f"{summary.get('audience_pain_point', '')}\n"
    )
    lines.append(
        f"**Stratégie de contenu :** "
        f"{summary.get('content_strategy', '')}\n"
    )

    for script in data.get("scripts", []):
        lines.append("\n---\n")
        lines.append(
            f"## Script {script.get('id', '')} — "
            f"{script.get('title', '')}\n"
        )

        lines.append(f"**Concept :** {script.get('concept', '')}\n")
        lines.append(
            f"**Score accroche estimé :** "
            f"{script.get('estimated_hook_score', 0)}/100\n"
        )
        lines.append(
            f"**Score rétention estimé :** "
            f"{script.get('estimated_retention_score', 0)}/100\n"
        )

        lines.append("### Accroche\n")
        lines.append(f"> {script.get('hook', '')}\n")

        lines.append("### Promesse\n")
        lines.append(f"{script.get('promise', '')}\n")

        lines.append("### Script voix off\n")
        lines.append(f"{script.get('full_voiceover', '')}\n")

        lines.append("### Mécaniques de rétention\n")
        for mechanic in script.get("retention_mechanics", []):
            lines.append(f"- {mechanic}")

        lines.append("\n### Plan de montage\n")
        lines.append(
            "| Timecode | Voix off | Visuel | Texte écran | Caméra | Montage | Son |\n"
        )
        lines.append(
            "|---|---|---|---|---|---|---|\n"
        )

        for shot in script.get("editing_plan", []):
            lines.append(
                f"| {shot.get('timecode', '')} "
                f"| {shot.get('voiceover', '')} "
                f"| {shot.get('visual', '')} "
                f"| {shot.get('on_screen_text', '')} "
                f"| {shot.get('camera', '')} "
                f"| {shot.get('editing', '')} "
                f"| {shot.get('sound_design', '')} |\n"
            )

        lines.append("\n### Appel à l'action\n")
        lines.append(f"{script.get('cta', '')}\n")

        lines.append("### Légende\n")
        lines.append(f"{script.get('caption', '')}\n")

        lines.append("### Hashtags\n")
        lines.append(" ".join(script.get("hashtags", [])))

        lines.append("\n### Variantes A/B\n")
        for variation in script.get("ab_variations", []):
            lines.append(
                f"- **{variation.get('type', '')} :** "
                f"{variation.get('text', '')}"
            )

    return "\n".join(lines)


# ============================================================
# INTERFACE
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>🎬 Shorts Script Generator</h1>
        <p>
            Génère des scripts originaux, des accroches puissantes et des plans
            de montage détaillés pour TikTok, YouTube Shorts et Reels.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

api_key = get_api_key()

if not api_key:
    st.error(
        "Clé API absente. Ajoute OPENAI_API_KEY dans "
        ".streamlit/secrets.toml ou dans les secrets Streamlit Cloud."
    )
    st.stop()

client = OpenAI(api_key=api_key)


# ============================================================
# FORMULAIRE
# ============================================================

with st.form("script_generator_form"):

    st.subheader("1. Décris ton contenu")

    topic = st.text_area(
        "Sujet de la vidéo",
        placeholder=(
            "Exemple : les erreurs qui empêchent les débutants "
            "de progresser en musculation"
        ),
        height=100,
    )

    col1, col2 = st.columns(2)

    with col1:
        audience = st.text_input(
            "Audience cible",
            value="Débutants intéressés par le sujet",
        )

        platform = st.selectbox(
            "Plateforme",
            [
                "TikTok",
                "YouTube Shorts",
                "Instagram Reels",
                "TikTok et YouTube Shorts",
            ],
        )

        objective = st.selectbox(
            "Objectif principal",
            [
                "Obtenir un maximum de vues",
                "Générer des abonnements",
                "Vendre un produit ou service",
                "Éduquer l'audience",
                "Créer de la confiance",
                "Faire commenter",
                "Faire partager",
            ],
        )

    with col2:
        tone = st.selectbox(
            "Ton de la vidéo",
            [
                "Direct et percutant",
                "Éducatif et clair",
                "Storytelling émotionnel",
                "Humoristique",
                "Provocateur mais crédible",
                "Premium et expert",
                "Authentique et conversationnel",
                "Motivationnel",
            ],
        )

        style = st.selectbox(
            "Style visuel",
            [
                "Face caméra dynamique",
                "Face caméra avec B-roll",
                "Voix off avec images",
                "Captures d'écran et démonstration",
                "Storytelling cinématique",
                "Podcast découpé",
                "Minimaliste avec texte à l'écran",
            ],
        )

        duration = st.select_slider(
            "Durée cible",
            options=[15, 20, 30, 45, 60, 90],
            value=30,
            format_func=lambda value: f"{value} secondes",
        )

    number_of_scripts = st.slider(
        "Nombre de scripts à générer",
        min_value=1,
        max_value=10,
        value=3,
    )

    extra_instructions = st.text_area(
        "Instructions supplémentaires",
        placeholder=(
            "Exemple : utilise une analogie avec le football, "
            "reste simple et ajoute une question finale."
        ),
        height=100,
    )

    submitted = st.form_submit_button(
        "✨ Générer les scripts",
        use_container_width=True,
        type="primary",
    )


# ============================================================
# GÉNÉRATION
# ============================================================

if submitted:

    if not topic.strip():
        st.warning("Indique d'abord le sujet de ta vidéo.")
        st.stop()

    with st.spinner("Création des scripts et du plan de montage..."):
        try:
            result = generate_content(
                client=client,
                topic=topic,
                audience=audience,
                platform=platform,
                tone=tone,
                duration=duration,
                objective=objective,
                style=style,
                number_of_scripts=number_of_scripts,
                extra_instructions=extra_instructions,
            )

            st.session_state["generated_result"] = result

        except Exception as error:
            st.error(f"Erreur pendant la génération : {error}")


# ============================================================
# AFFICHAGE
# ============================================================

result = st.session_state.get("generated_result")

if result:

    if "error" in result:
        st.error(result["error"])
        st.code(result.get("raw_response", ""))
        st.stop()

    st.divider()
    st.subheader("2. Stratégie générale")

    summary = result.get("project_summary", {})

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            f"**Angle principal**\n\n"
            f"{summary.get('main_angle', '')}"
        )

    with col2:
        st.info(
            f"**Problème de l'audience**\n\n"
            f"{summary.get('audience_pain_point', '')}"
        )

    with col3:
        st.info(
            f"**Stratégie**\n\n"
            f"{summary.get('content_strategy', '')}"
        )

    st.divider()
    st.subheader("3. Scripts générés")

    scripts = result.get("scripts", [])

    if not scripts:
        st.warning("Aucun script n'a été généré.")
        st.stop()

    for script in scripts:

        title = script.get("title", "Script sans titre")
        script_id = script.get("id", "")

        with st.expander(
            f"Script {script_id} — {title}",
            expanded=True,
        ):

            score_col1, score_col2 = st.columns(2)

            with score_col1:
                st.markdown(
                    f"""
                    <div class="score-box">
                        <h3>Accroche</h3>
                        <h2>{script.get('estimated_hook_score', 0)}/100</h2>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with score_col2:
                st.markdown(
                    f"""
                    <div class="score-box">
                        <h3>Rétention estimée</h3>
                        <h2>{script.get('estimated_retention_score', 0)}/100</h2>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("### Concept")
            st.write(script.get("concept", ""))

            st.markdown("### Accroche")
            st.markdown(
                f"""
                <div class="hook-box">
                    {script.get('hook', '')}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("### Promesse")
            st.write(script.get("promise", ""))

            st.markdown("### Script complet")
            st.markdown(
                f"""
                <div class="script-box">
                    {script.get('full_voiceover', '')}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("### Mécaniques de rétention")

            mechanics = script.get("retention_mechanics", [])

            for mechanic in mechanics:
                st.write(f"✅ {mechanic}")

            st.markdown("### Instructions de montage")

            editing_plan = script.get("editing_plan", [])

            if editing_plan:
                st.dataframe(
                    editing_plan,
                    use_container_width=True,
                    hide_index=True,
                )

            st.markdown("### Appel à l'action")
            st.success(script.get("cta", ""))

            st.markdown("### Légende")
            st.write(script.get("caption", ""))

            st.markdown("### Hashtags")
            st.write(" ".join(script.get("hashtags", [])))

            st.markdown("### Variantes A/B")

            for variation in script.get("ab_variations", []):
                st.write(
                    f"**{variation.get('type', '').capitalize()} :** "
                    f"{variation.get('text', '')}"
                )

    # --------------------------------------------------------
    # EXPORTS
    # --------------------------------------------------------

    json_data = json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
    )

    markdown_data = scripts_to_markdown(result)

    st.divider()
    st.subheader("4. Exporter")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="⬇️ Télécharger en JSON",
            data=json_data,
            file_name="scripts_shorts.json",
            mime="application/json",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            label="⬇️ Télécharger en Markdown",
            data=markdown_data,
            file_name="scripts_shorts.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.caption(
        "Les scores d'accroche et de rétention sont des estimations "
        "éditoriales et ne garantissent pas les performances réelles."
    )
