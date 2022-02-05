# Overview

What I have created here is a simple account creating/editing program which lightly models a banking service. The user is able to create an account which contains a username and password. Once those are set up, the user can then enter in some typical "private information" including an account balance as if they were using this account to store funding. Once an account is created, it is saved to a Firebase project under a collection (called "users") where each username produces a document which contains the user's private information.

The user can then, using the main navigation menu, either display all the account which exist in the Firebase without being able to access private information. Additionally, they have the option to log into an account given that they knew the username and password. Upon accessing their account, they are given access to update and modify their private information, including making deposits and withdrawals, and can even choose to delete their account if desired. This program is coded with a password-access validator and does not use Firebase's authentication service. This is simply because I wanted to practice implementing my own log-in service vs. Firebase's ready-to-use service.

Lastly, this program is written so that each major change and update made to any account is logged to the Firebase for record keeping. An additional notification system will also alert users if an account has a low account_balance. While this notification could be implemented better to be more relevant and user friendly, I wanted it to function more generally for practice purposes.

I chose to write this software because I wanted to gain a basic understanding of how to set up and access a cloud database. On top of that, I wanted to practice inserting information, modifying that information, and deleting that information from a cloud database to ensure that I understood how to use the database correctly. I've taken part of a lot of smaller projects in the past which were shot down because no one in my group understood how to implement a database correctly. Above all else, I wrote this program so that I can be able to implement cloud databases into future projects.

{Provide a link to your YouTube demonstration.  It should be a 4-5 minute demo of the software running, a walkthrough of the code, and a view of the cloud database.}

[Software Demo Video](http://youtube.link.goes.here)

# Cloud Database

What cloud database I used:
* Firebase

What data structure I used:

The Firestore documentation will explain that their data structure is a JSON tree which funnels from a collection to documents which each have multiple attributes. While that description is accurate and pretty easy to understand, I used Firestore project in a key-value data pair manner in my code. I requested a key (the document) which returned dictionary of key-value variables (the attributes). Going one level back, I even requested a collection which returned a dictionary of documents. Of course, this is all thanks to using the .to_dict() function in my code.

# Development Environment

* Google Authentication Service
* Firebase Console
* Python v. 3.9.5
* Visual Studio Code
* VSCode Python Extension "Python"
* VSCode Extention "Code Runner"
* VSCode pip installer + pip firebase-admin installation
* Firebase-admin library
* Time library
* Local device OS library (to set up environ with private key)

# Useful Websites

* [Firebase Console](https://console.firebase.google.com/u/0/)
* [NoSQL Explanation](https://www.guru99.com/nosql-tutorial.html)
* [Firestore Introduction](https://firebase.google.com/docs/firestore)
* [Google Authentication Introduction](https://cloud.google.com/docs/authentication/getting-started)
* [Firebase Documentation](https://firebase.google.com/docs)

# Future Work

* Create another implementation of the same program but using the Firebase built-in authentication system for separate users.
* Re-apply the notification system to send more useful messages/notification to each specific user. *Right now it sends notification messages to anybody using the program because it's not user specific
* Move this program to a web application so that it's not a terminal-based program.