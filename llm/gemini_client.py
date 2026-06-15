import os
from google import genai
from google.genai import types
from content.prompts import SYSTEM_PROMPT, build_character_block, build_scene_block, build_history_block
from content.scenes import SCENES

_client = None


def init_gemini():
    global _client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY no encontrada. Revisa tu archivo .env")
    _client = genai.Client(api_key=api_key)


def _client_or_init():
    global _client
    if _client is None:
        init_gemini()
    return _client


def get_dm_response(state: dict, player_input: str, scene_id: str) -> str:
    client = _client_or_init()
    scene = SCENES[scene_id]

    prompt = SYSTEM_PROMPT.format(
        character_block=build_character_block(state),
        scene_block=build_scene_block(scene),
        history_block=build_history_block(state.get("history", [])),
        player_input=player_input,
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.85,
            max_output_tokens=512,
        ),
    )
    return response.text.strip()


def get_ending_narration(state: dict, ending_type: str) -> str:
    client = _client_or_init()

    endings = {
        "victoria": (
            "Eres el Dungeon Master de una partida de D&D en los Reinos Olvidados. "
            "Narra un épico cierre de victoria para el personaje {name} ({race} {char_class}) "
            "que acaba de derrotar a Malachar el Señor de las Sombras en las Criptas de Undermountain. "
            "Describe cómo regresa como héroe a Faerûn. Máximo 3 párrafos, épico y emotivo. En español."
        ),
        "derrota": (
            "Eres el Dungeon Master de una partida de D&D en los Reinos Olvidados. "
            "Narra un oscuro cierre de derrota para {name} ({race} {char_class}) "
            "que ha fracasado en las Criptas de Undermountain. "
            "Máximo 2 párrafos, sombrío pero narrativamente satisfactorio. En español."
        ),
        "secreto": (
            "Eres el Dungeon Master de una partida de D&D en los Reinos Olvidados. "
            "Narra el ending secreto para {name} ({race} {char_class}) que destruyó el Sello de Undermountain "
            "liberando a cien almas atrapadas durante siglos. "
            "Es el mejor ending posible. Épico, místico, grandioso. Máximo 3 párrafos. En español."
        ),
    }

    template = endings.get(ending_type, endings["victoria"])
    prompt = template.format(
        name=state.get("name", "el aventurero"),
        race=state.get("race", ""),
        char_class=state.get("char_class", ""),
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.9,
            max_output_tokens=600,
        ),
    )
    return response.text.strip()
