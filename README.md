# Groovetime! (backend)

An application that motivates users to share music that best fits a weekly changing theme—a “Weekly Groove!”.

The need for this app came from how traditional social music platforms focus on listening, archiving music, and discussion. Groovetime! encourages users to think critically about their music choices, participate in a low-commitment weekly event, and interact with others in a fun way with an emphasis on community-driven interpretation. Coupled with a fresh prompt every week and a point system that awards both participation and competitiveness, the app becomes a dynamic and exciting way to share music. 

When a user logs in for the first time, they will create a profile, including a username, bio, and profile image. Once their profile is set up, they will be directed to the main page, which displays the current week’s “Weekly Groove!”.

A Weekly Groove is a prompt set by an admin-level user, and per week, all users can submit up to three video-based submissions that they feel best fit the theme. Users can also rate and comment on other users’ submissions and view how others interpreted the theme. An example of a “Weekly Groove!” prompt could be anything from “I’m bleeding out in the snow…” to “Alien dance party!”.

At the end of each week, the “Weekly Groove!” and related submissions are archived, the highest-rated submission is declared the winner, and a new Weekly Groove is posted. Users receive points to display on their profile that are equal to the the total of average ratings they’ve accumulated from their submissions, with bonus points for being #1 that week.

It will allow me to work with authentication, real-time data, many-to-many relationships, and UI state management, all while building a unique, social music-sharing experience. The many to many comes from the rating system– a submission can have multiple ratings by multiple users, and multiple users can give ratings to multiple submissions.

[Postman Documentation](https://documenter.getpostman.com/view/29718199/2sAYk7S4VD)

[ERD](https://dbdiagram.io/d/groovetime-67b3e549263d6cf9a07eb4d5)

# Installation and Setup

1. Clone repo

_disregard 2-5 if there is a .vscode folder already present within the directory with the following code blocks_

2. Create a ```.vscode``` folder
3. Create a ```launch.json``` AND ```settings.json``` file within the ```.vscode``` folder.
4. Place the following code block within the ```launch.json```. 
```
    {
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Django",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/manage.py",
      "args": [
        "runserver"
      ],
      "django": true,
      "autoReload": {
        "enable": true
      }
    }
  ]
} 
```
_${workspaceFolder} should be the name of the folder that has the settings.py file_

5. Place the following code block within the ```settings.json```.
```
{
  "python.linting.pylintArgs": [
    "--load-plugins=pylint_django",
    "--django-settings-module=groovetime.settings",
  ],
}
```
6. Run ```pipenv shell```
7. Run ```python manage.py startapp groovetimeapi```
8. Run ```python manage.py makemigrations```
9. Run ```python manage.py migrate```
10. Load fixtures in the following order:
    -  ```python manage.py loaddata ratings```
    -  ```python manage.py loaddata groovetime_users```
    -  ```python manage.py loaddata weekly_grooves```
    -  ```python manage.py loaddata groove_submissions```
    -  ```python manage.py loaddata groove_submission_ratings```
    -  ```python manage.py loaddata groove_submission_comments```
11. Confirm successful loading of data within the `db.sqlite3` file.
12. Run ```python manage.py test```

...and that's it!


