![Dungeons and Pythons](https://imgur.com/a/g061inc)

# Dungeons & Pythons: Las Criptas de Undermountain

## Resumen del proyecto

"Dungeons & Pythons: Las Criptas de Undermountain" es la evolución natural de mis versiones anteriores del juego. Un RPG de texto ambientado en los Reinos Olvidados de D&D donde el jugador escribe libremente lo que quiere hacer y el sistema responde con narrativa generada en tiempo real.

El cambio respecto a versiones anteriores es pasar de respuestas predefinidas a generación dinámica con un LLM. En lugar de vectorizar el input del usuario y buscarlo contra un banco de respuestas fijas, aquí los embeddings detectan la intención del jugador y Llama 3.3 70B (vía Groq) hace de Dungeon Master generando la narración al momento. Cada partida es diferente porque el modelo tiene en cuenta el personaje, lo que ha pasado antes y la escena actual.

Este proyecto es continuación directa de [Dungeons & Pythons (Embedding Edition)](https://github.com/TonioDominguez/dungeons_and_pythons_embeddings), al que le añado generación de texto con IA sobre el sistema de embeddings original.

## Contenido del repositorio

```
claude-dungeons-n-pythons/
│
├── content/                    # Contenido narrativo y de personaje
│   ├── characters.py           # Razas, clases y atributos D&D
│   ├── scenes.py               # Escenas, condiciones de avance y endings
│   └── prompts.py              # System prompts del Dungeon Master
│
├── engine/                     # Motor del juego
│   ├── game_state.py           # Estado del juego (personaje, progreso, inventario)
│   ├── intent_detector.py      # Detección de intención con embeddings
│   └── scene_manager.py        # Gestión de transiciones entre escenas
│
├── llm/                        # Cliente del modelo de lenguaje
│   └── groq_client.py          # Integración con Groq API (Llama 3.3 70B)
│
├── .env.example                # Plantilla de variables de entorno
├── .gitignore                  # Archivos ignorados por Git
├── README.md                   # Documentación del proyecto
├── app.py                      # Aplicación Streamlit
└── requirements.txt            # Dependencias del proyecto
```

## Características principales

- RPG de texto ambientado en los Reinos Olvidados (Faerûn) de D&D
- Narrativa generada en tiempo real por un LLM, cada partida es única
- Creación de personaje con 36 combinaciones posibles (6 razas x 6 clases)
- Sistema de atributos D&D (Fuerza, Destreza, Inteligencia, Carisma, Vida) que afectan mecánicamente la narrativa
- 4 escenas, sistema de branching y 3 endings posibles (victoria, derrota y ending secreto)
- Interfaz en tema pergamino medieval con hoja de personaje en tiempo real

## Características técnicas

- Detección de intención del jugador mediante embeddings semánticos (`all-MiniLM-L6-v2`)
- Generación de narrativa con Llama 3.3 70B a través de la API de Groq
- Historial de conversación para mantener contexto narrativo entre turnos
- Gestión de estado de sesión con Streamlit
- Arquitectura modular con contenido, motor, LLM e interfaz separados

## Modelos de IA

- [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2): detección de intenciones del jugador mediante similitud semántica
- [Llama 3.3 70B](https://console.groq.com) vía Groq API: generación de narrativa como Dungeon Master

## Cómo jugar

Necesitas una API key gratuita de Groq. La puedes obtener en [console.groq.com](https://console.groq.com/keys) sin tarjeta de crédito.

1. Clona el repositorio

   ```git clone https://github.com/TonioDominguez/claude-dungeons-n-pythons.git```

2. Navega al directorio

   ```cd claude-dungeons-n-pythons```

3. Instala las dependencias

   ```pip install -r requirements.txt```

4. Copia el archivo de entorno y añade tu key

   ```cp .env.example .env```

5. Lanza la aplicación

   ```streamlit run app.py```

## Estructura del juego

El jugador elige raza y clase al crear el personaje, lo que genera unos atributos base que el Dungeon Master tiene en cuenta durante toda la partida. A partir de ahí, escribe sus acciones en texto libre.

El sistema de embeddings clasifica la intención detrás de cada input (atacar, explorar, negociar, huir...) y decide si el jugador avanza de escena. El LLM genera la respuesta narrativa con toda esa información disponible.

Las cuatro escenas del juego son:
- La Taberna del Grifo Cojo: punto de partida
- Los Túneles Exteriores: primer enfrentamiento y exploración
- La Sala del Oráculo: puzle narrativo, negociación o engaño
- La Cámara del Señor de las Sombras: confrontación final con Malachar

## Apuntes finales

Este proyecto es un prototipo funcional que muestra lo que ocurre cuando combinas embeddings para la lógica de juego con un LLM para la narrativa. El resultado me ha sorprendido bastante: el Dungeon Master responde de forma coherente al personaje, recuerda lo que ha pasado y adapta el tono a la situación mejor de lo que esperaba al empezar.

Hay cosas que me gustaría desarrollar en el futuro, como un sistema de combate con dados y tiradas reales, más escenas y ramificaciones, o inventario interactivo. Pero como punto de partida creo que refleja bien hacia dónde puede ir este tipo de proyectos.

Si tienes alguna sugerencia o quieres contribuir, puedes contactarme en antonio.d.ambunan@gmail.com o conectar por [LinkedIn](https://www.linkedin.com/in/antoniodominguezambunan/)

---
