const tf = require("@tensorflow/tfjs");
const { model } = require("@tensorflow/tfjs");

main('07/19/2020', 'Children', '40.656564', '-113.675837');

async function main(date, STAT_CAUSE_DISC, LATITUDE, LONGITUDE){
    tempDate = daysIntoYear(date)/* This is formatted as mm/dd/yyyy but is flexible for some reason? We should try to consider year when outputting date also. */
    doy = tempDate[0]
    year = tempDate[1]
    STAT_CAUSE_CODE = toint(STAT_CAUSE_DISC)
    tempPredict = await predictModel(doy, STAT_CAUSE_CODE, LATITUDE, LONGITUDE)// Can we explicitly convert lat/long to float?
    fireSize = await tempPredict[0].toFixed(0);
    contDiff = await tempPredict[1].toFixed(0);
    date = await doyIntoDays(contDiff, year+1)
    console.log(date)
    console.log(fireSize)
    //return [fireSize, date] // Make sure we get only the first 10 characters, as we don't care about the hours/minutes/seconds, only the date
}

function daysIntoYear(date){
    var date = new Date(date)
    doy = (Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()) - Date.UTC(date.getFullYear(), 0, 0)) / 24 / 60 / 60 / 1000;
    year = date.getFullYear();// I think this only works if the year is first. 
    return [doy, year]
}

function doyIntoDays(day, year){
    var date = new Date(year, 0)
    return new Date(date.setDate(day))
}

function toint(STAT_CAUSE_DISC) {
    if (STAT_CAUSE_DISC.toLowerCase() == "lightning"){
        STAT_CAUSE_CODE = 1;
    }
    else if (STAT_CAUSE_DISC.toLowerCase() == "equipment use"){
        STAT_CAUSE_CODE = 2; 
    }
    else if (STAT_CAUSE_DISC.toLowerCase() == "smoking"){
        STAT_CAUSE_CODE = 3; 
    }
    else if (STAT_CAUSE_DISC.toLowerCase() == "campfire"){
        STAT_CAUSE_CODE = 4; 
    }
    else if (STAT_CAUSE_DISC.toLowerCase() == "debris burning"){
        STAT_CAUSE_CODE = 5; 
    }
    else if (STAT_CAUSE_DISC.toLowerCase() == "railroad"){
        STAT_CAUSE_CODE = 6; 
    }
    else if (STAT_CAUSE_DISC.toLowerCase() == "arson"){
        STAT_CAUSE_CODE = 7; 
    }
    else if (STAT_CAUSE_DISC.toLowerCase() == "children"){
        STAT_CAUSE_CODE = 8; 
    }
    else if (STAT_CAUSE_DISC.toLowerCase() == "misc/other"){
        STAT_CAUSE_CODE = 9; 
    }
    else if (STAT_CAUSE_DISC.toLowerCase() == "fireworks"){
        STAT_CAUSE_CODE = 10; 
    }
    else if (STAT_CAUSE_DISC.toLowerCase() == "power line"){
        STAT_CAUSE_CODE = 11; 
    }
    else if (STAT_CAUSE_DISC.toLowerCase() == "structure"){
        STAT_CAUSE_CODE = 12; 
    }
    else if (STAT_CAUSE_DISC.toLowerCase() == "missing"){
        STAT_CAUSE_CODE = 13; 
    }
    else{
        STAT_CAUSE_CODE = 13;
    }
    return STAT_CAUSE_CODE
}

async function predictModel (DISCOVERY_DOY, STAT_CAUSE_CODE, LATITUDE, LONGITUDE){
    console.log(DISCOVERY_DOY)
    console.log(STAT_CAUSE_CODE)
    console.log(LATITUDE)
    console.log(LONGITUDE)
    const model = await tf.loadGraphModel("http://localhost:3000/saves/model.json").catch(err => console.log(err))//https://drive.google.com/uc?export=download&id=1SLh4UDSRMH8YXdFd_nWaqKwCc0AlNajX
    DISCOVERY_DOY = DISCOVERY_DOY/366
    STAT_CAUSE_CODE= STAT_CAUSE_CODE/13
    LATITUDE = (Math.abs(LATITUDE)-25)/48
    LONGITUDE = (Math.abs(LONGITUDE)-50)/116
    label = await model.predict(tf.tensor([[[DISCOVERY_DOY, STAT_CAUSE_CODE, LATITUDE, LONGITUDE]]]))
    label = await label.data()
    contained = Math.abs(label[0]*366)
    fireSize = Math.abs(label[1]*606945)
    fireSizeClass = Math.abs(label[2]*7)
    if (contained > DISCOVERY_DOY){
        containDiff = contained-DISCOVERY_DOY;
    }
    else if (contained<DISCOVERY_DOY){
        containDiff = contained-DISCOVERY_DOY+365
    }
    else if (contained == DISCOVERY_DOY){
        containDiff = 365
    }
    else {
        containDiff = 28
    }
    if (fireSizeClass==1){
        fireSizeVerBottom=0;
        fireSizeVerTop=0.25;
    }
    else if (fireSizeClass==2){
        fireSizeVerBottom=0.26;
        fireSizeVerTop=9.99;
    }
    else if (fireSizeClass==3){
        fireSizeVerBottom=10;
        fireSizeVerTop=99.99;
    }
    else if (fireSizeClass==4){
        fireSizeVerBottom=100;
        fireSizeVerTop=299.99;
    }
    else if (fireSizeClass==5){
        fireSizeVerBottom=300;
        fireSizeVerTop=999.99;
    }
    else if (fireSizeClass==6){
        fireSizeVerBottom=1000;
        fireSizeVerTop=4999.99;
    }
    else if (fireSizeClass==7){
        fireSizeVerBottom=5000;
        fireSizeVerTop=150000;
    }
    else {
        fireSizeVerTop = 100000;
        fireSizeVerBottom = 20;
    }
    if (fireSize>fireSizeVerTop){
        fireSize = (fireSizeVerBottom+fireSize)/2;
    }
    else if (fireSize<fireSizeVerBottom*0.75){
        fireSizeAvg = (fireSizeVerTop+fireSizeVerBottom)/2;
        fireSize = (fireSizeAvg + fireSize)/2;
    }
    return [fireSize, containDiff]
}