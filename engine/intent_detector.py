from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Mapa de intenciones → frases de ejemplo
INTENT_EXAMPLES = {
    "atacar": [
        "ataco", "golpeo", "combato", "lucho", "hiero", "embisto", "cargo", "ataque",
        "uso mi espada", "uso mi hacha", "disparo", "lanzo un hechizo de daño",
    ],
    "explorar": [
        "exploro", "miro alrededor", "busco", "inspecciono", "examino", "investigo",
        "recorro", "observo", "registro el lugar", "busco secretos",
    ],
    "hablar": [
        "hablo", "pregunto", "digo", "me dirijo a", "converso", "saludo",
        "pregunto por", "intento hablar", "me acerco y hablo",
    ],
    "negociar": [
        "negocio", "ofrezco", "propongo un trato", "intento llegar a un acuerdo",
        "le ofrezco oro", "pactamos", "hagamos un trato",
    ],
    "engañar": [
        "engaño", "miento", "finjo", "me hago pasar por", "bluff", "intento engañar",
        "le digo una mentira", "lo distraigo",
    ],
    "huir": [
        "huyo", "corro", "me retiro", "escapo", "me voy", "abandono", "salgo corriendo",
        "busco la salida", "me marcho",
    ],
    "esconderse": [
        "me escondo", "me oculto", "sigilo", "me pongo en las sombras",
        "paso desapercibido", "me agacho", "me meto detrás de",
    ],
    "usar objeto": [
        "uso", "utilizo", "saco del inventario", "aplico", "bebo la poción",
        "uso el objeto", "equipo", "agarro",
    ],
    "descender": [
        "bajo", "desciendo", "entro a la mazmorra", "me adentro", "cruzo la puerta",
        "acepto la misión", "voy a la mazmorra",
    ],
    "leer": [
        "leo", "examino el papel", "miro la carta", "leo el pergamino",
        "estudio el mapa", "leo el aviso",
    ],
    "beber": [
        "bebo", "pido una cerveza", "tomo algo", "me siento en la barra",
        "pido algo de beber", "bebo cerveza",
    ],
    "avanzar": [
        "avanzo", "sigo adelante", "continúo", "camino hacia", "me muevo hacia",
        "prosigo", "sigo el pasillo",
    ],
    "pensar": [
        "pienso", "reflexiono", "analizo", "medito", "recapacito", "considero",
        "evalúo la situación", "me tomo un momento",
    ],
    "destruir sello": [
        "destruyo el sello", "rompo el sello", "ataco el sello", "golpeo el sello",
        "uso magia en el sello", "intento destruir el sello",
    ],
}


class IntentDetector:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self._build_index()

    def _build_index(self):
        self.intent_labels = []
        self.intent_embeddings = []
        for intent, examples in INTENT_EXAMPLES.items():
            embeddings = self.model.encode(examples)
            for emb in embeddings:
                self.intent_labels.append(intent)
                self.intent_embeddings.append(emb)
        self.intent_embeddings = np.array(self.intent_embeddings)

    def detect(self, text: str, valid_intents: list, threshold: float = 0.45) -> str:
        """Devuelve la intención detectada o 'otro' si no supera el umbral."""
        query_emb = self.model.encode([text])
        sims = cosine_similarity(query_emb, self.intent_embeddings)[0]
        best_idx = int(np.argmax(sims))
        best_score = sims[best_idx]
        best_intent = self.intent_labels[best_idx]

        if best_score >= threshold and best_intent in valid_intents:
            return best_intent
        # Segunda oportunidad: mejor intención válida aunque no sea la top global
        valid_scores = {
            label: score
            for label, score in zip(self.intent_labels, sims)
            if label in valid_intents
        }
        if valid_scores:
            best_valid = max(valid_scores, key=valid_scores.get)
            if valid_scores[best_valid] >= threshold - 0.1:
                return best_valid
        return "otro"
