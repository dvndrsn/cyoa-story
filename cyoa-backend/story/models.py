from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    twitter_account = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Story(models.Model):
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    published_year = models.CharField(max_length=4)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} ({self.published_year})'


class Choice(models.Model):
    from_passage = models.ForeignKey(
        'Passage',
        on_delete=models.CASCADE,
        related_name='to_choices'
    )
    to_passage = models.ForeignKey(
        'Passage',
        on_delete=models.CASCADE,
        related_name='from_choices'
    )
    
    description = models.CharField(max_length=255)
    is_main_story = models.BooleanField()

    def __str__(self):
        return f'{self.from_passage.name}-{self.to_passage.name}: {self.description}'


class Passage(models.Model):
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='passages'
    )
    to_passages = models.ManyToManyField(
        'self',
        through='Choice',
        through_fields=('from_passage', 'to_passage'),
        symmetrical=False,
    )
    pov_character = models.ForeignKey(
        'Character',
        on_delete=models.CASCADE,
        null=True
    )

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    is_ending = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.description}'


class Character(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

