Quiero que me ayudes a importar los datos de los nodos de Pokémon a partir de un JSON con esta estructura (te paso un fragmento de ejemplo):

También genera todos los nodos que puedas a partir del dataset JSON anterior. Después te pasaré otros dos datasets más con la información de los movimientos de cada Pokémon

```json
{
    "bulbasaur": {
        "num": 1,
        "name": "Bulbasaur",
        "types": [
            "Grass",
            "Poison"
        ],
        "genderRatio": {
            "M": 0.875,
            "F": 0.125
        },
        "baseStats": {
            "hp": 45,
            "atk": 49,
            "def": 49,
            "spa": 65,
            "spd": 65,
            "spe": 45
        },
        "abilities": {
            "0": "Overgrow",
            "H": "Chlorophyll"
        },
        "heightm": 0.7,
        "weightkg": 6.9,
        "color": "Green",
        "evos": [
            "Ivysaur"
        ],
        "eggGroups": [
            "Monster",
            "Grass"
        ],
        "tier": "LC"
    },
    "ivysaur": {
        "num": 2,
        "name": "Ivysaur",
        "types": [
            "Grass",
            "Poison"
        ],
        "genderRatio": {
            "M": 0.875,
            "F": 0.125
        },
        "baseStats": {
            "hp": 60,
            "atk": 62,
            "def": 63,
            "spa": 80,
            "spd": 80,
            "spe": 60
        },
        "abilities": {
            "0": "Overgrow",
            "H": "Chlorophyll"
        },
        "heightm": 1,
        "weightkg": 13,
        "color": "Green",
        "prevo": "Bulbasaur",
        "evoLevel": 16,
        "evos": [
            "Venusaur"
        ],
        "eggGroups": [
            "Monster",
            "Grass"
        ],
        "tier": "NFE"
    },
    "venusaur": {
        "num": 3,
        "name": "Venusaur",
        "types": [
            "Grass",
            "Poison"
        ],
        "genderRatio": {
            "M": 0.875,
            "F": 0.125
        },
        "baseStats": {
            "hp": 80,
            "atk": 82,
            "def": 83,
            "spa": 100,
            "spd": 100,
            "spe": 80
        },
        "abilities": {
            "0": "Overgrow",
            "H": "Chlorophyll"
        },
        "heightm": 2,
        "weightkg": 100,
        "color": "Green",
        "prevo": "Ivysaur",
        "evoLevel": 32,
        "eggGroups": [
            "Monster",
            "Grass"
        ],
        "otherFormes": [
            "Venusaur-Mega"
        ],
        "formeOrder": [
            "Venusaur",
            "Venusaur-Mega"
        ],
        "canGigantamax": "G-Max Vine Lash",
        "tier": "PU"
    },
    "venusaurmega": {
        "num": 3,
        "name": "Venusaur-Mega",
        "baseSpecies": "Venusaur",
        "forme": "Mega",
        "types": [
            "Grass",
            "Poison"
        ],
        "genderRatio": {
            "M": 0.875,
            "F": 0.125
        },
        "baseStats": {
            "hp": 80,
            "atk": 100,
            "def": 123,
            "spa": 122,
            "spd": 120,
            "spe": 80
        },
        "abilities": {
            "0": "Thick Fat"
        },
        "heightm": 2.4,
        "weightkg": 155.5,
        "color": "Green",
        "eggGroups": [
            "Monster",
            "Grass"
        ],
        "requiredItem": "Venusaurite",
        "tier": "Illegal",
        "isNonstandard": "Past"
    },
    "venusaurgmax": {
        "num": 3,
        "name": "Venusaur-Gmax",
        "baseSpecies": "Venusaur",
        "forme": "Gmax",
        "types": [
            "Grass",
            "Poison"
        ],
        "genderRatio": {
            "M": 0.875,
            "F": 0.125
        },
        "baseStats": {
            "hp": 80,
            "atk": 82,
            "def": 83,
            "spa": 100,
            "spd": 100,
            "spe": 80
        },
        "abilities": {
            "0": "Overgrow",
            "H": "Chlorophyll"
        },
        "heightm": 24,
        "weightkg": 0,
        "color": "Green",
        "eggGroups": [
            "Monster",
            "Grass"
        ],
        "changesFrom": "Venusaur",
        "tier": "Illegal",
        "isNonstandard": "Past"
    }
}
```	