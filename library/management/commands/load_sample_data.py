from django.core.management.base import BaseCommand
from library.models import Book, Member, Borrow
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Load sample data for the library system'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')

        # Create sample books
        books_data = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'isbn': '9780743273565',
                'available_copies': 3
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'isbn': '9780446310789',
                'available_copies': 2
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'isbn': '9780451524935',
                'available_copies': 4
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'isbn': '9780141439518',
                'available_copies': 1
            },
            {
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'isbn': '9780547928241',
                'available_copies': 2
            }
        ]

        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
            if created:
                self.stdout.write(f'Created book: {book.title}')

        # Create sample members
        members_data = [
            {
                'name': 'John Doe',
                'email': 'john.doe@example.com'
            },
            {
                'name': 'Jane Smith',
                'email': 'jane.smith@example.com'
            },
            {
                'name': 'Bob Johnson',
                'email': 'bob.johnson@example.com'
            },
            {
                'name': 'Alice Brown',
                'email': 'alice.brown@example.com'
            }
        ]

        for member_data in members_data:
            member, created = Member.objects.get_or_create(
                email=member_data['email'],
                defaults=member_data
            )
            if created:
                self.stdout.write(f'Created member: {member.name}')

        # Create some sample borrow records
        if Book.objects.exists() and Member.objects.exists():
            book1 = Book.objects.first()
            book2 = Book.objects.all()[1]
            member1 = Member.objects.first()
            member2 = Member.objects.all()[1]

            # Create a returned borrow
            borrow1, created = Borrow.objects.get_or_create(
                book=book1,
                member=member1,
                defaults={
                    'borrow_date': timezone.now() - timedelta(days=5),
                    'return_date': timezone.now() - timedelta(days=2),
                    'returned': True
                }
            )
            if created:
                self.stdout.write(f'Created borrow record: {member1.name} borrowed {book1.title}')

            # Create an active borrow
            borrow2, created = Borrow.objects.get_or_create(
                book=book2,
                member=member2,
                defaults={
                    'borrow_date': timezone.now() - timedelta(days=1),
                    'returned': False
                }
            )
            if created:
                self.stdout.write(f'Created borrow record: {member2.name} borrowed {book2.title}')

        self.stdout.write(
            self.style.SUCCESS('Sample data loaded successfully!')
        ) 