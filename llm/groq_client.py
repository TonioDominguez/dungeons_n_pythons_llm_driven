import os
from groq import Groq
from content.prompts import SYSTEM_PROMPT, build_character_block, build_scene_block, build_history_block
from content.scenes import SCENES

MODEL = "llama-3.3-70b-versatile"
_client = None


def init_groq():
    global _client
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            pass
    if not api_key:
        raise ValueError("GROQ_API_KEY no encontrada. Revisa tu archivo .env o los Secrets de Streamlit Cloud")
    _client = Groq(api_key=api_key)


def _get_client():
    global _client
    if _client is None:
        init_groq()
    return _client


def get_dm_response(state: dict, player_input: str, scene_id: str) -> str:
    client = _get_client()
    scene = SCENES[scene_id]

    system = SYSTEM_PROMPT.format(
        character_block=build_character_block(state),
        scene_block=build_scene_block(scene),
        history_block=build_history_block(state.get("history", [])),
        player_input=player_input,
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": player_input},
        ],
        temperature=0.85,
        max_tokens=512,
    )
    return response.choices[0].message.content.strip()


def get_ending_narration(state: dict, ending_type: str) -> str:
    client = _get_client()

    endings = {
        "victoria": (
            "Eres el Dungeon Master de D&D en los Reinos Olvidados. "
            "Narra un épico cierre de victoria para {name} ({race} {char_class}) "
            "que acaba de derrotar a Malachar el Señor de las Sombras en Undermountain. "
            "Máximo 3 párrafos, épico y emotivo. Responde solo en español."
        ),
        "derrota": (
            "Eres el Dungeon Master de D&D en los Reinos Olvidados. "
            "Narra un oscuro cierre de derrota para {name} ({race} {char_class}) "
            "que ha fracasado en las Criptas de Undermountain. "
            "Máximo 2 párrafos, sombrío pero narrativamente satisfactorio. Solo en español."
        ),
        "secreto": (
            "Eres el Dungeon Master de D&D en los Reinos Olvidados. "
            "Narra el ending secreto para {name} ({race} {char_class}) que destruyó el Sello "
            "de Undermountain liberando a cien almas atrapadas. "
            "Épico, místico, grandioso. Máximo 3 párrafos. Solo en español."
        ),
    }

    prompt = endings.get(ending_type, endings["victoria"]).format(
        name=state.get("name", "el aventurero"),
        race=state.get("race", ""),
        char_class=state.get("char_class", ""),
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=600,
    )
    return response.choices[0].message.content.strip()
