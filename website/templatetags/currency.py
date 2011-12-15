from django import template
from django.conf import settings
from decimal import Decimal

#The moneyfmt script was taken from the Python decimal recipes.
#See it here - http://docs.python.org/lib/decimal-recipes.html

register = template.Library()




def moneyfmt(value, places=2, curr='', sep='.', dp=',',
             pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<.02>'

    """
    try:
        if value == '':
            return value

        value = Decimal(str(value))

        q = Decimal((0, (1,), -places))    # 2 places --> '0.01'
        sign, digits, exp = value.quantize(q).as_tuple()
        assert exp == -places
        result = []
        digits = map(str, digits)
        build, next = result.append, digits.pop
        if sign:
            build(trailneg)
        if curr:
            build(' ' + unicode(curr))
        for i in range(places):
            if digits:
                build(next())
            else:
                build('0')
        if places>0:build(dp)
        i = 0
        if not digits: build('0') # ,00 yerine 0,00 gostersin diye.
        while digits:
            build(next())
            i += 1
            if i == 3 and digits:
                i = 0
                build(sep)

        if sign:
            build(neg)
        else:
            build(pos)
        result.reverse()
        return ''.join(result)
    except:
        pass

register.filter('currency',moneyfmt)


from random import random

@register.filter()
def rasgele_sayi(hane): return str(random())[2:2+hane]

