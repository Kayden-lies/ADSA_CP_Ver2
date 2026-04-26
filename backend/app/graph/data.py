NODES = {
    "EntryGate": (18.463686, 73.867395),
    "Spine_Junction_1": (18.463627, 73.867702),
    "Spine_Junction_2": (18.463549, 73.867429),
    "Spine_Junction_3": (18.463380, 73.867381),
    "ExitGate": (18.463370, 73.867345),

    "StaffCanteen": (18.463911, 73.867705),
    "MainHub": (18.463952, 73.868112),
    "ConnectorHub": (18.463935, 73.867985),

    "BoatClub": (18.464040, 73.868036),
    "Building1": (18.464265, 73.868036),
    "Arena": (18.464301, 73.868483),
    "B2_Node": (18.463971, 73.868511),
    "Parking": (18.463637, 73.868161),
    "FruitCanteen": (18.463967, 73.868712),

    "B2_Junction": (18.463962, 73.868242),
    "B3_Junction": (18.463767, 73.868265),

    "B3_Entry_1": (18.463752, 73.868405),
    "Library": (18.463488, 73.868461),
    "B3_Entry_2": (18.463374, 73.868433),
    "Canteen_Junction": (18.463187, 73.868434),

    "MainCanteen": (18.463189, 73.868179),
    "FoodStalls": (18.463184, 73.868085)
}

EDGES = [
    ("EntryGate","Spine_Junction_1"),
    ("Spine_Junction_1","Spine_Junction_2"),
    ("Spine_Junction_2","Spine_Junction_3"),
    ("Spine_Junction_3","ExitGate"),

    ("Spine_Junction_1","StaffCanteen"),
    ("StaffCanteen","MainHub"),
    ("StaffCanteen","ConnectorHub"),
    ("ConnectorHub","MainHub"),

    ("MainHub","BoatClub"),
    ("BoatClub","Building1"),
    ("Building1","Arena"),
    ("Arena","B2_Node"),

    ("MainHub","Parking"),
    ("MainHub","B2_Node"),
    ("MainHub","FruitCanteen"),

    ("MainHub","B2_Junction"),
    ("B2_Junction","B2_Node"),
    ("B2_Junction","B3_Junction"),

    ("B3_Junction","B3_Entry_1"),
    ("B3_Entry_1","Library"),
    ("Library","B3_Entry_2"),
    ("B3_Entry_2","Canteen_Junction"),

    ("Canteen_Junction","MainCanteen"),
    ("MainCanteen","FoodStalls"),
    ("MainCanteen","Parking"),

    ("ConnectorHub","FoodStalls")
]