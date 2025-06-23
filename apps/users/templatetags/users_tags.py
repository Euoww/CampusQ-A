from django import template

register = template.Library()


@register.filter(name='attr')
def add_attr(field, css_class):
    """
    Adds HTML attributes to a Django form field.
    Usage: {{ field|attr:"id:my_id,class:my_class" }}
    """
    attrs = {}
    classes = []
    pairs = css_class.split(',')
    for pair in pairs:
        key_val = pair.split(':', 1)
        if len(key_val) == 2:
            key, val = key_val
            key = key.strip()
            val = val.strip()
            if key == 'class':
                classes.append(val)
            else:
                attrs[key] = val

    if classes:
        # Get existing classes and add new ones
        existing_classes = field.field.widget.attrs.get('class', '').split()
        all_classes = existing_classes + classes
        attrs['class'] = ' '.join(set(all_classes))  # Use set to avoid duplicates

    return field.as_widget(attrs=attrs)