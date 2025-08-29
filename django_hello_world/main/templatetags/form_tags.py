from django import template
register = template.Library()

@register.filter(name='addclass')
def addclass(field, css):
    """Ajoute une classe CSS à un champ de formulaire."""
    return field.as_widget(attrs={'class': css})
    