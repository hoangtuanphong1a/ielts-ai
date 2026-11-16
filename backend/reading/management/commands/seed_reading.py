from django.core.management.base import BaseCommand
from django.db import transaction

from reading.content import PASSAGES
from reading.models import Passage, Question, QuestionGroup


class Command(BaseCommand):
    help = "Nạp / cập nhật bài đọc mẫu (chạy lại an toàn: câu hỏi được tạo lại theo nội dung mới)"

    @transaction.atomic
    def handle(self, *args, **options):
        for data in PASSAGES:
            passage, created = Passage.objects.update_or_create(
                title=data["title"],
                defaults={k: data[k] for k in ("topic", "difficulty", "minutes", "body")},
            )
            passage.groups.all().delete()
            for order, g in enumerate(data["groups"], start=1):
                group = QuestionGroup.objects.create(
                    passage=passage, order=order, kind=g["kind"], instructions=g["instructions"],
                    options=g.get("options", []), max_words=g.get("max_words"),
                )
                for q in g["questions"]:
                    number, text, answers, explanation, evidence, *rest = q
                    choices = [{"key": k, "text": t} for k, t in rest[0]] if rest else []
                    Question.objects.create(group=group, number=number, text=text, answers=answers,
                                            explanation=explanation, evidence=evidence, choices=choices)
            self.stdout.write(f"{'Created' if created else 'Updated'}: {passage.title}")
