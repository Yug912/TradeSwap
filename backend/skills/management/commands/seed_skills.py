from django.core.management.base import BaseCommand

from skills.models import Skill


SKILLS = [
    "Adobe Photoshop", "Android Development", "AWS", "Baking", "Basketball",
    "Blender", "Blog Writing", "C++", "Canva", "Chess", "Content Writing",
    "Cooking", "Cybersecurity", "Django", "Drawing", "Excel", "Figma",
    "Financial Planning", "French", "Frontend Development", "Guitar", "Hindi",
    "Illustration", "Java", "JavaScript", "Kotlin", "Machine Learning", "Music Theory",
    "Node.js", "Photography", "Piano", "Power BI", "Presentation Skills", "Product Management",
    "Public Speaking", "Python", "React", "Resume Writing", "SEO", "SQL", "Singing",
    "Spanish", "Swimming", "TypeScript", "UI/UX Design", "Video Editing", "Web Development",
    "WordPress", "Yoga", "YouTube Editing",
]


class Command(BaseCommand):
    help = "Create the shared TradeSwap skill catalogue."

    def handle(self, *args, **options):
        created = 0
        for name in SKILLS:
            _, was_created = Skill.objects.get_or_create(name=name)
            created += was_created
        self.stdout.write(self.style.SUCCESS(f"Added {created} skills; catalogue now has {Skill.objects.count()} skills."))
