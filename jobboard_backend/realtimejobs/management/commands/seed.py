import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from realtimejobs.models import Company, Tag, Category, JobType, JobPost, JobInteraction, JobAlert

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = "Seed the database with sample data."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("🌱 Seeding database..."))

        # Create Users
        users = [User.objects.create_user(email=fake.unique.email(), full_name=fake.name(), password="password123") for _ in range(5)]
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(users)} users"))

        # Create Companies
        companies = [Company.objects.create(name=fake.company(), description=fake.text(), contact_name=fake.name(), contact_email=fake.unique.email()) for _ in range(5)]
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(companies)} companies"))

        # Create Tags
        tag_names = ["Python", "Django", "Remote", "Entry-Level", "Backend", "Frontend"]
        tags = [Tag.objects.create(name=name, slug=slugify(name)) for name in tag_names]
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(tags)} tags"))

        # Create Categories
        category_names = ["Software Development", "Data Science", "Design"]
        categories = [Category.objects.create(name=name, slug=slugify(name)) for name in category_names]
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(categories)} categories"))

        # Create Job Types
        job_type_names = ["Full-time", "Part-time", "Contract", "Freelance", "Internship"]
        job_types = [JobType.objects.create(name=name) for name in job_type_names]
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(job_types)} job types"))

        # Create Job Posts
        jobs = []
        for _ in range(10):
            title = fake.job()
            job = JobPost.objects.create(
                user=random.choice(users),
                company=random.choice(companies),
                title=title,
                slug=slugify(title),
                job_url=fake.url(),
                category=random.choice(categories),
                job_type=random.choice(job_types),
                salary=f"${random.randint(40000, 200000)}",
                description=fake.text(),
                short_description=fake.text(max_nb_chars=200),
                location=fake.city(),
                is_worldwide=random.choice([True, False])
            )
            job.tags.set(random.sample(tags, min(len(tags), random.randint(1, 3))))
            jobs.append(job)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(jobs)} job posts"))

        # Create Job Interactions
        interactions = [JobInteraction.objects.create(user=random.choice(users), job=random.choice(jobs), status=random.choice(["saved", "applied"])) for _ in range(10)]
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(interactions)} job interactions"))

        # Create Job Alerts
        alerts = []
        for user in users:
            alert = JobAlert.objects.create(user=user, email=user.email, is_active=True, location="Remote")
            alert.categories.set(random.sample(categories, 1))
            alert.job_types.set(random.sample(job_types, 1))
            alerts.append(alert)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(alerts)} job alerts"))

        self.stdout.write(self.style.SUCCESS("🎉 Database seeding complete!"))
