from django.db import models


class ModelBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Joke(ModelBase):
    host = models.CharField(max_length=64)
    source = models.CharField(max_length=16)
    date = models.DateField()
    text = models.TextField()

    def __str__(self):
        return '{}-{}-{}'.format(self.host, self.date, self.id)

    def to_dict(self):
        fields = ['id', 'host', 'source', 'date', 'text']
        return {f: getattr(self, f) for f in fields}
