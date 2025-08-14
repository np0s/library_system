# Library Management System

A complete Django-based Library Management System with authentication, role-based access control, book borrowing/returning functionality, member management, and comprehensive logging.

## ✨ New Features (v2.0)

### 🔐 Authentication & Roles
- **User Authentication**: Login/logout/register with secure forms
- **Role-Based Access Control**:
  - **Librarian**: Can add books, borrow books for members, return books, manage members, and view all logs
  - **Member**: Can log in, view available books, borrow books (if allowed), and view only their own borrow history
- **Secure Permissions**: Only librarians can change `available_copies` and manage inventory

### 🎨 Modern UI with TailwindCSS
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Dark Mode**: Toggle between light and dark themes with persistent preference
- **Modern Icons**: Heroicons for all buttons and actions
- **Beautiful Tables**: Hover effects, search functionality, and colored badges
- **Confirmation Modals**: Safe delete and return actions

### 📱 Enhanced User Experience
- **Member-Specific Pages**: `/my-borrows/` shows only the logged-in member's history
- **Smart Navigation**: Role-based navbar with appropriate links
- **Real-time Search**: Filter books by title, author, or ISBN
- **Status Badges**: Green for available, red for unavailable, blue for returned, orange for borrowed

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 5.1+

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd library_system
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Set up authentication system:**
   ```bash
   python manage.py setup_auth
   ```

