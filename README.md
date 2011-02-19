ERA Paper Review System
========================

ERA is a system for creating custom forms, for paper reviews, and then storing them. ERA reviews can be picked up and modified at any time.

This rewrite of ERA is build on top of Google app engine, in Python. For more information: http://code.google.com/appengine/docs/python/overview.html

How to Deploy
--------

It's easy to deploy your own instance of ERA on Google App Engine. All that is necessary is to modify the application name in app.yaml. Set it to a name of an application you have registered with app engine (you can do so at http://appengine.google.com), and then visit the /config_db URL, which generates the prompts from config_db.py.

Description of Files
---------

+ app.yaml contains the App Engine application name, as mentioned above. It also runs config_db.py, and limits access to administrator accounts, as designated in the App Engine settings panel.
+ config_db.py lays out the workflow for the prompts to be shown to the reviewer. Edit this file and then visit the /config_db URL as an administrator to change prompts.
+ era_db.py interfaces with the app engine Datastore.
+ main.py contains most of the logic, including processing the answers given by a reviewer.
+ /templates/ contains simple HTML templates.
+ /templates/base.html contains the HTML inserted on every page. Include a CSS file here to style the entire application to your liking.
+ /templates/index.html contains the first HTML file shown to a reviewer. This would be a good place to write advice to all reviewers, before beginning their review.
+ /templates/done.html contains the HTML shown when a reviewer completes their review.
+ /tornado is the Tornado, the Python web framework.