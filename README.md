# dialog_backend
## Install the requirements
$ pip install -r requirements.txt

Used database : POSTGRESQL

###

The backend part of imports images and some data via API to frontend app (VueJS).
Entering admin you can add serie title, description and image. The slug is created itself and it's unique for each serie. 
Serie also has a option to choose if it's sold or active in sale.

You can also add tokens (images) to each serie with title, author and number of image.

The welcome page shows sold serie which you can enter by 'View gallery' button. If you set the serie as 'Active' in it will not appear here -> the idea is to show only sold tokens.
Serie pages shows tokens that are in each serie -> series filtered according to slugs.
