from django.contrib import admin
from .models import Book, Member, Borrow


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'available_copies', 'total_borrowed', 'added_by', 'added_date']
    list_filter = ['available_copies', 'added_date']
    search_fields = ['title', 'author', 'isbn']
    readonly_fields = ['total_borrowed', 'added_by', 'added_date']
    
    def total_borrowed(self, obj):
        return Borrow.objects.filter(book=obj, returned=False).count()
    total_borrowed.short_description = 'Currently Borrowed'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set added_by for new books
            obj.added_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'user', 'joined_date', 'is_active', 'total_borrowed', 'active_borrows']
    list_filter = ['joined_date', 'is_active']
    search_fields = ['name', 'email', 'user__username']
    readonly_fields = ['total_borrowed', 'active_borrows']
    
    def total_borrowed(self, obj):
        return Borrow.objects.filter(member=obj).count()
    total_borrowed.short_description = 'Total Books Borrowed'
    
    def active_borrows(self, obj):
        return Borrow.objects.filter(member=obj, returned=False).count()
    active_borrows.short_description = 'Currently Borrowed'


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'borrowed_by', 'borrow_date', 'return_date', 'returned_by', 'returned', 'days_borrowed']
    list_filter = ['returned', 'borrow_date', 'return_date']
    search_fields = ['book__title', 'book__author', 'member__name', 'member__email', 'borrowed_by__username', 'returned_by__username']
    readonly_fields = ['days_borrowed']
    date_hierarchy = 'borrow_date'
    
    def days_borrowed(self, obj):
        if obj.returned and obj.return_date:
            return (obj.return_date - obj.borrow_date).days
        elif not obj.returned:
            from django.utils import timezone
            return (timezone.now() - obj.borrow_date).days
        return 0
    days_borrowed.short_description = 'Days Borrowed'
