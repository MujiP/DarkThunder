# Bolusaur Python Backend

This is the backend for our app. It is currently hosted on Heroku at https://darkthunder-1.herokuapp.com and uses Redis Cloud .

To see all events in a category, send a GET request to https://darkthunder-1.herokuapp.com/events/{category}, where {category} is any string. You can also visit the page in your browser. I have posted an event in the food category, which you can see here: https://darkthunder-1.herokuapp.com/events/food.

You can post an event by sending a POST request to https://darkthunder-1.herokuapp.com/events/{category}, where {category} is any string. Event information should be sent in the request body as a JSON object. For example, To make the Lunchtime Hangout at Pizza Planet, I POSTed this: 
``` 
{
   "name":"Lunchtime Hangout",
   "location":"Pizza Planet",
   "start_time":"12:00pm",
   "end_time":"1:00pm",
   "description":"Come hangout and eat pizza and we'll talk about how much we love this app!"
} 
```
to https://darkthunder-1.herokuapp.com/events/food.

Required fields are name, location, start_time, & end_time. You can add any number of optional fields (except "id", which is generated automatically). All fields are strings for now.
