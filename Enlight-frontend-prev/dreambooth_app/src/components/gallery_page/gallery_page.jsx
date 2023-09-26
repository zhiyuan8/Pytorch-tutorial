import React, { Component, useEffect, useState } from 'react'
import { AiOutlineMenu } from 'react-icons/ai';
import { useStateContext } from '../../contexts/ContextProvider';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';
import { SERVER_URL } from "../../config/config"
import Box from '@mui/material/Box';
import { ImageList, ImageListItem } from '@mui/material';
import close_icon from '../../data/close-icon.svg';
import image_download_icon from '../../data/image-download.svg';
import NavButton from './nav_button';
import GalleryComponent from './gallery_component';

const GalleryPage = (props) => {

    // To store the current project id
    const { setActiveTab, setProjectId, activeMenu, setActiveMenu, activeMenuOverlay, setActiveMenuOverlay, setZoomImage, mode, projectList } = useStateContext();

    // we need to write these, otherwise when reloading the page within gallery, the projectId will be 0 and the activeTab will be 'project'
    useEffect(() => {
        setActiveTab('gallery');
    });

    return (
        <div className={'h-screen bg-main-bg dark:bg-main-dark-bg fixed '+((activeMenu && !activeMenuOverlay)?'w-screenw_minus_240':'w-full')}>

        {/* Show the menu button if the menu is not active */}
        {(!activeMenu || activeMenuOverlay) && <div className="flex justify-between items-center h-50 w-full bg-generation-component-light-bg dark:bg-generation-component-dark-bg">
            <NavButton title="Menu" color={mode=='dark'?'white':'black'}  customFunc={() => {setActiveMenuOverlay(true); setActiveMenu((prevActiveMenu) => !prevActiveMenu )}} icon={<AiOutlineMenu />} />
        </div>}

        {/* The main body of the page */}
        <div className={'mt-0 bg-main-bg dark:bg-main-dark-bg overflow-y-auto overflow-x-hidden '+((activeMenu && !activeMenuOverlay)?'h-screen':'h-screen_minus_50')}>
            <GalleryComponent product={'product'}/>
            {/*{projectList.map((item) => (*/}
            {/*    <div className={"flex flex-wrap lg:flex-nowrap justify-center "}>*/}
            {/*            <GalleryComponent project_id={item.project_id} project_name={item.project_name} username={props.username} num_columns={4} set_zoom_image={setZoomImage} mode={mode}/>*/}
            {/*</div>))}*/}
        </div>

    </div>
    )
}

export default GalleryPage