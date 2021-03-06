# Path_nodes are enemy walking path from left to right
path_nodes = [
    (-80, 450),
    (180, 430),
    (220, 374),
    (250, 230),
    (280, 200),
    (438, 210),
    (485, 320),
    (485, 500),
    (516, 555),
    (666, 555),
    (684, 510),
    (696, 236),
    (705, 200),
    (785, 170),
    (800, 170)]

bot_tower_locations = [
    # Bottom (in order of ascending y)
    (777, 259),
    (780, 354),
    (779, 451),
    (363, 271),
    (326, 346),
    (402, 347),
    (317, 425),
    (415, 440),
    (214, 505),
    (92,  511),
    (493, 614),
    (681, 637),
    (580, 643)]
top_tower_locations = [
    # Top (in order of ascending y)
    (386, 107),
    (292, 122),
    (694, 122),
    (461, 123),
    (199, 175),
    (543, 198),
    (615, 232),
    (172, 278),
    (567, 299),
    (142, 347),
    (627, 357),
    (571, 413),
    (604, 483),
]

# Dict of tower tower_types for converting to other towers
tower_types = {
    "sell": 0,
    "basic": 1,
    "ice1": 2,
    "fire1": 3,
    "poison1": 4,
    "dark1": 5,
    "ice2": 6,
    "fire2": 7,
    "poison2": 8,
    "dark2": 9
}
