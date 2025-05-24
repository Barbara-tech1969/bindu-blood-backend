# Bindu Blood Bank
A blood donation application api using Django REST Framework.

## Technology
- Framework: Django REST Framework
- Database: Supabase PostgreSQL Database
- Static Storage: Cloudinary Storage
- Host: Koyeb

# API documentation
- The root directory itself contains swagger api documentation
- Schema Download: https://sour-libby-thzone.koyeb.app/schema/
- ReDoc : https://sour-libby-thzone.koyeb.app/schema/redoc/


## Deployment

The first thing to do is to clone the repository:

```bash
  git clone https://github.com/tanzid64/Bindu-Blood-Bank.git
  cd Bindu-Blood-Bank/backend/
```
Create a virtual environment to install dependencies in and activate it:
<br/>
For windows:
```bash
  python -m venv .venv
  .venv\Scripts\activate
```
For Ubuntu:
```bash
  virtualenv .venv
  source .venv/bin/activate
```
Then install the dependencies:

```bash
  pip install -r requirements.txt
```
Create a file name .env in project folder.
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`
`DEBUG`
`EMAIL_HOST_USER`
`EMAIL_HOST_PASSWORD`
`DB_HOST`
`DB_NAME`
`DB_USER`
`DB_PASSWORD`
`CLOUDINARY_CLOUD_NAME`
`CLOUDINARY_API_KEY`
`CLOUDINARY_API_SECRET`

Apply migrations:

```bash
  python manage.py migrate
```
Create an admin account:

```bash
  python manage.py createsuperuser
```
Start the django application::

```bash
  python manage.py runserver
```

That's it! You should now be able to see the demo application.
Browse:
- HomePage:  localhost:8000/
- Admin Panel:  localhost:8000/admin/




Live Link: https://sour-libby-thzone.koyeb.app/