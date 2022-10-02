import React, {useState} from "react";
import axios from "axios";
import Button from 'react-bootstrap/Button';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Popover from 'react-bootstrap/Popover';


const IdentityComponent = (identity_id) => {

    const [identity, setIdentity] = useState({});

    const fetchIdentity = (identity_id) => {
        axios.get("http://127.0.0.1:8081/api/identity/" + identity_id["identity_id"])
        .then(res => {
            setIdentity(res.data);
        })
        .catch(err => {
            console.log(err);
        });
    }

    const popover = (
        <Popover id="popover-basic">
          <Popover.Header as="h3">Identity {identity.id}</Popover.Header>
          <Popover.Body>
            <p>{identity.id}</p>
            <p>{identity.uid}</p>
            <p>{identity.fullname}</p>
          </Popover.Body>
        </Popover>
      );

    return (
        <OverlayTrigger trigger="click" placement="right" overlay={popover}>
          <Button variant="success" onClick={() => fetchIdentity(identity_id)}>Identity</Button>
        </OverlayTrigger>
    );
}

export default IdentityComponent;
