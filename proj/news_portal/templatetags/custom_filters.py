from django import template

register = template.Library()


SLUR_WORDS = ['эко', 'текст']


@register.filter()
def censor(text: str):
    if type(text) is not str:
        raise TypeError('"censor" can be used only with string types')

    for word in SLUR_WORDS:
        redacted = text.replace(word, f'{word[0]} {"*" * (len(word)-1)}')
        redacted = text.replace(word.title(), f'{word[0]} {"*" * (len(word)-1)}')

    return redacted
