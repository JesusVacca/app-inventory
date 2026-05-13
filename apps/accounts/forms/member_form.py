from django import forms
from apps.accounts.models import Member
from apps.common.utils import FormModelBase, RoleChoices


class MemberForm(FormModelBase):
    custom_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
    )
    class Meta:
        model = Member
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        user = getattr(self.request, 'user', None)
        super().__init__(*args, **kwargs)

        if user and user.role != RoleChoices.Admin:
            self.fields['role'].choices = (
                (i,i.label)
                for i in RoleChoices
                if i == RoleChoices.Cliente
            )




    def save(self, commit=True):
        instance = super().save(commit=False)
        custom_password = self.cleaned_data.get('custom_password', None)
        role = self.cleaned_data.get('role', None)
        if not self.instance.pk and role == RoleChoices.Cliente:
            instance.set_password('<PASSWORD>')
        elif custom_password:
            instance.set_password(custom_password)
        if commit:
            instance.save()
        return instance
