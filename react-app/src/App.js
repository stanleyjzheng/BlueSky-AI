import React, {useState, useEffect} from 'react';
import './index.css';
import logo from './logo.svg';
import Results from './Results';
import DatePicker from 'react-date-picker';
import LocationPicker from './LocationPicker';
const tf = require("@tensorflow/tfjs");
const { model } = require("@tensorflow/tfjs");

const App = () =>{
  const [data, setData] = useState({'data' : [0,1]});
  const [loading, setLoading] = useState(false);
  useEffect(() => {
  })
  return (
    <div class = 'App'>
      <img src="https://media.discordapp.net/attachments/733836130277130263/734525199701115022/unknown.png?width=347&height=324" alt="logo"></img>
      <Form currentData = {data} setData = {setData}/>
    </div>
  )//Put a bit of padding below the blueskyai picture. 

}

const Form = ({setData, currentData}) => {
  const [showResults, setShowResults] = useState(false);
  const [value, onChange] = useState(new Date());//  mm/dd/yyyy in a string
  const [selectedOption, setOption] = useState('Children');
  const [latitude, setLatitude] = useState(0);
  const [longitude, setLongitude] = useState(0);
  const [startDate, setStartDate] = useState('01/01/0000');
  const arr = ["Lightning", "Equipment Use", "Smoking", "Campfire", "Debris Burning", "Railroad", "Arson", "Children", "Misc/other", "Fireworks", "Power Line", "Structure", "Missing"]
  const options = arr.map((val) => {return {value: val, label: val}})
  const hello = async() => {
    //var a = await main()
    var month = value.getMonth() + 1;
    var day = value.getDate();
    var year = value.getFullYear();
    var startInputDate = `${month}/${day}/${year}`;
    setStartDate(startInputDate);
    setShowResults(true);
  }
  return showResults ? (
    <Results run = {main} startDate = {startDate} selectedOption = {selectedOption} ltd = {latitude} 
      long = {longitude}
    />
  ):(
    <form onSubmit={
      hello
    }>
      <div>
        <label className = 'label' for="lname">Start Date</label>
        <DatePicker id = 'date' clearIcon = {null} className = 'input' value = {value} onChange = {onChange}/>
      </div>
      <div class = 'custom-select'>
        <label className = 'label' for="cause">Cause</label>
        <div>
          <select onChange = {(event) => {setOption(event.target.value)}}>
            {arr.map((opt) => {return <option value = {opt}>{opt}</option>})}
          </select>
        </div>
      </div>
      <div style = {{display: 'flex', justifyContent: 'space-evenly', marginBottom: '30px'}}>
        <div style = {{display: 'flex', flexDirection: 'column'}}>
          <label id='lat' htmlFor="lname">Latitude</label>
          <input className = 'locInput' type='number' onChange = {(evt) => setLatitude(evt.target.value)}
          ></input>
        </div>
        <div style = {{display: 'flex', flexDirection: 'column'}}>
          <label id='long' htmlFor="lname">Longitude</label>
          <input class = 'locInput' type='number' onChange = {(evt) => setLongitude(evt.target.value)}
          ></input>
        </div>
      </div>
      <input className = 'input' id = "submitButton" type="submit" value="Submit" />
    </form> 
  )
}

async function main(start_date, STAT_CAUSE_DISC, LATITUDE, LONGITUDE){
  let tempDate = daysIntoYear(start_date)/* This is formatted as dd/mm/yyyy but is flexible for some reason? We should try to consider year when outputting date also. */
  let doy = tempDate[0]
  let year = tempDate[1]
  let STAT_CAUSE_CODE = toint(STAT_CAUSE_DISC)
  let tempPredict = await predictModel(doy, STAT_CAUSE_CODE, LATITUDE, LONGITUDE, year)// Can we explicitly convert lat/long to float?
  let fireSize = await tempPredict[0].toFixed(0);
  let contDiff = await tempPredict[1].toFixed(0);
  let years = tempPredict[2];
  let end_date = await doyIntoDays(contDiff, years);
  //console.log(end_date)
  return [fireSize, end_date] // Make sure we get only the first 10 characters, as we don't care about the hours/minutes/seconds, only the date
}

function daysIntoYear(date){
  var date = new Date(date)
  let doy = (Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()) - Date.UTC(date.getFullYear(), 0, 0)) / 24 / 60 / 60 / 1000;
  let year = date.getFullYear();// I think this only works if the year is first. 
  return [doy, year]
}

function doyIntoDays(day, year){
  var date = new Date(year, 0)
  return new Date(date.setDate(day))
}

function toint(STAT_CAUSE_DISC) {
  let STAT_CAUSE_CODE = 13;
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

async function predictModel (DISCOVERY_DOY, STAT_CAUSE_CODE, LATITUDE, LONGITUDE, year){
  let model = await tf.loadGraphModel("https://stanley-zheng.github.io/BlueSky-AI/saves/model.json").catch(err => console.log(err))//https://drive.google.com/uc?export=download&id=1SLh4UDSRMH8YXdFd_nWaqKwCc0AlNajX
  DISCOVERY_DOY = DISCOVERY_DOY/366
  STAT_CAUSE_CODE= STAT_CAUSE_CODE/13
  LATITUDE = (Math.abs(LATITUDE)-25)/48
  LONGITUDE = (Math.abs(LONGITUDE)-50)/116
  let label = await model.predict(tf.tensor([[[DISCOVERY_DOY, STAT_CAUSE_CODE, LATITUDE, LONGITUDE]]]))
  label = await label.data()
  let contained = Math.abs(label[0]*366)
  let fireSize = Math.abs(label[1]*606945)
  let fireSizeClass = Math.abs(label[2]*7).toFixed(0);
  let containDiff = 0;
  let fireSizeVerBottom = 0;
  let fireSizeVerTop = 0;
  if (contained > DISCOVERY_DOY*366){
      containDiff = contained;
      //console.log('contained>discovery')
  }
  else if (contained<DISCOVERY_DOY*366){
      containDiff = Math.abs(contained)+365;
      year += 1
      //console.log('contained<discovery')
  }
  //console.log(fireSizeClass)
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
      fireSizeVerTop=100000;
  }
  else {
      fireSizeVerTop = 100000;
      fireSizeVerBottom = 20;
  }
  if (fireSize>fireSizeVerTop){
      fireSize = (fireSizeVerBottom+fireSize)/2;
  }
  else if (fireSize<fireSizeVerBottom*0.75){
      let fireSizeAvg = (fireSizeVerTop+fireSizeVerBottom)/2;
      fireSize = (fireSizeAvg + fireSize)/2;
  }
  return [fireSize, containDiff, year]
}

/* <select class='input' name="causeList" id="causeList">
          {arr.map((cause) => {return <option class = 'causeOption' value = {cause}>{cause}</option>})}
        </select> */
export default App;
