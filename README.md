# LMSLite
These instructions do not include how to install Pycharm or Python. These are for the purpose of getting the project running inside of Pycharm.

Setup...

Install/Setup Pycharm Professional Version<br/>
Install Python 3.6 or later<br/>
Restart computer<br/>
Launch Pycharm<br/>
Click "Check out from Version Control"<br/>
Choose "Git" from the drop-down list<br/>
Enter the GitHub URL and the Directory you wish the project to be stored<br/>
Click "Test" to make sure the connect is good, Proceed if Test passes<br/>
#Project should be open at this point<br/>
Go to File : Settings : "Project: LMSLite" : "Project Interpretor"<br/>
Click the gear icon and click "Add"<br/>
Under "Virtualenv Environment" choose "Existing environment"<br/>
Click the LOV and select your python.exe file<br/>
Click ok and ok again<br/>
Click the + button on the right side of the setting pane (you should still be in the Project Interpreter at this point)<br/>
Search "Django" and click "Install Package"<br/>
Wait for the package to completely install (Pycharm normally has a status bar toward the bottom of the application)<br/>
Exit Settings<br/>

Click "Edit Configurations" in the toolbar<br/>
Click the + button and choose Django server<br/>
Enable Run browser<br/>
Add the following Environment Variables ; Name: DJANGO_SETTINGS_MODULE    Value: LMSLite.settings<br/>
Choose the Python Interpretor you created earlier<br/>
Click Apply and OK<br/>
#Project is now set up<br/>
