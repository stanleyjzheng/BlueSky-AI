![BlueSky-AI Logo](https://media.discordapp.net/attachments/733836130277130263/734503177566552114/unknown.png)

# BlueSky-AI

The following is the info used in our model:
1. FIRES - FOD_ID as a unique identifier to sort into test and train
3. FIRES - DISCOVERY_DOY is similar to discovery date but as a date of year instead
5. FIRES - STAT_CAUSE_CODE is the statistical cause of the fire. Try to make this optional.
6. FIRES - CONT_DATE is the time the fire was contained or controlled
7. FIRES - CONT_DOY is the date of the year that the fire was contained or controlled
9. FIRES - FIRE_SIZE size of the fire in acres
10. FIRES - FIRE_SIZE_CLASS is the class of fire size. Make sure this is similar to FIRE_SIZE, and if not, average the two for more accuracy.
11. FIRES - LATITUDE/LONGITUDE (JUST TRY THIS, MIGHT NOT BE REGRESSION FRIENDLY)
12. FIRES - STATE BE CAREFUL WITH THE DIFFERENT STATES. 

Output: CONT_DATE, CONT_DOY, FIRE_SIZE, FIRESIZECLASS
Input: DISCOVERY_DOY, STAT_CAUSE_CODE, LATITUDE, LONGITUDE

STAT_CAUSE_CODE 
1 - Lightning
2 - Equipment Use
3 - Smoking
4 - Campfire
5 - Debris Burning
6 - Railroad
7 - Arson
8 - Children
9 - Misc/other
10 - Fireworks
11 - Power Line
12 - Structure
13 - Missing or undefined  N/A

## Inspiration
Our team is composed of individuals from Alberta and California, where wildfires have raged and our cities have been blanketed in smoke. With such regular wildfires and thin resources, how should fire departments prioritize their resources?

## What it does
Taking only the latitude, longitude, start cause, and discovery date, Wildfire-AI uses advanced machine learning to predict the acreage and date the wildfire will be under control. Our momentum design UI is intuitive and user friendly. 

assurefire, firesupplier, acquirefire, Blue-skyAI

## How I built it
Using Panda's and SQLite3, we parsed the SQLITE file the dataset was packaged in. We loaded everything into a dataframe, where we IS THIS THE RIGHT WORD -> referenced every string into a number between 0 and 1. We then coded the model in tensorflow and trained it. After saving the model weights, we wrote a file to load the dataset, take input from the frontend, and output the date the fire was controlled as well as the acreage burned. The frontend was build in React.js, alongside Flask to interface with the 

## Challenges I ran into
None of our team members have used SQL, but the dataset was a SQLITE file. We had some trouble parsing it until we started using Panda's. 

## Accomplishments that I'm proud of

## What I learned

## What's next for Wildfire-AI