# LMSLite
## These instructions do not include how to install Pycharm or Python. These are for the purpose of getting the project running inside of Pycharm.

## Setup...

### Windows
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
Add the following Environment Variables ; Name: "DJANGO_SETTINGS_MODULE"    Value: "LMSLite.settings"<br/>
Choose the Python Interpretor you created earlier<br/>
Click Apply and OK<br/>
#Project is now set up<br/>



## Google Cloud Setup
### - Use [this link](https://cloud.google.com/storage/docs/creating-buckets) as a reference for creating google cloud storage buckets and starting your google cloud project.<br/>

After installing the reqirements.txt file using pip use [this link](https://cloud.google.com/storage/docs/reference/libraries) to guide you for creating the credentails .json file. After, in pycharm cretae an enviornment variable named **GOOGLE_APPLICATION_CREDENTIALS="[PATH]"** where path is the path to the .json in the project.<br/>
After add these line to the settings.py file
```
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = '[YOUR-BUCKET-NAME]'

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    '[PATH].json')
```
 Once done the project default storage should now be set to your google cloud bucket you can check using
 ```
from django.core.files.storage import default_storage
print default_storage.__class__

>>> <class 'storages.backends.gcloud.GoogleCloudStorage'>
```

## Database Setup
### - Use [this link](https://aws.amazon.com/getting-started/tutorials/create-connect-postgresql-db/) to begin the PostgreSQL database setup on AWS.

Once the databse instance is made change the security settings to public, and allow the IP's of machines expected to have access.
Once done the databse instance can be used via minor edits to the settings.py file as such:
```
'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '[YOUR-DATABASE-NAME]',
        'USER': '[DATABASE-USER]',
        'PASSWORD': '[DATABASE-PASSWORD]',
        'HOST': '[YOUR-HOST-NAME]#usually the 'endpoint' in AWS',
        'PORT': '[YOUR-PORT]',
    }
