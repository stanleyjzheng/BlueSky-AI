import React, {Fragment} from "react";
import {
  withGoogleMap,
  GoogleMap,
  withScriptjs,
  Marker,
  Circle
} from "react-google-maps";

const Map = props => {
    return (
      <GoogleMap
        defaultZoom={props.zoom}
        defaultCenter={props.center}
      >
        {props.places.map(place => {
          return (
            <Fragment key={place.id}>
              <Marker
                position={{
                  lat: parseFloat(place.latitude),
                  lng: parseFloat(place.longitude)
                }}
              />
              {place.circle && <Circle
                defaultCenter={{
                  lat: parseFloat(place.latitude),
                  lng: parseFloat(place.longitude)
                }}
                radius={place.circle.radius}
                options={place.circle.options}
              />}
            </Fragment>
          );
        })}
      </GoogleMap>
    );
}

export default withScriptjs(withGoogleMap(Map));