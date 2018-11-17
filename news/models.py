from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Clase que contiene la información del usuario. Se relaciona con el User que define Django.
    """
    image = models.URLField(max_length=500, blank=True)
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Section(models.Model):
    """
    Representa la clasificación que hace el usuario de sus canales de noticias.
    """
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)

    user = models.ForeignKey(Profile, related_name="sections", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Feed(models.Model):
    """
    Representa al canal de noticias: al periódico. Contiene su información esencial y se relaciona con Section.
    """
    title = models.CharField(max_length=500)
    link_rss = models.URLField(max_length=500)
    link_web = models.URLField(max_length=500)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, blank=True)
    logo = models.URLField(blank=True)

    sections = models.ManyToManyField(Section, related_name="feeds")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title', )


class Item(models.Model):
    """
    Representa a una noticia. Este se relaciona con el feed y por defecto se ordena por la fecha de publicación de
    manera descendente.
    """
    title = models.CharField(max_length=500)
    link = models.URLField(max_length=500)
    description = models.TextField()
    image = models.URLField(max_length=500)
    article = models.TextField()
    pubDate = models.DateTimeField()
    creator = models.CharField(max_length=500)

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pubDate', )

    def __create_status(self):
        for section in self.feed.sections.all():
            Status.objects.get_or_create(user_id=section.user.id, item_id=self.id)

    def on_save(self):
        self.__create_status()


class Status(models.Model):
    """
    Contiene la información de un usuario con respecto a una noticia. Se inicializan a falso los atributos.
    """
    view = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    web = models.BooleanField(default=False)
    like = models.BooleanField(default=False)
    saves = models.BooleanField(default=False)

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="statuses")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="statuses")

    def as_view(self):
        self.view = True
        self.save()

    def as_read(self):
        self.view = True
        self.read = True
        self.save()

    def as_web(self):
        self.web = True
        self.save()

    def as_like(self):
        self.like = True
        self.save()

    def as_unlike(self):
        self.like = False
        self.save()

    def as_save(self):
        self.saves = True
        self.save()

    def as_unsave(self):
        self.saves = False
        self.save()

    def get_score(self):
        if self.like:
            return 10
        elif self.web:
            return 5
        elif self.read:
            return 1
        else:
            return 0

    def __str__(self):
        return "{}-{}: {}/{}/{}/{}/{}".format(self.item.id, self.user.user.username, self.view,
                                              self.read, self.web, self.like, self.saves)


class Keyword(models.Model):
    """
    Representa las palabras claves asociadas a un usuario. Estas servirán para el para el sistema de recomendación.
    """
    term = models.CharField(max_length=250)

    users = models.ManyToManyField(Profile, related_name="keywords")
    items = models.ManyToManyField(Item, related_name="keywords")

    def __str__(self):
        return self.term


class Comment(models.Model):
    """
    Representa un comentario de un usuario en un Item.
    """
    description = models.TextField()
    pubDate = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return "{}-{}".format(self.item.id, self.user.user.username)
