# TODO: Features to be implemented

We use this Google doc to keep track of features that we want to implement: https://docs.google.com/document/d/1r26DPI-wTq0bvvgpTkmwBx5vseDOBYoJpAgOBo8kW_4/edit?usp=sharing

# Intruduction

This folder contains the frontend code for our dreambooth app. 

## Running the script

`npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

## Code Structure

The main files are:

- `src/pages/project.jsx`: The main body of the dashboard, including image uploading, training and image generation.

- `src/components/sidebar.jsx`: The sidebar, including user profile, projects names and settings (e.g., project resetting), and logout button.

- `src/app.js`: The top level component.

- `src/context/ContextProvider.js`: Definition of some global states that can be used across files.
