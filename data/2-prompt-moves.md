Luego veremos el tema de la conexión. Ahora quiero que amplíes el código anterior para generar los nodos de movimientos y las asociaciones pertinentes a partir de este extracto de mi dataset JSON de movimientos:

```json
{
    "10000000voltthunderbolt": {
        "num": 719,
        "accuracy": true,
        "basePower": 195,
        "category": "Special",
        "isNonstandard": "Past",
        "name": "10,000,000 Volt Thunderbolt",
        "pp": 1,
        "priority": 0,
        "flags": {},
        "isZ": "pikashuniumz",
        "critRatio": 3,
        "secondary": null,
        "target": "normal",
        "type": "Electric",
        "contestType": "Cool",
        "desc": "Has a very high chance for a critical hit.",
        "shortDesc": "Very high critical hit ratio."
    },
    "absorb": {
        "num": 71,
        "accuracy": 100,
        "basePower": 20,
        "category": "Special",
        "name": "Absorb",
        "pp": 25,
        "priority": 0,
        "flags": {
            "protect": 1,
            "mirror": 1,
            "heal": 1,
            "metronome": 1
        },
        "drain": [
            1,
            2
        ],
        "secondary": null,
        "target": "normal",
        "type": "Grass",
        "contestType": "Clever",
        "desc": "The user recovers 1/2 the HP lost by the target, rounded half up. If Big Root is held by the user, the HP recovered is 1.3x normal, rounded half down.",
        "shortDesc": "User recovers 50% of the damage dealt."
    },
    "accelerock": {
        "num": 709,
        "accuracy": 100,
        "basePower": 40,
        "category": "Physical",
        "name": "Accelerock",
        "pp": 20,
        "priority": 1,
        "flags": {
            "contact": 1,
            "protect": 1,
            "mirror": 1,
            "metronome": 1
        },
        "secondary": null,
        "target": "normal",
        "type": "Rock",
        "contestType": "Cool",
        "desc": "No additional effect.",
        "shortDesc": "Usually goes first."
    },
    "acid": {
        "num": 51,
        "accuracy": 100,
        "basePower": 40,
        "category": "Special",
        "name": "Acid",
        "pp": 30,
        "priority": 0,
        "flags": {
            "protect": 1,
            "mirror": 1,
            "metronome": 1
        },
        "secondary": {
            "chance": 10,
            "boosts": {
                "spd": -1
            }
        },
        "target": "allAdjacentFoes",
        "type": "Poison",
        "contestType": "Clever",
        "desc": "Has a 10% chance to lower the target's Special Defense by 1 stage.",
        "shortDesc": "10% chance to lower the foe(s) Sp. Def by 1."
    }
}
```	