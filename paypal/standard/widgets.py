#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode


class ValueHiddenInput(forms.HiddenInput):
    """
    Widget that renders only if it has a value.
    Used to remove unused fields from PayPal buttons.
    """
    def render(self, name, value, attrs=None):
        if value is None:
            return u''
        else:
            return super(ValueHiddenInput, self).render(name, value, attrs)

class ReservedValueHiddenInput(ValueHiddenInput):
    """
    Overrides the default name attribute of the form.
    Used for the PayPal `return` field.
    """
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type)
        if value != '':
            final_attrs['value'] = force_unicode(value)
        return mark_safe(u'<input%s />' % flatatt(final_attrs))

class ItemOptionsInput(ValueHiddenInput):
    """ Displays a list of options on the PayPal button. Each option has a
        different price.

        choices is a tuple of amount/name pairs:
            (('10.00', 'Ten Dollars'),
             ('20.00', 'Twenty Dollars'))
    """
    def render(self, name, value, attrs=None, choices=()):
        if not self.choices:
            return ''

        hiddens = []
        options = []
        count = 0
        hidden = """<input type="hidden" name="option_select%(count)s" value="%(name)s">
                    <input type="hidden" name="option_amount%(count)s" value="%(amount)s">
                 """
        option = '<option value="%(name)s">%(name)s</option>'

        for amount, opt_name in self.choices:
            vars = {'count': count, 'amount': amount, 'name': opt_name}
            options.append(option % vars)
            hiddens.append(hidden % vars)
            count += 1

        output = """<table><tr><td>
                    <input type="hidden" name="on0" value="%(name)s">%(name)s
                    </td></tr><tr><td>
                    <select name="os0">
                    %(options)s
                    </select></table>
                    <input type="hidden" name="option_index" value="0">
                    %(hiddens)s
                """ % {'options': '\n'.join(options),
                       'hiddens': '\n'.join(hiddens),
                       'name': 'Amount'}

        return mark_safe(output)
