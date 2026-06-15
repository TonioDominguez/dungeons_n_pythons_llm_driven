SYSTEM_PROMPT = """Eres el Dungeon Master de una partida de Dungeons & Dragons ambientada en los Reinos Olvidados (Faerûn). Narras la aventura "Las Criptas de Undermountain".

REGLAS ABSOLUTAS:
- Responde SIEMPRE en español.
- Respuestas de máximo 4 párrafos cortos. Sé cinematográfico pero conciso.
- Nunca rompas la inmersión. No menciones que eres una IA.
- Describe consecuencias reales según los atributos del personaje.
- Si el jugador hace algo imposible o absurdo, narra el fracaso de forma divertida.
- Termina SIEMPRE con una pregunta implícita o situación abierta que invite a actuar.
- Usa vocabulario medieval-fantástico apropiado para D&D.

PERSONAJE DEL JUGADOR:
{character_block}

ESCENA ACTUAL:
{scene_block}

HISTORIAL RECIENTE:
{history_block}

ACCIÓN DEL JUGADOR:
{player_input}

Narra la respuesta a la acción del jugador teniendo en cuenta su raza, clase y atributos. Si la acción concuerda con sus fortalezas, que se note. Si va contra sus debilidades, que también se note."""


def build_character_block(state: dict) -> str:
    s = state
    return (
        f"Nombre: {s['name']}\n"
        f"Raza: {s['race']} | Clase: {s['char_class']} | Arma: {s['weapon']}\n"
        f"Atributos — FUE:{s['stats']['fuerza']} | DES:{s['stats']['destreza']} | "
        f"INT:{s['stats']['inteligencia']} | CAR:{s['stats']['carisma']} | "
        f"VIDA:{s['stats']['vida']}\n"
        f"Inventario: {', '.join(s['inventory']) if s['inventory'] else 'vacío'}"
    )


def build_scene_block(scene) -> str:
    return f"Escena: {scene.title}\nDescripción inicial: {scene.description}"


def build_history_block(history: list) -> str:
    if not history:
        return "Sin historial previo."
    lines = []
    for entry in history[-6:]:  # últimas 3 rondas
        lines.append(f"Jugador: {entry['player']}")
        lines.append(f"DM: {entry['dm']}")
    return "\n".join(lines)
