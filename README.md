![BlueSky-AI Logo](https://media.discordapp.net/attachments/733836130277130263/734503177566552114/unknown.png)

# BlueSky-AI
## Inspiration
Our team is composed of individuals from Alberta and California, where wildfires have raged and our cities have been blanketed in smoke. With such regular wildfires and thin resources, how should fire departments prioritize their resources?

## What it does
Taking only the latitude, longitude, start cause, and discovery date, Wildfire-AI uses advanced machine learning to predict the acreage and date the wildfire will be under control. Our momentum design UI is intuitive and user friendly. 

assurefire, firesupplier, acquirefire, Blue-skyAI

## How I built it
Using Panda's and SQLite3, we parsed the SQLITE file the dataset was packaged in. We loaded everything into a dataframe, where we IS THIS THE RIGHT WORD -> referenced every string into a number between 0 and 1. We then coded the model in tensorflow and trained it. After saving the model weights, we wrote a file to load the dataset, take input from the frontend, and output the date the fire was controlled as well as the acreage burned. The frontend was build in React.js, alongside Flask to interface with the 

## Challenges I ran into
None of our team members have used SQL, but the dataset was a SQLITE file. We had some trouble parsing it until we started using Panda's. 

Please see our Devpost for more.
https://devpost.com/software/bluesky-ai
