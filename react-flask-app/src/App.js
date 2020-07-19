import React,{useState} from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [acreage, setAcreage] = useState('0');
  const [currentDate, setCurrentDate] = useState('1/1/2020');
  
  /*window.setInterval(() => {
    /*fetch('/model').then(res => res.json()).then(data => {
      let timestamp = data.time;
      var date = new Date(timestamp * 1000);
      var hours = date.getHours();
      var minutes = "0" + date.getMinutes();
      var seconds = "0" + date.getSeconds();
      var formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
      setCurrentTime(formattedTime);
      var today = new Date();
      var dd = String(today.getDate()).padStart(2, '0');
      var mm = String(today.getMonth()).padStart(2, '0');
      var yyyy = today.getFullYear();
      today = mm + '/' + dd + '/' + yyyy;
      setCurrentDate(today);
    });
  }, 1000);
  fetch('/model', {
    method: "POST",
    body: {'date': '09.02', 'stat': 'Children', 'latitude':'40.656564', 'longitude':'-113.675837'}
  }).then(res => res.json()).then(data => {
    console.log('Data', data);
    setCurrentDate(data.contDate);
    setAcreage(data.acreage);
  })*/
  fetch('/test', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({'date': '09.02', 'stat': 'Children', 'latitude':'40.656564', 'longitude':'-113.675837'}),
    }).then(res => res.json()).then(
      (res) =>{ 
        setCurrentDate(res.contDate);
        setAcreage(res.acreage);
      });
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo"/>
        <h1>{currentDate}</h1>
        <h3>{acreage}</h3>
      </header>
    </div>
  );
}

export default App;