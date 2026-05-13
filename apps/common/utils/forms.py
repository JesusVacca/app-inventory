from django import forms
from django.utils.safestring import mark_safe


class FormModelMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__load_styles()

    def __load_styles(self):
        for name,field in self.fields.items():
            field.widget.attrs.update({'class': 'form__input'})

    def as_custom_form(self):
        html = ''

        for field in self.fields:
            current_field = self[field]
            required = current_field.field.required
            has_error = bool(current_field.errors)
            error_message = ''
            if has_error:
                error_message = f'''
                    <p class="form__error">{current_field.errors[0]}</p>
                '''
                current_field.field.widget.attrs.update({'class': 'form__input form__input--error'})
            html +=f'''
                <div class="form__group">
                    <label for="{current_field.id_for_label}" class="form__label" data-required="{True if required else False}" >{current_field.label}</label>
                    {current_field}
                    {error_message}
                </div>
            '''

        return mark_safe(html)

class FormModelBase(FormModelMixin, forms.ModelForm):...
