from django.core.management.base import BaseCommand

from vocab.models import Word
from writing.models import WritingPrompt

PROMPTS = [
    ("task2", "Remote work",
     "Some people believe that working from home is more productive than working "
     "in an office. To what extent do you agree or disagree?"),
    ("task2", "Technology and children",
     "Children today spend too much time on electronic devices. What are the causes "
     "of this problem and what solutions can you suggest?"),
    ("task2", "Public transport",
     "Governments should invest more money in public transport than in building new "
     "roads. Discuss both views and give your own opinion."),
    ("task1", "Internet usage chart",
     "The chart below shows the percentage of households with internet access in "
     "three countries between 2000 and 2020. Summarise the information by selecting "
     "and reporting the main features, and make comparisons where relevant."),
]

WORDS = [
    ("mitigate", "make something less severe", "Planting trees can mitigate air pollution.", "environment"),
    ("detrimental", "causing harm", "Excessive screen time is detrimental to children's health.", "health"),
    ("prevalent", "widespread in a particular area or time", "Remote work has become prevalent since 2020.", "work"),
    ("alleviate", "make suffering or a problem less severe", "Public transport can alleviate traffic congestion.", "city"),
    ("substantial", "of considerable importance or size", "There was a substantial increase in internet use.", "data"),
    ("advocate", "publicly support", "Many experts advocate stricter regulations.", "society"),
    ("inevitable", "certain to happen", "Technological change is inevitable.", "technology"),
    ("exacerbate", "make a problem worse", "Building more roads may exacerbate congestion.", "city"),
    ("fluctuate", "rise and fall irregularly", "Prices fluctuated throughout the decade.", "data"),
    ("sustainable", "able to be maintained long-term", "We need sustainable energy sources.", "environment"),
    ("curriculum", "subjects in a course of study", "Coding should be part of the school curriculum.", "education"),
    ("productivity", "rate of output per unit of effort", "Flexible hours can boost productivity.", "work"),
]


class Command(BaseCommand):
    help = "Seed sample Writing prompts and vocabulary"

    def handle(self, *args, **options):
        for task_type, title, text in PROMPTS:
            WritingPrompt.objects.get_or_create(
                title=title, defaults={"task_type": task_type, "prompt_text": text}
            )
        for term, definition, example, topic in WORDS:
            Word.objects.get_or_create(
                term=term,
                defaults={"definition": definition, "example": example, "topic": topic},
            )
        self.stdout.write(self.style.SUCCESS(
            f"Seeded {WritingPrompt.objects.count()} prompts, {Word.objects.count()} words"
        ))
