from django import template

register = template.Library()


@register.filter(name='get_text')
def get_text(dictionary, clause_id):

    return dictionary[clause_id]


@register.filter(name='get_index')
def get_index(lst, id):

    return lst[id]

