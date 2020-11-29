# SCU-Bronco-Buddies
Repository for our COEN 174 project

## Contributors: 
* [Chelsea Fernandes](https://github.com/ccfernandes) - product manager + developer
* [Andrea Horvath](https://github.com/ahorvath12) - developer
* [Zac Hardy](https://github.com/zachardy) - developer

## Problem Statement
Currently the SCU website does not provide a designated community-based section for students to directly ask questions about anything related to SCU (on going events, technology help, and any other concerns). While the SCU website does currently have pages designated for frequently asked questions, it doesn’t allow for specific questions one may have. As a result, student’s may only find an answer to part of the question; there is no personalized response. Students may then experience having to navigate the SCU website for multiple parts of their question, with possibly little luck.

## Our Solution
Our solution is to create a forum accessible through the SCU portal to allow students to ask and answer questions that fellow students may have. This will give students a platform to directly help fellow broncos as soon as possible, without having to wait for an administrator to respond. 

### Developer Notes: 
- make sure you have all the required libraries installed --> see requirements.txt (add to the file whenever you install and use another library)
- all html files go in the templates folder 
- all styling files go in static folder
- forms.py is where we define the forms that we are making (i.e. login, register, create a new thread..etc)
- models.py is where we define the structure of our database tables (i.e. users, posts..etc)
- routes.py is where we define all the url paths. we can use the function name when referring to paths in our html files
