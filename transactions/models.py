from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError




class OwnedModel(models.Model):
    owner = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    editable=False
)

    class Meta:
        abstract = True

class Status(OwnedModel):
    name = models.CharField('Статус', max_length=50)
    class Meta:
        unique_together = ('owner', 'name')
    def __str__(self): return self.name

class Type(OwnedModel):
    name = models.CharField('Тип', max_length=50)
    class Meta:
        unique_together = ('owner', 'name')
    def __str__(self): return self.name

class Category(OwnedModel):
    name = models.CharField('Категория', max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories')
    class Meta:
        unique_together = ('owner', 'name', 'type')
    def __str__(self): return self.name

class Subcategory(OwnedModel):
    name = models.CharField('Подкатегория', max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    class Meta:
        unique_together = ('owner', 'name', 'category')
    def __str__(self): return self.name

class Transaction(OwnedModel):
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    date = models.DateField('Дата')
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    amount = models.DecimalField('Сумма (₽)', max_digits=12, decimal_places=2)
    comment = models.TextField('Комментарий', blank=True)

    def clean(self):
        if self.category.type_id != self.type_id:
            raise ValidationError("Категория не относится к выбранному типу.")
        if self.subcategory.category_id != self.category_id:
            raise ValidationError("Подкатегория не относится к выбранной категории.")

    def save(self, *args, **kwargs):
        # При создании автоматически назначаем владельца
        if not self.pk:
            from django_currentuser.middleware import get_current_authenticated_user
            self.owner = get_current_authenticated_user()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} — {self.type} / {self.category} / {self.subcategory} — {self.amount}₽"
