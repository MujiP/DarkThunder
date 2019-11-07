# Heroku

`heroku apps:create darkthunder-1`
Creates a new heroku app, and adds the heroku remote to git in the current directory. The app region gets set to us-east by default, which is best since that's where we are. Make sure the region of an important backing service, like redis, is also in us-east to avoid unnecessary transatlantic latency.

`heroku ps:scale web=1:Free`
Sets the app to run on 1 free type dyno. This will be all we need. With the free type, the app goes to sleep when there's no activity for a certain amount of time, and then the first request takes a few seconds for the app to wake up.

`heroku logs --tail`
Outputs the app logs in near realtime to your command line window. Also useful for seeing print statements you put in.

`git push heroku master`
Heroku is triggered from git. So once you commit, you push to heroku and the app will be running in around 10 seconds. In this example, it will be running the latest commit of the master branch. You can also push other branches to deploy those instead.

`heroku open`
Opens the root url of the app in a web browser window. Useful for getting the app url. You can then append the endpoints right in the browser, which will show you the returned data. Note that you can only test GET requests this way. Or you can use something like Postman.
