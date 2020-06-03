# BinBlogger

◎◎ A comprehensive multi-user blog app ◎◎

## Usage

If you need a **full featured Django Blog** app then you can use this project to develop your Blog by customizing and extending fucntionalities. This project contains almost every fucntionality a blog need.

> [!CAUTION]
> Look through the setup process before using this project so that you can avoid errors.

## Features

> ℹ️ watch the attachted images for better view of features

- Multi User Authentication
- Post CRUD
- [Visual Post editor](demo_images/visual_editor.png) (medium-editor plugin)
- [Featured Post](demo_images/featured_post.png) ( based on views)
- [Popular Posts](demo_images/popular_posts.png) and [Recent posts](demo_images/recent_posts.png)
- Post views count
- [Comments and Reply](demo_images/comments_reply.png) Functionalities
- Categories and [top Categories](demo_images/categories.png)(based on posts count)
- [Tag Functionalities](demo_images/tags.png)
- Profile create on registration
- [Profile Update](demo_images/profile_update.png) after registration
- [Preview image](demo_images/preview.png) before upload
- Auto image optimization on upload.
- [Authors page](demo_images/authors_page.png) with posts and commnets count
- Page for posts of individual [tag](demo_images/tag_posts.png), [category](demo_images/category_posts.png) and [user](demo_images/user_posts.png)
- [Search Fuctionalies](demo_images/search.png)
- User Restictions to view pages
- Delete post-thumbnail when post deleted
- [Admin Panel](demo_images/admin_db.png) with Jquery live search
- [User dashboard](demo_images/user_dashboard.png) with Jquery live search
- [Newsleters](demo_images/newsleters.png)
- [Category multi-select](demo_images/multiselect.png) functionalities (Jquery multiselect plugin)
- [Python Code syntax highlighter](demo_images/codehighlight.png) on Details view(Jquery prism plugin)
- [Redirect alert](demo_images/massage.png)

## Setup Process

> ❗Make sure You have python3 and pip installed on your machine.

### Step 1

1. Create a folder where you want to clone the project.
   - I am creating a folder named ‘example’ in desktop

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

> ℹ️ *Optional but better to use a virtual environment for every project.*

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

1. Create a .env file in the project directory, open it with your favorite text editor and paste the bellow lines

```.file
SECRET_KEY=[YOUR SECRET_KEY]
DEBUG=True
MAILCHIMP_API_KEY=[YOUR MAILCHIMP_API_KEY]
MAILCHIMP_DATA_CENTER=[YOUR MAILCHIMP_DATA_CENTER]
MAILCHIMP_EMAIL_LIST_ID=[YOUR MAILCHIMP_DATA_CENTER]
```

2. Now generate a secret key for your project.

run python on your shell

```bash
python
```

``` python
>>>from django.core.management.utils import get_random_secret_key
>>>get_random_secret_key()
>>>[ YOUR SECRET KEY ]
```

3. Copy the secret key, open .env file again and assign the secret key. If you don't have mailchimp credentials then make sure your file look like this

```.file
SECRET_KEY=YOUR_SECRET_KEY
DEBUG=True
MAILCHIMP_API_KEY=''
MAILCHIMP_DATA_CENTER=''
MAILCHIMP_EMAIL_LIST_ID=''
```

> ⚠️ make sure not to use any space between the equal(=) sign or any quotations(“) for the secret key

> ℹ️
> If you want to setup Mailchimp now then go to this [section](mailchimp_setup.md)

4. You are all setup, let’s migrate now.

```bash
python manage.py migrate
```

5. Create a superuser to rule the site 😎

```bash
python manage.py create superuser

```

> *follow the instructions*

6. Hahh! Long wait. Let’s visit the site now

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and rock 🤘

---

## Contribution and Support

If you want you can to contribute to this project.
For that you need to fork the project.

Support this project giving a star ❤️

## Questions, feedback or Contact ?

Find me on LinkedIn [@mohammadnobinur](https://www.linkedin.com/in/mohammadnobinur/)
