import React,{useState, useEffect} from 'react';
import logo from './logo.svg';
import Map from './Map';
var Spinner = require('react-spinkit');


const Results = ({run, startDate, selectedOption, ltd, long}) =>{
    const [loading, setLoading] = useState(false);
    const[data, setData] = useState([0, new Date("October 13, 2013 11:13:00")]);
    const[radius, setRadius] = useState();
    const convertToNormal = (date) => {
        var monthDay = date.getDate();
        var month = date.getMonth() + 1;
        var years = date.getFullYear();
        return `${monthDay}-${month}-${years}`;
    }
    const circleData = [{
        id: 1,
        name: "Park Slope",
        latitude: ltd,
        longitude: long,
    }]

    useEffect(() => {
        setLoading(true);
        const fetchData = async() => {
            console.log(ltd);
            const a = await run(startDate, selectedOption, ltd, long);
            setData(a);
        }
        fetchData();
        setLoading(false);
    })

    circleData[0].circle = {
        radius: (Math.sqrt((data[0]*5152.62)/3.1415)),
        options: {
            strokeColor: "#ff0000"
        }
    }
    
    return loading ? (
        <Spinner name='folding-cube'/>
    ):(
        <div>
            <p style = {{fontSize: '28px'}}>Acres Burnt</p>
            <p style = {{fontSize: '35px'}}>{data[0]}</p>
            <p style = {{fontSize: '28px'}}>End Date</p>
            <p style = {{fontSize: '35px'}}>{convertToNormal(data[1])}</p>
            <Map
                center={{ lat: 1 * ltd, lng: 1 * long}}
                zoom={10}
                places={circleData}
                googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyCf_xsnmKqpegq5y1oL-kOwGziFRauYZTo"
                loadingElement={<div style={{ height: `100%` }} />}
                containerElement={<div style={{ height: `800px` }} />}
                mapElement={<div style={{ height: `100%` }} />}
            />
        </div>
    )

}

export default Results;