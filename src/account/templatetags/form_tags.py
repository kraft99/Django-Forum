from django import template

register = template.Library()


@register.filter
def field_type(bound_field):
	return bound_field.field.widget.__class__.__name__
	


@register.filter
def input_class(bound_field):
	css_class = ''
	if bound_field.form.is_bound:
		if bound_field.errors:
			css_class = 'is-invalid'
		elif field_type(bound_field) != 'PasswordInput':
			css_class = 'is-valid'
	return 'form-control {}'.format(css_class)


"""
@use : (template)

{% load form_tags %}

{{ form.username|field_type }}

Will return:
'TextInput'


{% for field in form %}
  <div class="form-group">
    {{ field.label_tag }}
    {% render_field field class=field|input_class %}
    {% for error in field.errors %}
      <div class="invalid-feedback">
        {{ error }}
      </div>
    {% endfor %}
    {% if field.help_text %}
      <small class="form-text text-muted">
        {{ field.help_text|safe }}
      </small>
    {% endif %}
  </div>
{% endfor %}

"""