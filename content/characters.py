from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Race:
    name: str
    description: str
    stat_bonuses: Dict[str, int]
    lore: str

@dataclass
class CharClass:
    name: str
    description: str
    stat_bonuses: Dict[str, int]
    weapon: str
    lore: str

RACES = {
    "humano": Race(
        name="Humano",
        description="Versátil y ambicioso, los humanos dominan Faerûn por su adaptabilidad.",
        stat_bonuses={"fuerza": 1, "destreza": 1, "inteligencia": 1, "carisma": 1},
        lore="Tu linaje no porta magia antigua ni sangre de gigante, pero tu determinación no conoce límites.",
    ),
    "elfo": Race(
        name="Elfo",
        description="Gráciles y de larga vida, los elfos perciben lo que otros no pueden ver.",
        stat_bonuses={"destreza": 2, "inteligencia": 2},
        lore="Tus ojos han visto el bosque de Cormanthor antes de que los humanos construyeran sus primeras ciudades.",
    ),
    "enano": Race(
        name="Enano",
        description="Resistentes y tercos, los enanos son tan duros como la piedra que tallan.",
        stat_bonuses={"fuerza": 2, "vida": 3},
        lore="Las minas de Mithral Hall corren por tu sangre. Cada golpe que das lleva el peso de siglos de tradición.",
    ),
    "semiorco": Race(
        name="Semiorco",
        description="Portadores de sangre orca, su fuerza bruta intimida incluso a los veteranos.",
        stat_bonuses={"fuerza": 3, "vida": 2},
        lore="Llevas la marca de Gruumsh, pero eliges tu propio destino. Eso te hace más peligroso que cualquier orco.",
    ),
    "mediano": Race(
        name="Mediano",
        description="Pequeños y sigilosos, los medianos tienen suerte donde otros tienen fuerza.",
        stat_bonuses={"destreza": 3, "carisma": 1},
        lore="Tu tamaño te ha enseñado a moverte en las sombras. Lo que te falta en estatura lo ganas en astucia.",
    ),
    "drow": Race(
        name="Drow",
        description="Elfos oscuros del Underdark, maestros de la magia y el veneno.",
        stat_bonuses={"destreza": 2, "inteligencia": 3},
        lore="Naciste bajo la mirada de Lolth, pero rechazaste sus telarañas. Ahora caminas en la superficie, donde la luz duele y los secretos abundan.",
    ),
}

CLASSES = {
    "guerrero": CharClass(
        name="Guerrero",
        description="Maestro del combate cuerpo a cuerpo. Resuelve los problemas con acero.",
        stat_bonuses={"fuerza": 3, "vida": 2},
        weapon="espada larga",
        lore="Has sobrevivido cien batallas. Una mazmorra más no te asustará.",
    ),
    "mago": CharClass(
        name="Mago",
        description="Doblegador del tejido arcano. Conocimiento es poder.",
        stat_bonuses={"inteligencia": 4},
        weapon="báculo de roble",
        lore="Tu grimorio contiene hechizos que podrían arrasar ciudades. Si supieras cuándo usarlos.",
    ),
    "pícaro": CharClass(
        name="Pícaro",
        description="Sombras y sigilo. Golpea primero, pregunta después.",
        stat_bonuses={"destreza": 3, "carisma": 1},
        weapon="daga envenenada",
        lore="Nadie espera al pícaro. Esa es exactamente la ventaja que necesitas.",
    ),
    "clérigo": CharClass(
        name="Clérigo",
        description="Canal de poder divino. Cura aliados, destruye no-muertos.",
        stat_bonuses={"vida": 3, "carisma": 2},
        weapon="maza sagrada",
        lore="Tu dios te ha elegido para esta misión. O eso esperas que sea verdad cuando llegue el momento.",
    ),
    "bárbaro": CharClass(
        name="Bárbaro",
        description="Furia encarnada. Cuanto más daño recibe, más peligroso se vuelve.",
        stat_bonuses={"fuerza": 4, "vida": 1},
        weapon="hacha de guerra",
        lore="La rabia que llevas dentro no es una debilidad. Es el arma más afilada de tu arsenal.",
    ),
    "paladín": CharClass(
        name="Paladín",
        description="Guerrero sagrado que combina espada y fe. Imparable en la batalla justa.",
        stat_bonuses={"fuerza": 2, "vida": 2, "carisma": 1},
        weapon="espadón bendecido",
        lore="Tu juramento te da fuerza que ningún entrenamiento podría igualar. Que los dioses te acompañen.",
    ),
}

BASE_STATS = {
    "fuerza": 5,
    "destreza": 5,
    "inteligencia": 5,
    "carisma": 5,
    "vida": 10,
}

def build_stats(race_key: str, class_key: str) -> Dict[str, int]:
    stats = BASE_STATS.copy()
    for attr, bonus in RACES[race_key].stat_bonuses.items():
        stats[attr] = stats.get(attr, 0) + bonus
    for attr, bonus in CLASSES[class_key].stat_bonuses.items():
        stats[attr] = stats.get(attr, 0) + bonus
    return stats
