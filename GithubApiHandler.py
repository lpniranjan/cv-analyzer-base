from urllib.parse import urlparse
import inflect

def NumberToWords(number):
    p = inflect.engine()
    return p.number_to_words(number)

