import csv

from story.models import Passage, Choice, Character, Story, Author

print('creating Author...')
rnorth, _ = Author.objects.get_or_create(
    first_name='Ryan',
    last_name='North',
    twitter_account='@ryanqnorth',
)

Story.objects.all().delete()

print('creating story..')
story, _ = Story.objects.get_or_create(
    title='Romeo and/or Juliet',
    subtitle='A Chooseable-Path Adventure',
    description='What if Romeo never met Juliet? What if Juliet got really buff instead of moping around the castle all day? What if they teamed up to take over Verona with robot suits?',
    published_year='2016',
    author=rnorth,
)
print(f'Created story: {story}')

Passage.objects.all().delete()
Choice.objects.all().delete()

print('creating passages..')
with open('passages.csv') as passages_csv:
    reader = csv.DictReader(passages_csv)
    for row in reader:
        pov_character, _ = Character.objects.get_or_create(
            name=row['pov_character']
        )
        print(f'For character - {pov_character}')
        passage, _ = Passage.objects.get_or_create(
            pov_character=pov_character,
            story=story,            
            name=row['passage_number'],
            description=row['passage_description'],
            is_ending='ending' in row['tags'],
        )
        print(f'Created passage: {passage}')

print('creating choices..')
with open('choices.csv') as choices_csv:
    reader = csv.DictReader(choices_csv)
    for row in reader:
        # print(f'loading choice: {row['from_passage']}-{row['to_passage']}')
        from_passage = Passage.objects.get(
            name=row['from_passage']
        )
        print(f'From: {from_passage}')
        to_passage = Passage.objects.get(
            name=row['to_passage']
        )
        print(f'To: {to_passage}')
        choice, _ = Choice.objects.get_or_create(
            from_passage=from_passage,
            to_passage=to_passage,
            description=row['choice_description'],
            is_main_story=row['is_main_story']=='Y',
        )
        print(f'Created choice: {choice}')
