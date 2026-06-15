import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from content.characters import RACES, CLASSES, build_stats
from content.scenes import SCENES, STARTING_SCENE
from engine.game_state import GameState
from engine.intent_detector import IntentDetector
from engine.scene_manager import SceneManager
from llm.groq_client import init_groq, get_dm_response, get_ending_narration

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Dungeons & Pythons",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=IM+Fell+English&display=swap');

    .stApp { background-color: #f5f0e8; }

    /* Texto general de Streamlit */
    .stApp, .stApp p, .stApp label, .stApp span, .stMarkdown p { color: #2c1e0f !important; }

    .game-title {
        font-family: 'Cinzel', serif;
        font-size: 2.4rem;
        color: #7a4f2d;
        text-align: center;
        text-shadow: 1px 1px 4px #c9a84c55;
        margin-bottom: 0.2rem;
    }
    .scene-title {
        font-family: 'Cinzel', serif;
        font-size: 1.3rem;
        color: #7a4f2d;
        border-bottom: 2px solid #c9a84c88;
        padding-bottom: 0.3rem;
        margin-bottom: 1rem;
    }
    .dm-bubble {
        background: #fdf6e3;
        border-left: 4px solid #a0714f;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        color: #2c1e0f;
        font-family: 'IM Fell English', serif;
        font-size: 1.05rem;
        line-height: 1.8;
        box-shadow: 2px 2px 6px #c9a84c22;
    }
    .player-bubble {
        background: #eaf3ea;
        border-right: 4px solid #5a8a5a;
        border-radius: 8px 0 0 8px;
        padding: 0.7rem 1rem;
        margin: 0.4rem 0;
        color: #1a3a1a;
        font-family: monospace;
        font-size: 0.95rem;
        text-align: right;
    }
    .stat-box {
        background: #fdf6e3;
        border: 1px solid #c9a84c66;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.3rem 0;
        color: #2c1e0f;
        font-size: 0.85rem;
    }
    .ending-victoria {
        background: linear-gradient(135deg, #fdf6e3, #f5ead0);
        border: 2px solid #c9a84c;
        border-radius: 12px;
        padding: 2rem;
        color: #5a3a0a;
        font-family: 'Cinzel', serif;
        text-align: center;
    }
    .ending-derrota {
        background: linear-gradient(135deg, #f5e8e8, #ecdada);
        border: 2px solid #8b0000;
        border-radius: 12px;
        padding: 2rem;
        color: #5a0000;
        font-family: 'Cinzel', serif;
        text-align: center;
    }
    .ending-secreto {
        background: linear-gradient(135deg, #ede8f5, #e0d8f0);
        border: 2px solid #7b59b6;
        border-radius: 12px;
        padding: 2rem;
        color: #3a1a5a;
        font-family: 'Cinzel', serif;
        text-align: center;
    }
    div[data-testid="stTextInput"] input {
        background: #fdf6e3 !important;
        color: #2c1e0f !important;
        border: 1px solid #a0714f !important;
        border-radius: 6px !important;
        font-family: 'IM Fell English', serif !important;
    }
    .stButton > button {
        background: #fdf6e3 !important;
        color: #7a4f2d !important;
        border: 1px solid #a0714f !important;
        border-radius: 6px !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        background: #f0e0c0 !important;
        border-color: #7a4f2d !important;
    }
    section[data-testid="stSidebar"] {
        background: #f0e8d8 !important;
        border-right: 2px solid #c9a84c66 !important;
    }
    /* Métricas en sidebar */
    [data-testid="stMetricValue"] { color: #2c1e0f !important; }
    [data-testid="stMetricLabel"] { color: #7a4f2d !important; }
</style>
""", unsafe_allow_html=True)

# ── Inicialización ────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Cargando el motor de inteligencia...")
def load_resources():
    init_groq()
    detector = IntentDetector()
    manager = SceneManager()
    return detector, manager

try:
    detector, manager = load_resources()
except ValueError:
    st.error(
        "**GROQ_API_KEY no encontrada.** "
        "Añádela en Streamlit Cloud → Manage app → Settings → Secrets:\n\n"
        "```toml\nGROQ_API_KEY = \"gsk_...\"\n```"
    )
    st.stop()

if "state" not in st.session_state:
    st.session_state.state = None
if "phase" not in st.session_state:
    st.session_state.phase = "intro"  # intro | creation | game | ending
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# ── Sidebar: hoja de personaje ────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="game-title" style="font-size:1.5rem">⚔️ Hoja de Personaje</div>', unsafe_allow_html=True)
    st.divider()

    if st.session_state.state:
        gs = GameState.from_dict(st.session_state.state)
        st.markdown(f"**{gs.name}**")
        st.markdown(f"*{RACES[gs.race].name} · {CLASSES[gs.char_class].name}*")
        st.markdown(f"🗡️ {gs.weapon.capitalize()}")
        st.divider()
        cols = st.columns(2)
        stat_icons = {"fuerza": "💪", "destreza": "🎯", "inteligencia": "🧠", "carisma": "✨", "vida": "❤️"}
        for i, (stat, val) in enumerate(gs.stats.items()):
            cols[i % 2].metric(f"{stat_icons[stat]} {stat.upper()[:3]}", val)
        st.divider()
        if gs.inventory:
            st.markdown("**🎒 Inventario**")
            for item in gs.inventory:
                st.markdown(f"- {item}")
        else:
            st.markdown("*Inventario vacío*")
        st.divider()
        scene = SCENES[gs.current_scene]
        st.markdown(f"📍 **{scene.title}**")
    else:
        st.markdown("*Crea tu personaje para comenzar*")

    st.divider()
    if st.button("🔄 Nueva partida"):
        st.session_state.state = None
        st.session_state.phase = "intro"
        st.session_state.chat_messages = []
        st.rerun()

# ── FASE: INTRO ───────────────────────────────────────────────────────────────
if st.session_state.phase == "intro":
    st.markdown('<div class="game-title">⚔️ Dungeons & Pythons ⚔️</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;color:#a0714f;font-family:\'Cinzel\',serif;font-size:1rem;margin-bottom:2rem">Las Criptas de Undermountain</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="dm-bubble">
    <strong>Bienvenido a Faerûn.</strong><br><br>
    Bajo la ciudad de Waterdeep se extiende Undermountain, la mazmorra más profunda y peligrosa
    de los Reinos Olvidados. Durante siglos, aventureros han descendido buscando gloria y tesoros.
    Pocos han regresado.<br><br>
    Ahora, una nueva amenaza se agita en sus profundidades. <strong>Malachar, el Señor de las Sombras</strong>,
    ha roto el Sello que mantenía en reposo a los muertos. Ejércitos de no-muertos amenazan con
    desbordarse hacia la superficie.<br><br>
    Se busca un héroe. Alguien que descienda, encuentre a Malachar y lo detenga antes de que
    Waterdeep caiga.<br><br>
    <em>¿Serás tú ese héroe?</em>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⚔️ Comenzar la aventura", use_container_width=True):
            st.session_state.phase = "creation"
            st.rerun()

# ── FASE: CREACIÓN DE PERSONAJE ───────────────────────────────────────────────
elif st.session_state.phase == "creation":
    st.markdown('<div class="game-title">Forja tu Destino</div>', unsafe_allow_html=True)
    st.markdown("")

    with st.form("character_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("📛 Nombre del personaje", placeholder="Ej: Thorin, Aelindra, Rook...")
            race_key = st.selectbox(
                "🧬 Raza",
                options=list(RACES.keys()),
                format_func=lambda k: RACES[k].name,
            )
        with col2:
            gender = st.selectbox("⚧ Género (narrativo)", ["masculino", "femenino", "no binario"])
            class_key = st.selectbox(
                "⚔️ Clase",
                options=list(CLASSES.keys()),
                format_func=lambda k: CLASSES[k].name,
            )

        st.markdown("")
        if race_key and class_key:
            col_r, col_c = st.columns(2)
            with col_r:
                st.markdown(f"<div class='stat-box'>🧬 <b>{RACES[race_key].name}</b><br><small>{RACES[race_key].lore}</small></div>", unsafe_allow_html=True)
            with col_c:
                st.markdown(f"<div class='stat-box'>⚔️ <b>{CLASSES[class_key].name}</b><br><small>{CLASSES[class_key].lore}</small></div>", unsafe_allow_html=True)

            preview_stats = build_stats(race_key, class_key)
            st.markdown("**Atributos resultantes:**")
            cols = st.columns(5)
            stat_labels = {"fuerza": "💪 FUE", "destreza": "🎯 DES", "inteligencia": "🧠 INT", "carisma": "✨ CAR", "vida": "❤️ VIDA"}
            for i, (stat, val) in enumerate(preview_stats.items()):
                cols[i].metric(stat_labels[stat], val)

        submitted = st.form_submit_button("⚔️ Descender a Undermountain", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Tu personaje necesita un nombre.")
        else:
            stats = build_stats(race_key, class_key)
            gs = GameState(
                name=name.strip(),
                race=race_key,
                char_class=class_key,
                weapon=CLASSES[class_key].weapon,
                stats=stats,
                inventory=[],
                current_scene=STARTING_SCENE,
            )
            st.session_state.state = gs.to_dict()
            # Mensaje inicial del DM
            intro_scene = SCENES[STARTING_SCENE]
            st.session_state.chat_messages = [
                {"role": "dm", "content": intro_scene.description}
            ]
            st.session_state.phase = "game"
            st.rerun()

# ── FASE: JUEGO ───────────────────────────────────────────────────────────────
elif st.session_state.phase == "game":
    gs = GameState.from_dict(st.session_state.state)
    scene = manager.current_scene(gs)

    st.markdown(f'<div class="scene-title">📍 {scene.title}</div>', unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.chat_messages:
        if msg["role"] == "dm":
            st.markdown(f'<div class="dm-bubble">🎲 <b>DM:</b> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="player-bubble">🗡️ {msg["content"]}</div>', unsafe_allow_html=True)

    st.markdown("")

    # Input del jugador
    with st.form("action_form", clear_on_submit=True):
        col_input, col_btn = st.columns([4, 1])
        with col_input:
            player_input = st.text_input(
                "Tu acción",
                placeholder="Describe lo que haces...",
                label_visibility="collapsed",
            )
        with col_btn:
            send = st.form_submit_button("➤ Actuar", use_container_width=True)

    if send and player_input.strip():
        with st.spinner("El DM narra..."):
            # 1. Detectar intención
            intent = detector.detect(player_input, scene.intents)

            # 2. Obtener respuesta narrativa de Gemini
            dm_response = get_dm_response(gs.to_dict(), player_input, gs.current_scene)

            # 3. Guardar en historial
            gs.add_history(player_input, dm_response)
            st.session_state.chat_messages.append({"role": "player", "content": player_input})
            st.session_state.chat_messages.append({"role": "dm", "content": dm_response})

            # 4. Intentar avanzar escena
            advanced, new_scene_id = manager.try_advance(gs, intent)
            if advanced and new_scene_id != gs.current_scene:
                if not gs.game_over:
                    new_scene = SCENES[new_scene_id]
                    st.session_state.chat_messages.append(
                        {"role": "dm", "content": f"*— {new_scene.description} —*"}
                    )

            st.session_state.state = gs.to_dict()

            if gs.game_over:
                st.session_state.phase = "ending"

            st.rerun()

    # Pista de intenciones válidas
    with st.expander("💡 Sugerencias de acciones posibles"):
        st.markdown(", ".join([f"`{i}`" for i in scene.intents]))

# ── FASE: ENDING ─────────────────────────────────────────────────────────────
elif st.session_state.phase == "ending":
    gs = GameState.from_dict(st.session_state.state)
    ending_type = gs.ending_type or "victoria"

    css_class = {
        "victoria": "ending-victoria",
        "derrota": "ending-derrota",
        "secreto": "ending-secreto",
    }.get(ending_type, "ending-victoria")

    titles = {
        "victoria": "⚔️ ¡Victoria! ⚔️",
        "derrota": "💀 Caído en la Oscuridad 💀",
        "secreto": "✨ El Sello Roto ✨",
    }

    with st.spinner("El DM narra el final de tu aventura..."):
        ending_text = get_ending_narration(gs.to_dict(), ending_type)

    st.markdown(f"""
    <div class="{css_class}">
        <h2>{titles.get(ending_type, "Fin")}</h2>
        <p style="font-family:'IM Fell English',serif;font-size:1.1rem;line-height:1.8;color:#e8d5b0;text-align:left;margin-top:1rem">
            {ending_text.replace(chr(10), '<br>')}
        </p>
        <p style="margin-top:1.5rem;opacity:0.6;font-size:0.9rem">— Fin de la aventura de {gs.name} —</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Jugar de nuevo", use_container_width=True):
            st.session_state.state = None
            st.session_state.phase = "intro"
            st.session_state.chat_messages = []
            st.rerun()
