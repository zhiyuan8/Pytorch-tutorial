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
import BookmarkComponent from './bookmark_component';

const BookmarkPage = (props) => {

    // To store the current project id
    const { setActiveTab, activeMenu, setActiveMenu, activeMenuOverlay, setActiveMenuOverlay, setZoomImage, mode, projectList } = useStateContext();

    // bookmarked images list
    const [bookmarkedImages, setBookmarkedImages] = useState([]);

    // we need to write these, otherwise when reloading the page within bookmark, the projectId will be 0 and the activeTab will be 'project'
    useEffect(() => {
        setActiveTab('bookmark');
    });

    // get the bookmarked images from the server when the page is loaded
    useEffect(() => {
        // get the bookmarked images from the server
        const get_bookmarked_images = async () => {
            await fetch(SERVER_URL + '/get-bookmarked-images?'+new URLSearchParams({
                username: props.username
            }), {method: 'GET'})
            .then(response => response.json())
            .then(
                data => {
                    // sort bookmarked images by project id
                    data.output.sort((a, b) => (a.project_id > b.project_id) ? 1 : -1);
                    setBookmarkedImages(data.output);
                }
            );
        }
        get_bookmarked_images();
    }, []);
    
    return (
        <div className={'h-screen bg-main-bg dark:bg-main-dark-bg fixed '+((activeMenu && !activeMenuOverlay)?'w-screenw_minus_240':'w-full')}>

        {/* Show the menu button if the menu is not active */}
        {(!activeMenu || activeMenuOverlay) && <div className="flex justify-between items-center h-50 w-full bg-generation-component-light-bg dark:bg-generation-component-dark-bg">
            <NavButton title="Menu" color={mode=='dark'?'white':'black'}  customFunc={() => {setActiveMenuOverlay(true); setActiveMenu((prevActiveMenu) => !prevActiveMenu )}} icon={<AiOutlineMenu />} />
        </div>}

        {/* The main body of the page */}
        {bookmarkedImages.length > 0 &&
        <div className={'mt-0 bg-main-bg dark:bg-main-dark-bg overflow-y-auto overflow-x-hidden '+((activeMenu && !activeMenuOverlay)?'h-screen':'h-screen_minus_50')}>   
            {/* {bookmarkedProjectList.map((item) => (
                <div className={"flex flex-wrap lg:flex-nowrap justify-center "}>
                        <BookmarkComponent id={item.project_id} 
                            bookmarked_images={bookmarkedImages.filter((image) => image.project_id == item.project_id)}
                            project_name={item.project_name}
                            num_columns={4} set_zoom_image={setZoomImage} mode={mode}
                        />
            </div>))} */}
            
            <div className={"flex flex-wrap lg:flex-nowrap justify-center "}>
                <BookmarkComponent
                    bookmarked_images={bookmarkedImages}
                    num_columns={4} set_zoom_image={setZoomImage} mode={mode} />
            </div>
        </div>}

    </div>
    )
}

export default BookmarkPage;