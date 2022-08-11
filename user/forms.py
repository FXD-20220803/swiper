from django import forms

from user.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'id', 'dating_sex', 'location', 'min_distance',
            'max_distance', 'min_dating_age', 'max_dating_age',
            'vibration', 'only_match', 'only_play'
        ]

    def clean_max_dating_age(self):
        """对这个字段进行额外的处理"""
        max_dating_age = self.cleaned_data.get('max_dating_age')
        min_dating_age = self.cleaned_data.get('min_dating_age')
        if min_dating_age > max_dating_age:
            raise forms.ValidationError('min_dating_age > max_dating_age')
        else:
            return max_dating_age
