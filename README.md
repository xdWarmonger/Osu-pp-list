# Osu-pp-list
Custom highscorelist for your selected users

osu_highscorelist_api.py is the current file i'm working on. It is still in development.

You need to register an OAuth application on the osu website:  
Account -> Settings -> scroll down -> create new OAuth -> name it (you don't need a callback url).  
Then you need to create a .env file in the same location as the program with the content "client secret:'your_client_secret'"

### To Do:
- improve gui
- automatically load in save file when starting the program
- pandas dataframe from user-jsons.
  - right click-functionality (hide / show columns)
  - delete players from list

