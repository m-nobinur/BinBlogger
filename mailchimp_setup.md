# Mailchimp Setup for Newsleters

If you don't have a mailchimp account then sign up for one or login to your mailchimp account.

1. After login go to account section then extras. Click on extras, you will see Api key. Click on it.

2. Copy the mailchimp api key

3. Now assign your Api key to MAILCHIMP_API_KEY

4. Assign last three digit of your Api key to MAILCHIMP_DATA_CENTER.(like: us7,us1)

5. Go to Audience section then 'audience name and defaults' settings of your mailchimp account there you will get your Audience ID

6. Assign the Audience ID to MAILCHIMP_EMAIL_LIST_ID

After completing the steps your .env file will look like as bellow

```.file
SECRET_KEY=YOUR_SECRET_KEY
DEBUG=True
MAILCHIMP_API_KEY=YOUR_MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER=YOUR_MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID=YOUR_MAILCHIMP_EMAIL_LIST_ID
```

> ⚠️ make sure not to use any space between the equal(=) sign or any quotations(“) for the keys or ids

---

## Contribution and Support

If you want you can to contribute to this project.
For that you need to fork the project.

Support this project giving a star ❤️

## Questions, feedback or Contact ?

Find me on LinkedIn [@mohammadnobinur](https://www.linkedin.com/in/mohammadnobinur/)
