from django.db import models


class Story(models.Model):
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    published_year = models.CharField(max_length=4)
    author = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.author} - {self.title}'


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
    # from_passages = models.ManyToManyField(
    #     'self',
    #     through='Choice',
    #     through_fields=('to_passage', 'from_passage'),
    #     symmetrical=False,
    # )
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

