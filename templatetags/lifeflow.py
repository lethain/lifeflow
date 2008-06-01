from django import template
register = template.Library()

def boundary(value, arg):
    """Defines a boundary for an integer. If the value of the integer
    is higher than the boundary, then the boundary is returned instead.

    Example:  {{ comment.depth|:"4" }} will return 4 if the value of
    comment.depth is 4 or higher, but will return 1, 2 or 3 if the
    value of comment.depth is 1, 2 or 3 respectively.
    """
    value = int(value)
    boundary = int(arg)
    if value > boundary:
        return boundary
    else:
        return value

register.filter('boundary', boundary)

