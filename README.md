# BinBlogger

◎ A comprehensive multi-user blog app

## Usage

If you need a **full featured Django Blog** app then you can use this project to develop your Blog by customizing and extending fucntionalities. This project contains almost every fucntionality a blog need.

> [!CAUTION]
> Look through the setup process before using this project so that you can avoid errors.

## Features

> [!TIP]
> watch the attachted images for better view of features

- Multi User Authentication
- Post CRUD
- Visual Post editor (medium-editor plugin)
- Featured Post ( based on views)
- Popular Posts and Recent posts
- Post views count
- Comments and Reply Functionalities
- Categories and top Categories(based on posts count)
- Tag Functionalities
- Profile create on registration
- Profile Update after registration
- Preview image before upload
- Auto image optimization on upload.
- Authors page with posts and commnets count
- Page for posts of individual tag, category and user
- Search Fuctionalies
- User Restictions to view pages
- Delete post-thumbnail when post deleted
- Admin Panel with Jquery live search
- User dashboard with Jquery live search
- Newsleters
- Category multi-select functionalities (Jquery multiselect plugin)
- Python Code syntax highlighter on Details view(Jquery prism plugin)

## Setup Process

> [!IMPORTANT]
> Make sure You have python3 and pip installed on your machine.

### Step 1

1. Create a folder where you want to clone the project.
   - I am creating a folder named ‘example’ in desktop*

2. Now navigate to "example" via cmd or terminal

(Mac)

```bash
cd ~/desktop/example
```

(Windows)

 ```shell
cd C:\Users\YourDesktopName\Desktop\example
 ```

### Step 2

*Optional but better to use a virtual environment for every project.*

If don’t have any virtual environment manager installed in your machine then install one. (I will use pipenv)

For installing pipenv run

```bash
pip install pipenv
```

1. Now clone the project and navigate to BinBlogger-master

```bash
git clone git@github.com:m-nobinur/BinBlogger.git
cd BinBlogger-master
```

2. Install all the dependencies for the project.


```bash
pipenv install -r requirements.txt
```

3. Activate the virtual environment

```bash
pipenv shell
```

### Step 3

1. Create a .env file in the project directory open it with your favorite text editor and paste the bellow lines

```.file
SECRET_KEY=[YOUR SECRET_KEY]
DEBUG=True
MAILCHIMP_API_KEY=[YOUR MAILCHIMP_API_KEY]
MAILCHIMP_DATA_CENTER=[YOUR MAILCHIMP_DATA_CENTER]
MAILCHIMP_EMAIL_LIST_ID=[YOUR MAILCHIMP_DATA_CENTER]
```

2. Now generate a secret key for your project.

```bash
python
```

``` python
>>>from django.core.management.utils import get_random_secret_key
>>>get_random_secret_key()
>>>[ YOUR SECRET KEY ]
```

3. Copy the secret key and open .env file again and assign the secret key.If you don't have mailchimp credentials then make sure your file look like this

```.file
SECRET_KEY=YOUR_SECRET_KEY
DEBUG=True
MAILCHIMP_API_KEY=''
MAILCHIMP_DATA_CENTER=''
MAILCHIMP_EMAIL_LIST_ID=''
```

> [!CAUTION]
> make sure not to use any space between the equal(=) sign or any quotations(“) for the secret key

> [!NOTE]
> If you want to setup Mailchimp now then go to this [section](#Mailchimp)

4. You are all setup, let’s migrate now.

```bash
python manage.py migrate
```

5. Create a superuser to rule the site :D

```bash
python manage.py create superuser

```

> *follow the instructions*

6. Hahh! Long wait. Let’s visit the site now

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and rock 🤘
