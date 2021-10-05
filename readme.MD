## This is the code-base of the master thesis of Reyhane Shahmoradi

For this project I determine key positions of the human motor
system using an Intel Realsense D435i. My goal is to get accurate and
robust (X,Y,Z) coordinates of different joints.

###Workflow:
So far
* take and save pictures + depth using ```script```.
* import pictures into openpose program to determine positions
* combine joint positions and depth in ```script2```

Next (in no order):
* perform backprojection
* use openpose API 

###folder declaration
In **scrapyard** we collect old functions for further reference
(not very important). 

In **weird_functions** there are some functions which serve no
direct purpose.



