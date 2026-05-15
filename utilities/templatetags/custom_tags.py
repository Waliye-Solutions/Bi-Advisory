from django import template

register = template.Library()

@register.filter()
def convert_to_int(value):
    return int(value or 0)


@register.filter()
def number_is_negative(value: int|float):
    try:
        if value < 0:
            return True
        return False
    except:
        return False


@register.filter
def get_item_from_dict(dictionary: dict, key):
    """ Get an item in a dict """
    return dictionary.get(key)
