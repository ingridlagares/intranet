from django import template

register = template.Library()


@register.filter(name='is_coordinator')
def is_coordinator(project, user):
    return project.coordenador.id == user.id


@register.filter(name='format_field_name')
def format_field_name(value):
    print(value)
    return value.replace(":", "")


@register.filter('form_field_type')
def form_field_type(ob):
    return ob.__class__.__name__


@register.filter('form_field_tag')
def form_field_tag(field):
    widget = field.field.widget
    field_type = widget.__class__.__name__

    if (field_type == 'Select2MultipleWidget'):
        return field

    node = None

    if (field_type == 'SelectDateWidget'):
        return field

    if (field_type == "Textarea"):
        node = 'textarea'
    else:
        node = 'input'

    base_class = "form-control border-top-0 border-right-0 border-left-0 rounded-0 pl-0"
    if(field.errors):
        base_class += " is-invalid"

    if(field_type == "ClearableFileInput"):
        base_class += " border-bottom-0"

    final_tag = f'{node} class="{base_class}" name="{field.name}"'

    if (hasattr(widget, 'input_type')):
        final_tag += f' type="{widget.input_type}"'
    if (hasattr(field.field, 'max_length')):
        final_tag += f' maxlength="{field.field.max_length}"'
    if (field.field.required):
        final_tag += ' required'

    value = (f'{field.value()}' if field.value() else f'')
    if field_type == 'Textarea':
        return f'<{final_tag}>' + value + f'</{node}>'
    else:
        final_tag += f' value="' + value + f'"'

    return "<" + final_tag + "/>"
