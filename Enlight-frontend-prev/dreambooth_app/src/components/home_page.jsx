import React, { Component, useState } from 'react'
import { useEffect } from 'react';
import { SERVER_URL } from "../config/config"
import { useNavigate } from "react-router-dom";
import { useStateContext } from '../contexts/ContextProvider';


const HomePage = (props) => {

    const navigate = useNavigate();

    // get the first project id, and then redirect to the project page
    useEffect(() => {
        async function redirect_to_project() {
            var res = await fetch(SERVER_URL + '/get-first-project-id?' + new URLSearchParams({
                username: props.username
            }));
            var res_json = await res.json();
            var project_id = res_json.project_id;
            navigate('/project/' + project_id);
        };
        redirect_to_project();
    }, []);

    return (
    <div></div>
    )
}

export default HomePage;