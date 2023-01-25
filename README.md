# Mind Meter: A meditation app
![Mind Meter header](https://i.imgur.com/bQf1Iaw.png)

[Try out Mind Meter](http://meetmindmeter.com/)  


## Table of Contents
- [Project Description](https://github.com/ismarjiw/Mind-Meter#project-description)
- [Tech Stack](https://github.com/ismarjiw/Mind-Meter#tech-stack)
- [Features](https://github.com/ismarjiw/Mind-Meter#features)
- [Possible Future Features](https://github.com/ismarjiw/Mind-Meter#possible-future-features)
- [Known Bugs](https://github.com/ismarjiw/Mind-Meter#known-bugs)
- [Installation](https://github.com/ismarjiw/Mind-Meter#installation)


## Project Description
Mind Meter is a web app that helps users log timed meditation sessions, write journal reflections, and listen to calming music all in one space! Users start by creating an account and logging into their profile page. From there, they can choose to start a 5 or 10 minute meditation. While they're meditating, the user also has the option to listen to 4 different sound buttons ranging from rain sounds to etheral beats. If they have a Spotify account, they may also choose to listen to a curated meditation playlist as well. After they meditate, the user can write a journal reflection recording any revelations, thoughts or feelings they had during their meditation session. In addition, there is a handy focused breathing animation the user can reference to help with breath control. To see if it would be a good day to go for a walk or not, the user can enter their zipcode and check to see what their local weather is (weather info coming from Open Weather's API). In addition, the user can reference a bar graph, charting what days they've meditated and for how long each day.

With Mind Meter, anyone can start their meditation journey!

<hr>

**Homepage**

<img src="https://media0.giphy.com/media/3PL3YXsdGLH3BakNsO/giphy.gif?cid=790b7611492fda7080098c644be66c6434f35c5a9d163c79&rid=giphy.gif&ct=g">

**Login page**

<img src="https://media4.giphy.com/media/zemz4fbHCsPYt90nYJ/giphy.gif?cid=790b7611070aadc16075ad1c84996680621fcb6306b0e60a&rid=giphy.gif&ct=g">

**Profile page**

<img src="https://media4.giphy.com/media/GsyWuQAL3AUnrYqecs/giphy.gif?cid=790b76118e8f1ce67aabeeddea491f612d99f5c94344e72f&rid=giphy.gif&ct=g">


## Tech Stack
- Python
- Flask
- Jinja2
- PostgreSQL
- SQLAlchemy
- JavaScript
- React
- Chart.js 
- jQuery
- HTML
- CSS
- Tailwind
- Flowbite
- GSAP

APIs:
- [OpenWeather API](https://openweathermap.org/api)
- [Youtube Player API](https://developers.google.com/youtube/iframe_api_reference)
- [Spotify API/OAuth 2.0](https://developer.spotify.com/documentation/web-api/)
- [Google API/OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)


## Features
- **Create an account, login / logout, and delete account**
- **Start a meditation session with either a 5 or 10 minute meditation**
- **Write a journal reflection after a meditation**
- **Journal page where all past reflections can be reviewed and deleted if chosen**
- **Focused breathing animation to help with breath control**
- **Login to Spotify and listen to a curated meditation playlist that changes daily**
- **Check the weather to see if it's a good day to go for a walk**
- **View on an interactive bar graph what days a meditation was logged and how many minutes per day was spent meditating**


## Possible Future Features
- **Customizable timer that the user can set for their meditation session**
- **Include research / additional reading material users can review to learn more about the benefits of meditation**
- **Asking the user if they would like a text reminder to be sent to them to meditate daily**
- **Instead of having sounds being streamed from Youtube, create play buttons with React that would play a curated sound directly from a file**
- **Add a "how are you feeling today" mood selector where users can choose from different emojis to express their mood for the day**
- **A forum where other meditation users can connect and have discussion**
- **Add personal testimonials to the homepage from other Mind Meter users**


## Known Bugs
- ***Responsiveness***: 
  - The youtube sound buttons take a second to load since it's buffering the videos hosting the sounds in the background. 
- ***Accessibility***: 
  - While I tried to make my app as accessible as I could, given my limited knowledge of accessibility in web design, I need to do further testing and do more research to see what I missed.
- ***Spotify***:
   - After a user logs in, the Spotify player still is in "preview" mode even though it should allow full playback of songs.
   - Playback works on localhost and [Codepen](https://codepen.io/ismarjiw/pen/bGjYyaR) but can't figure out why it's not playing back server side -> need to do further research as to why that is. May be on Spotify's end.


## Installation
To run Mind Meter locally on your computer:
1. **Clone repository to your local computer**
2. **Activate virtual environment**
    ```
    $ cd Mind-Meter
    $ virtualenv env
    $ source env/bin/activate
    ```
3. **Download requirements from requirements.txt**
    ```
    $ pip3 install -r requirements.txt
    ```
4. **Get API key for OpenWeather, Spotify, and Google**
  - [OpenWeather](https://openweathermap.org/api)
  - [Spotify](https://developer.spotify.com/dashboard/) 
  - [Google](https://console.cloud.google.com/)
  - In addition, set the redirect for Spotify in developer tools for your app to http://localhost:5001/redirect and for Google, http://localhost:5001/callback
5. **Store your OpenWeather, Spotify, and Google API key**
  - Create a file called `secrets.sh` in the app directory. Add the code below to the file and replace the text in the quotation marks:
    ```
    export SPOTIPY_REDIRECT_URI=""
    export SPOTIPY_CLIENT_ID=""
    export SPOTIPY_CLIENT_SECRET=""

    export GOOGLE_CLIENT_ID=""

    export OPEN_WEATHER_API_KEY=""
    ```
  - Create another file called `client_secret.json` in the app directory to save JSON client ID data from Google
  - JSON can be downloaded and found under the "Credentials" tab from the Google Cloud API console
    ```
    {
      "web":{
          "client_id":"",
          "project_id":"",
          "auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"","redirect_uris":[
              ""
          ]
      }
    }
    ```
6. **In `server.py`, under flow, change the 'redirect_uri' to http://localhost:5001**
7. **Read the key variables into your shell**
  ```
  $ source secrets.sh
  ```
8. **Create the database**
  ```
  $ python3 seed_data.py
  ```
9. **Start up the Flask server**
  ```
  $ python3 server.py
  ```
10. **Go to http://localhost:5001 in your browser and have fun with Mind Meter!**