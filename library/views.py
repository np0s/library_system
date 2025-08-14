from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from .models import Book, Member, Borrow
from .forms import MemberForm, BorrowForm, UserRegistrationForm, UserLoginForm, BookForm
from .utils import is_librarian, is_member, librarian_required, member_required, create_default_groups


def home_redirect(request):
	"""Redirect to appropriate page based on user role"""
	if request.user.is_authenticated:
		if is_librarian(request.user):
			return redirect('library:book_list')
		elif is_member(request.user):
			return redirect('library:my_borrows')
	return redirect('library:login')


def register(request):
	"""User registration view"""
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			# Add user to Member group by default
			member_group, _ = Group.objects.get_or_create(name='Member')
			user.groups.add(member_group)
			
			# Create member profile
			Member.objects.create(
				user=user,
				name=f"{user.first_name} {user.last_name}".strip() or user.username,
				email=user.email or f"{user.username}@example.com"
			)
			
			messages.success(request, 'Account created successfully! Please log in.')
			return redirect('library:login')
	else:
		form = UserRegistrationForm()
	
	return render(request, 'library/register.html', {'form': form})


def user_login(request):
	"""User login view"""
	if request.method == 'POST':
		form = UserLoginForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, f'Welcome back, {user.first_name or user.username}!')
				return redirect('library:home')
	else:
		form = UserLoginForm()
	
	return render(request, 'library/login.html', {'form': form})


@login_required
def user_logout(request):
	"""User logout view"""
	logout(request)
	messages.success(request, 'You have been logged out successfully.')
	return redirect('library:login')


@login_required
def book_list(request):
	"""Home page - list all books with available copies and borrow form"""
	books = Book.objects.all()
	borrow_form = BorrowForm()
	
	if request.method == 'POST' and is_librarian(request.user):
		borrow_form = BorrowForm(request.POST)
		if borrow_form.is_valid():
			member = borrow_form.cleaned_data['member']
			book_id = request.POST.get('book_id')
			if book_id:
				return redirect('library:borrow_book', book_id=book_id, member_id=member.id)
	
	context = {
		'books': books,
		'borrow_form': borrow_form,
		'is_librarian': is_librarian(request.user),
	}
	return render(request, 'library/book_list.html', context)


@librarian_required
def members(request):
	"""Members page - list members and add member form (librarians only)"""
	members = Member.objects.all()
	
	if request.method == 'POST':
		form = MemberForm(request.POST)
		if form.is_valid():
			member = form.save()
			messages.success(request, 'Member added successfully!')
			return redirect('library:members')
	else:
		form = MemberForm()
	
	context = {
		'members': members,
		'form': form,
	}
	return render(request, 'library/members.html', context)


@librarian_required
def borrow_book(request, book_id, member_id):
	"""Borrow a book action (librarians only)"""
	book = get_object_or_404(Book, id=book_id)
	member = get_object_or_404(Member, id=member_id)
	
	if book.available_copies > 0:
		# Create borrow record
		Borrow.objects.create(
			book=book, 
			member=member,
			borrowed_by=request.user
		)
		
		# Decrease available copies
		book.available_copies -= 1
		book.save()
		
		messages.success(request, f'Book "{book.title}" borrowed successfully by {member.name}!')
	else:
		messages.error(request, f'Book "{book.title}" is not available for borrowing.')
	
	return redirect('library:book_list')


@login_required
def return_book(request, borrow_id):
	"""Return a book action"""
	borrow = get_object_or_404(Borrow, id=borrow_id)
	
	# Check permissions
	if not is_librarian(request.user) and borrow.member.user != request.user:
		messages.error(request, 'You can only return your own borrowed books.')
		return redirect('library:my_borrows')
	
	if not borrow.returned:
		# Update borrow record
		borrow.returned = True
		borrow.return_date = timezone.now()
		borrow.returned_by = request.user
		borrow.save()
		
		# Increase available copies
		book = borrow.book
		book.available_copies += 1
		book.save()
		
		messages.success(request, f'Book "{book.title}" returned successfully!')
	else:
		messages.warning(request, 'This book has already been returned.')
	
	if is_librarian(request.user):
		return redirect('library:logs')
	else:
		return redirect('library:my_borrows')


@librarian_required
def logs(request):
	"""Borrow logs page with filters (librarians only)"""
	filter_type = request.GET.get('filter', 'all')
	
	if filter_type == 'returned':
		borrows = Borrow.objects.filter(returned=True)
	elif filter_type == 'unreturned':
		borrows = Borrow.objects.filter(returned=False)
	else:
		borrows = Borrow.objects.all()
	
	context = {
		'borrows': borrows,
		'filter_type': filter_type,
	}
	return render(request, 'library/logs.html', context)


@login_required
def my_borrows(request):
	"""Show logged-in member's own borrow history. Auto-create profile if missing."""
	if is_librarian(request.user):
		return redirect('library:logs')
	
	# Ensure a Member profile exists for the user
	member, _ = Member.objects.get_or_create(
		user=request.user,
		defaults={
			'name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
			'email': request.user.email or f"{request.user.username}@example.com",
		}
	)
	borrows = Borrow.objects.filter(member=member)
	
	context = {
		'borrows': borrows,
		'member': member,
	}
	return render(request, 'library/my_borrows.html', context)


@librarian_required
def add_book(request):
	"""Add new book (librarians only)"""
	if request.method == 'POST':
		form = BookForm(request.POST)
		if form.is_valid():
			book = form.save(commit=False)
			book.added_by = request.user
			book.save()
			messages.success(request, f'Book "{book.title}" added successfully!')
			return redirect('library:book_list')
	else:
		form = BookForm()
	
	return render(request, 'library/add_book.html', {'form': form})


@librarian_required
def edit_book(request, book_id):
	"""Edit book (librarians only)"""
	book = get_object_or_404(Book, id=book_id)
	
	if request.method == 'POST':
		form = BookForm(request.POST, instance=book)
		if form.is_valid():
			form.save()
			messages.success(request, f'Book "{book.title}" updated successfully!')
			return redirect('library:book_list')
	else:
		form = BookForm(instance=book)
	
	return render(request, 'library/edit_book.html', {'form': form, 'book': book})


@librarian_required
def delete_book(request, book_id):
	"""Delete book (librarians only)"""
	book = get_object_or_404(Book, id=book_id)
	
	if request.method == 'POST':
		title = book.title
		book.delete()
		messages.success(request, f'Book "{title}" deleted successfully!')
		return redirect('library:book_list')
	
	return render(request, 'library/delete_book.html', {'book': book})
