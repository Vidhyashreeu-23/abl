from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from accounts.models import Skill, Interest
from clubs.models import Category, Club, Membership
from events.models import Event
from posts.models import Post
from reviews.models import Review

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample campus data.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        categories = ['Arts & Culture', 'Sports', 'Technology', 'Volunteer', 'Business']
        category_objs = []
        for name in categories:
            category_objs.append(Category.objects.get_or_create(name=name)[0])

        skill_names = ['Leadership', 'Design', 'Python', 'Public Speaking', 'Marketing']
        for name in skill_names:
            Skill.objects.get_or_create(name=name)

        interest_names = ['Robotics', 'Dance', 'Photography', 'Entrepreneurship', 'Sustainability']
        for name in interest_names:
            Interest.objects.get_or_create(name=name)

        users = []
        for i in range(1, 21):
            username = f'student{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@campusconnect.edu',
                    'college': 'University College',
                    'first_name': f'Student{i}',
                    'last_name': 'Campus',
                }
            )
            if created:
                user.set_password('campus123')
                user.save()
            users.append(user)

        clubs = []
        club_names = [
            'Campus Coders', 'Media Makers', 'Green Volunteers',
            'Startup Society', 'Fitness Friends', 'Art Collective',
            'Debate League', 'Music Ensemble', 'Wellness Club', 'Photography Guild'
        ]
        for index, name in enumerate(club_names):
            category = category_objs[index % len(category_objs)]
            creator = users[index]
            club, created = Club.objects.get_or_create(
                name=name,
                defaults={
                    'description': f'{name} is a welcoming campus community for students interested in {category.name.lower()}.',
                    'logo': 'club_logos/default.png',
                    'category': category,
                    'created_by': creator,
                    'social_links': {'website': 'https://campusconnect.example.com'},
                }
            )
            if created:
                club.save()
            clubs.append(club)

        for club in clubs:
            memberships = users[:5]
            for idx, user in enumerate(memberships):
                Membership.objects.get_or_create(
                    user=user,
                    club=club,
                    defaults={'role': 'president' if idx == 0 else 'member'}
                )

        for idx, club in enumerate(clubs):
            for j in range(2):
                event = Event.objects.create(
                    club=club,
                    title=f'{club.name} Event {j + 1}',
                    description=f'Join us for {club.name} event {j + 1}.',
                    location='Campus Center',
                    start_datetime=timezone.now() + timedelta(days=3 + idx + j),
                    end_datetime=timezone.now() + timedelta(days=3 + idx + j, hours=2),
                    created_by=club.created_by,
                    max_attendees=50,
                    is_online=False,
                    meeting_link='',
                )
                event.save()

        for club in clubs:
            for k in range(2):
                post = Post.objects.create(
                    club=club,
                    author=club.created_by,
                    title=f'{club.name} Announcement {k + 1}',
                    content=f'Important update for members of {club.name}.',
                    is_pinned=(k == 0),
                )
                post.save()

        for club in clubs:
            for idx, user in enumerate(users[:3]):
                Review.objects.get_or_create(
                    club=club,
                    user=user,
                    defaults={
                        'rating': random.randint(3, 5),
                        'comment': f'{club.name} is a great group to join!',
                    }
                )

        self.stdout.write(self.style.SUCCESS('Seed data created successfully.'))
