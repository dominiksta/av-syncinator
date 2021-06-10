"""
(Very) simple localisation. i18n seemed overkill.
"""

LOCALE = 'en'

def set_locale(locale: str) -> None:
    global LOCALE
    LOCALE = locale

def translate(msg: str) -> str:
    global LOCALE
    if LOCALE not in localisation: raise Exception("Unknown Locale")
    if msg in localisation[LOCALE]:
        return localisation[LOCALE][msg]
    else:
        return msg

localisation = {
    'en': {},
    'de': {
        'AV Sync accuracy': 'AV Sync Genauigkeit',
        'Time Difference [ms]': 'Zeitunterschied [ms]',
        'Measured Data': 'Messwerte',
        'Average': 'Durchschnitt',
        'Nr. of detected white noise + white video':
            'Nr. gefundenes weißes rauschen + weißes bild',
    },
}