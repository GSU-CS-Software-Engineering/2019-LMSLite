# LMSLite
These instructions do not include how to install Pycharm or Python. These are for the purpose of getting the project running inside of Pycharm.

Setup...

Install/Setup Pycharm Professional Version
Install Python 3.6 or later
Restart computer
Launch Pycharm
Click "Check out from Version Control"
Choose "Git" from the drop-down list
Enter the GitHub URL and the Directory you wish the project to be stored
Click "Test" to make sure the connect is good, Proceed if Test passes
#Project should be open at this point
Go to File : Settings : "Project: LMSLite" : "Project Interpretor"
Click the gear icon and click "Add"
Under "Virtualenv Environment" choose "Existing environment"
Click the LOV and select your python.exe file
Click ok and ok again
Click the + button on the right side of the setting pane (you should still be in the Project Interpreter at this point)
Search "Django" and click "Install Package"
Wait for the package to completely install (Pycharm normally has a status bar toward the bottom of the application)
Exit Settings

Click "Edit Configurations" in the toolbar
Click the + button and choose Django server
Enable Run browser
Add the following Environment Variables ; Name: DJANGO_SETTINGS_MODULE    Value: LMSLite.settings
Choose the Python Interpretor you created earlier
Click Apply and OK
#Project is now set up
