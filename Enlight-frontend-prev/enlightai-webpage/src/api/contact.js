import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL;

// axios is a library that allows us to make HTTP requests
export default axios.create({
    baseURL: API_URL
});