4. **Load sample data (optional):**
   ```bash
   python manage.py load_sample_data
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - **Default users:**
     - **Librarian**: username=`librarian`, password=`librarian123`
     - **Member**: username=`member`, password=`member123`
     - **Admin**: username=`admin`, password=`admin123`

## 🔐 Authentication & Roles

### User Types

#### Librarian
- **Full Access**: Can manage all aspects of the library
- **Permissions**:
  - Add, edit, and delete books
  - Borrow books for any member
  - Return books for any member
  - Manage member accounts
  - View all borrow logs
  - Access admin panel

#### Member
- **Limited Access**: Can only manage their own account
- **Permissions**:
  - View available books
  - Return their own borrowed books
  - View their own borrow history
  - Cannot borrow books (librarians must do this)

### Security Features
- **@login_required**: All actions require authentication
- **@librarian_required**: Sensitive actions restricted to librarians
- **Permission Checks**: Members can only return their own books
- **CSRF Protection**: All forms protected against CSRF attacks

## 📱 User Interface

### Dark Mode
- **Toggle Button**: Click the sun/moon icon in the navbar
- **Persistent**: Preference saved in localStorage
- **Automatic**: Adapts all components (tables, forms, buttons)

### Responsive Design
- **Mobile-First**: Optimized for all screen sizes
- **Touch-Friendly**: Large buttons and touch targets
- **Flexible Layout**: Tables adapt to smaller screens

### Navigation
- **Role-Based**: Different links for librarians vs members
- **Smart Redirects**: Users go to appropriate pages based on role
- **Breadcrumbs**: Clear navigation hierarchy

## 📊 Features

### 📚 Book Management
- Add, edit, and view books with title, author, ISBN, and available copies
- Track book availability in real-time
- Automatic copy management when books are borrowed/returned
- Search functionality with instant filtering

### 👥 Member Management
- Register new library members with name and email
- View member details and borrowing history
- Track member activity and statistics
- Role-based member creation (librarians only)

### 🔄 Borrow/Return Workflow
- Borrow books only when copies are available
- Automatic copy count management
- Return books with timestamp tracking
- Comprehensive borrow history logging
- Confirmation modals for safety

### 📈 Admin Interface
- Full Django admin integration
- Advanced filtering and search capabilities
- Statistics and reporting features
- User-friendly management interface

## 🌐 URL Structure

### Public Routes
- `/` - Home page (redirects based on user role)
- `/login/` - User login
- `/register/` - User registration
- `/logout/` - User logout

### Librarian Routes
- `/books/` - Book list and management
- `/books/add/` - Add new book
- `/books/<id>/edit/` - Edit book
- `/books/<id>/delete/` - Delete book
- `/members/` - Member management
- `/logs/` - All borrow logs

### Member Routes
- `/books/` - View available books
- `/my-borrows/` - Personal borrow history

### Shared Routes
- `/return/<borrow_id>/` - Return book (with permission checks)

## 🗄️ Models

### Book
- `title` - Book title
- `author` - Book author
- `isbn` - Unique ISBN identifier
- `available_copies` - Number of available copies
- `added_by` - User who added the book
- `added_date` - When book was added

### Member
- `user` - OneToOneField to Django User (nullable for legacy)
- `name` - Member's full name
- `email` - Unique email address
- `joined_date` - Date when member joined
- `is_active` - Member status

### Borrow
- `book` - Foreign key to Book
- `member` - Foreign key to Member
- `borrowed_by` - User who processed the borrow
- `borrow_date` - When book was borrowed
- `return_date` - When book was returned (nullable)
- `returned_by` - User who processed the return
- `returned` - Boolean flag for return status

## 🔧 Workflow

### For Librarians
1. **Add Books**: Use the "Add Book" button or admin panel
2. **Borrow Books**: Select member and book, click "Borrow"
3. **Return Books**: Find book in logs, click "Return"
4. **Manage Members**: Add/edit members through the interface

### For Members
1. **View Books**: Browse available books on the books page
2. **Return Books**: Go to "My Borrows" and click "Return"
3. **View History**: Check personal borrow history

## 🎨 UI Components

### Badges
- **Green**: Available books, returned books, active members
- **Red**: Unavailable books, inactive members
- **Blue**: Returned books
- **Orange**: Borrowed books

### Icons
- **Heroicons**: Modern, consistent iconography
- **Contextual**: Different icons for different actions
- **Accessible**: Proper ARIA labels and descriptions

### Forms
- **TailwindCSS**: Consistent styling across all forms
- **Validation**: Real-time error messages
- **Dark Mode**: Automatic theme adaptation

## 🔒 Security Notes

- **Authentication Required**: All actions require login
- **Role-Based Access**: Sensitive operations restricted by role
- **CSRF Protection**: All forms protected
- **Permission Checks**: Users can only access their own data
- **Input Validation**: All user inputs validated
- **SQL Injection Protection**: Django ORM prevents SQL injection

## 🛠️ Development

### Running Tests
```bash
python manage.py test
```

### Creating New Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

### Setting Up Authentication
```bash
python manage.py setup_auth
```

### Loading Sample Data
```bash
python manage.py load_sample_data
```

## 🎯 Technology Stack

- **Backend**: Django 5.1
- **Database**: SQLite (default)
- **Frontend**: TailwindCSS (CDN)
- **Icons**: Heroicons
- **Admin**: Django Admin
- **Authentication**: Django Auth System
- **Security**: CSRF, Role-based permissions

## 📝 License

This project is open source and available under the MIT License.

## 🆕 What's New in v2.0

- ✅ Complete authentication system
- ✅ Role-based access control
- ✅ Modern TailwindCSS UI
- ✅ Dark mode support
- ✅ Responsive design
- ✅ Enhanced security
- ✅ Member-specific pages
- ✅ Confirmation modals
- ✅ Real-time search
- ✅ Improved admin interface
   - Decreases available copies by 1
   - Creates a Borrow record
   - Shows success message

### Returning a Book
1. Navigate to the Logs page
2. Find the unreturned book
3. Click "Return" button
4. System automatically:
   - Marks borrow as returned
   - Sets return date to current time
   - Increases available copies by 1

## Admin Features

### Book Admin
- List display: title, author, ISBN, available copies, currently borrowed
- Search by title, author, or ISBN
- Filter by available copies

### Member Admin
- List display: name, email, joined date, total borrowed, active borrows
- Search by name or email
- Filter by joined date

### Borrow Admin
- List display: book, member, borrow date, return date, returned status, days borrowed
- Search by book title/author or member name/email
- Filter by returned status and dates
- Date hierarchy for easy navigation

## Sample Data

The system comes with sample data including:
- 5 popular books with various copy counts
- 4 sample members
- 2 sample borrow records (one returned, one active)

## Technology Stack

- **Backend**: Django 5.1
- **Database**: SQLite (default)
- **Frontend**: Bootstrap 5 (CDN)
- **Icons**: Font Awesome 6
- **Admin**: Django Admin

## Customization

### Adding New Books
- Use the admin interface at `/admin/`
- Or add via the "Add Book" button on the Books page

### Adding New Members
- Use the form on the Members page
- Or add via the admin interface

### Styling
- Modify templates in `library/templates/library/`
- Base template: `base.html`
- Bootstrap 5 classes used throughout

## Security Notes

- CSRF protection enabled
- Form validation on all inputs
- Unique constraints on ISBN and email
- Admin authentication required for sensitive operations

## Development

### Running Tests
```bash
python manage.py test
```

### Creating New Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

## License

This project is open source and available under the MIT License. 