from django.core.validators import RegexValidator
from django.db import models


class State(models.Model):
    name = models.CharField(max_length=35, blank=False)

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=35, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'


class Auditee(models.Model):
    name = models.CharField(max_length=70, blank=False)
    cpf_and_cnpj_regex = RegexValidator(
        regex=r'^\+?1?\d{11}$|^\+?1?\d{14}$',
        message="CPF or CNPJ must be entered in the format: '99999999999'. CPF must have 11 numbers and CNPJ must have 14 numbers.",
    )
    code = models.CharField(
        'CPF/CNPJ',
        validators=[cpf_and_cnpj_regex],
        max_length=14,
        blank=False,
        unique=True,
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=False
    )
    email = models.EmailField(max_length=254, blank=False)
    address = models.CharField(max_length=200, blank=False)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('News', 'News'),
        ('Post', 'Post'),
        ('Comment', 'Comment'),
        ('Document', 'Document'),
        ('Webcache', 'Webcache'),
    ]
    CONTENT_FORMAT_CHOICES = [
        ('Text', 'Text'),
        ('Image', 'Image'),
        ('Hyperlink', 'Hyperlink'),
        ('Vídeo', 'Vídeo'),
    ]
    FAKENEWS_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Investigate', 'Investigate'),
    ]
    CLASSIFICATION_CHOICES = [
        ('Positive', 'Positive'),
        ('Negative', 'Negative'),
        ('Non-procedural Negative', 'Non-procedural Negative'),
        ('Procedural Negative', 'Procedural Negative'),
    ]
    SUSPECT_TYPE_CHOICES = [
        ('News portal', 'News portal'),
        ('Blog', 'Blog'),
        ('Website', 'Website'),
        ('User', 'User'),
    ]

    auditee = models.ForeignKey(Auditee, on_delete=models.CASCADE)
    description = models.TextField(blank=False)
    link = models.CharField(max_length=200, blank=True, null=True)
    platform = models.CharField(max_length=200, blank=False)
    content_type = models.CharField(
        max_length=8, choices=CONTENT_TYPE_CHOICES, blank=False
    )
    content_format = models.CharField(
        max_length=9, choices=CONTENT_FORMAT_CHOICES, blank=False
    )
    fakenews = models.CharField(
        max_length=11, choices=FAKENEWS_CHOICES, blank=False
    )
    attachment = models.FileField()
    suspect_name = models.CharField(max_length=70, blank=False)
    classification = models.CharField(
        max_length=23, choices=CLASSIFICATION_CHOICES, blank=False
    )
    suspect_profile = models.CharField(max_length=200, blank=False)
    suspect_type = models.CharField(
        max_length=11, choices=SUSPECT_TYPE_CHOICES, blank=False
    )
    state = models.ForeignKey(
        State, on_delete=models.SET_NULL, blank=True, null=True
    )
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, blank=True, null=True
    )
    writer_name = models.CharField(max_length=100, blank=False)
    created_date = models.DateField(auto_now_add=True)
