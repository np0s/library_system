from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from library.utils import create_default_groups
from library.models import Member


class Command(BaseCommand):
    help = 'Set up authentication groups and create default librarian user'

    def handle(self, *args, **options):
        self.stdout.write('Setting up authentication system...')

        # Create default groups
        librarian_group, member_group = create_default_groups()
        self.stdout.write(f'✓ Created groups: {librarian_group.name}, {member_group.name}')

        # Create default librarian user if it doesn't exist
        if not User.objects.filter(username='librarian').exists():
            librarian_user = User.objects.create_user(
                username='librarian',
                email='librarian@library.com',
                password='librarian123',
                first_name='Library',
                last_name='Librarian',
                is_staff=True,
                is_superuser=True
            )
            librarian_user.groups.add(librarian_group)
            self.stdout.write('✓ Created librarian user (username: librarian, password: librarian123)')
        else:
            self.stdout.write('✓ Librarian user already exists')

        # Create default member user if it doesn't exist
        if not User.objects.filter(username='member').exists():
            member_user = User.objects.create_user(
                username='member',
                email='member@library.com',
                password='member123',
                first_name='John',
                last_name='Member'
            )
            member_user.groups.add(member_group)
            # Ensure Member profile exists
            Member.objects.get_or_create(user=member_user, defaults={
                'name': f"{member_user.first_name} {member_user.last_name}".strip() or member_user.username,
                'email': member_user.email or 'member@library.com'
            })
            self.stdout.write('✓ Created member user (username: member, password: member123)')
        else:
            self.stdout.write('✓ Member user already exists')

        self.stdout.write(
            self.style.SUCCESS('Authentication system setup completed successfully!')
        )
        self.stdout.write('\nDefault users:')
        self.stdout.write('- Librarian: username=librarian, password=librarian123')
        self.stdout.write('- Member: username=member, password=member123') 