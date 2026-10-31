# Fonction ou constance partagées par ScoreEditor et Canvas

def get_note_value(note_type):
    note_values = {
        "ronde": 1,
        "blanche": 0.5,
        "noire": 0.25,
        "croche": 0.125,
        "double-croche": 0.0625,
    }
    return note_values.get(note_type, 0)