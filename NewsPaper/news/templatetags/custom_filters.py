from django import template

register = template.Library()

CENSOR_WORDS = ['сосед', 'питомец', 'цвет']

@register.filter()
def censor(word):
    if isinstance(word, str):
        for i in CENSOR_WORDS:
            word = word.replace(i[1:], '*' * len(i[1:]))
    else:
        raise ValueError(
            'custom_filters -> censor -> A string is expected, but a different data type has been entered')
    return word