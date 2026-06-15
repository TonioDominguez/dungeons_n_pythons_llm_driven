from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Scene:
    id: str
    title: str
    description: str          # Descripción inicial al entrar
    image_hint: str           # Palabra clave para imagen (uso futuro)
    intents: List[str]        # Intenciones válidas en esta escena
    advance_conditions: dict  # {intent: next_scene_id}
    is_ending: bool = False
    ending_type: Optional[str] = None  # "victoria", "derrota", "secreto"

SCENES = {
    "taberna": Scene(
        id="taberna",
        title="La Taberna del Grifo Cojo",
        description=(
            "El olor a cerveza rancia y madera quemada llena tus pulmones. "
            "La Taberna del Grifo Cojo es el último punto civilizado antes de las "
            "Criptas de Undermountain. En una esquina, un enano con cicatrices en la "
            "cara ofrece monedas de oro a quien se atreva a descender. "
            "En la barra, una carta desgastada describe los horrores que aguardan abajo. "
            "¿Qué haces?"
        ),
        image_hint="tavern",
        intents=["hablar", "explorar", "beber", "leer", "descender"],
        advance_conditions={
            "descender": "tuneles",
            "leer": "tuneles",
        },
    ),
    "tuneles": Scene(
        id="tuneles",
        title="Los Túneles Exteriores",
        description=(
            "La oscuridad se traga tu antorcha a pocos metros. El aire huele a "
            "tierra húmeda y algo más... a muerte. Las paredes de piedra están "
            "cubiertas de runas antiguas que pulsan con una débil luz azul. "
            "Escuchas pasos al fondo del pasillo. No eres el único aquí. "
            "¿Qué haces?"
        ),
        image_hint="dungeon_tunnel",
        intents=["atacar", "explorar", "esconderse", "avanzar", "huir"],
        advance_conditions={
            "atacar": "oraculo",
            "explorar": "oraculo",
            "avanzar": "oraculo",
        },
    ),
    "oraculo": Scene(
        id="oraculo",
        title="La Sala del Oráculo",
        description=(
            "Una cámara circular se abre ante ti. En el centro, una figura encadenada "
            "a un trono de obsidiana — el Oráculo de Undermountain. Sus ojos ciegos "
            "giran hacia ti aunque no puede verte. 'Bienvenido, buscador,' susurra con "
            "una voz que suena a piedras arrastrándose. 'Responde bien mis preguntas "
            "y te daré el camino. Falla... y te quedarás aquí para siempre.' "
            "¿Qué haces?"
        ),
        image_hint="oracle",
        intents=["hablar", "atacar", "negociar", "engañar", "pensar"],
        advance_conditions={
            "hablar": "camara_final",
            "negociar": "camara_final",
            "pensar": "camara_final",
            "engañar": "camara_final",
            "atacar": "derrota_oraculo",
        },
    ),
    "camara_final": Scene(
        id="camara_final",
        title="La Cámara del Señor de las Sombras",
        description=(
            "El suelo tiembla. Ante ti se alza Malachar, el Señor de las Sombras, "
            "una figura de oscuridad condensada con ojos como brasas. Detrás de él, "
            "el Sello de Undermountain pulsa en la pared — si lo destruyes, las "
            "criptas colapsan y los muertos descansan para siempre. "
            "'¿Has venido a morir?' pregunta Malachar, y su voz llena la cámara "
            "como el retumbar de un trueno. ¿Qué haces?"
        ),
        image_hint="boss_chamber",
        intents=["atacar", "usar objeto", "negociar", "huir", "destruir sello"],
        advance_conditions={
            "atacar": "victoria",
            "destruir sello": "victoria_secreta",
            "huir": "derrota_final",
            "negociar": "victoria",
        },
    ),
    "victoria": Scene(
        id="victoria",
        title="Victoria — Las Criptas Liberadas",
        description=(
            "Malachar se desvanece en un grito de oscuridad. Su forma se dispersa "
            "como humo ante el viento y las llamas que lo consumían se apagan. "
            "El silencio llega de golpe, tan pesado que casi duele. "
            "Has liberado las Criptas de Undermountain."
        ),
        image_hint="victory",
        intents=[],
        advance_conditions={},
        is_ending=True,
        ending_type="victoria",
    ),
    "victoria_secreta": Scene(
        id="victoria_secreta",
        title="El Sello Roto — Ending Secreto",
        description=(
            "Al destruir el Sello, una onda de energía arcana te traversa. "
            "No solo has derrotado a Malachar — has liberado a los espíritus "
            "atrapados durante siglos. Cien almas susurran tu nombre mientras "
            "ascienden. Undermountain nunca volverá a ser una amenaza. "
            "Tu nombre quedará grabado en las crónicas de Faerûn para siempre."
        ),
        image_hint="secret_ending",
        intents=[],
        advance_conditions={},
        is_ending=True,
        ending_type="secreto",
    ),
    "derrota_oraculo": Scene(
        id="derrota_oraculo",
        title="Atrapado en el Oráculo",
        description=(
            "Atacar al Oráculo fue tu último error. Las cadenas que lo atan "
            "cobran vida y te envuelven. La figura ciega sonríe. "
            "'Otro guardián para mi colección,' murmura. "
            "Tu aventura termina aquí, petrificado para la eternidad."
        ),
        image_hint="defeat",
        intents=[],
        advance_conditions={},
        is_ending=True,
        ending_type="derrota",
    ),
    "derrota_final": Scene(
        id="derrota_final",
        title="Huida — Derrota",
        description=(
            "Corres. Malachar no te persigue — no necesita hacerlo. "
            "Los túneles colapsan a tu alrededor mientras su risa llena las paredes. "
            "Llegas a la superficie, pero Undermountain permanece. "
            "Los muertos seguirán inquietos. La misión ha fallado."
        ),
        image_hint="defeat",
        intents=[],
        advance_conditions={},
        is_ending=True,
        ending_type="derrota",
    ),
}

STARTING_SCENE = "taberna"
