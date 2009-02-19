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

def nearby(lst, obj, count=5):
    lst = list(lst)
    l = len(lst)
    try:
        pos = lst.index(obj)
    except ValueError:
        pos = 0
    dist = count / 2
    if pos <= dist:
        return lst[:count]
    if pos >= l - dist:
        return lst[l-count:]
    else:
        return lst[pos-dist:pos+dist+1]

register.filter('nearby', nearby)

def human(lst, field):
    lst = list(lst)
    lst.sort(lambda a,b : cmp(getattr(a,field).lower(),
                              getattr(b,field).lower()))
    return lst

register.filter('human', human)
