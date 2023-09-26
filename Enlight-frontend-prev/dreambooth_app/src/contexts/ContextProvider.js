import React, { createContext, useContext, useState } from "react";

const StateContext = createContext();


export const ContextProvider = ({ children }) => {
    // whether the sidebar is active
    const [activeMenu, setActiveMenu] = useState(true);

    // whether the sidebar is overlaying on top of the main content
    const [activeMenuOverlay, setActiveMenuOverlay] = useState(false);

    const [screenSize, setScreenSize] = useState(undefined);

    // to store whether to use dark mode
    const [mode, setMode] = useState('dark');

    // the image component that is being zoomed
    const [zoomImage, setZoomImage] = useState(null);

    // the list of project names and their ids
    const [projectList, setProjectList] = useState([]);

    // the list of project names and their ids
    const [currentProjectId, setCurrentProjectId] = useState(30);

    // active tab
    const [activeTab, setActiveTab] = useState('project');


    return (
        <StateContext.Provider 
        value={{activeMenu, setActiveMenu,  screenSize, setScreenSize, 
            activeMenuOverlay, setActiveMenuOverlay,
            mode, setMode,
            zoomImage, setZoomImage,
            projectList, setProjectList,
            activeTab, setActiveTab,
            currentProjectId, setCurrentProjectId
        }}
        >
          {children}
        </StateContext.Provider>
    );

}

export const useStateContext = () => useContext(StateContext);