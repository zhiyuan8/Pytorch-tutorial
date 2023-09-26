import React, { useEffect } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import ProjectPage  from './components/project_page/project_page';
import BookmarkPage from './components/bookmark_page/bookmark_page';
import GalleryPage from './components/gallery_page/gallery_page';
import Sidebar from './components/sidebar'
import HomePage from './components/home_page'
import { SERVER_URL } from './config/config';
import { useAuth0 } from '@auth0/auth0-react';
import './App.css'

import { useStateContext } from './contexts/ContextProvider'

import CropComponent from './components/project_page/crop_component';


const App = () => {

  const { activeMenu, setActiveMenu, activeMenuOverlay, setActiveMenuOverlay, screenSize, setScreenSize, mode, setMode, zoomImage, setZoomImage } = useStateContext();

  // keep track of window size
  useEffect(
    () => {
      const handleResize = () => setScreenSize(window.innerWidth);
      window.addEventListener('resize', handleResize);
      handleResize();
      return () => window.removeEventListener('resize', handleResize);
    }, []
  );

  // set activeMenu to false if window size is less than 1200px
  useEffect(() => {
    if (screenSize <= 1200) {
      // if the menu is overlayed, we don't want to set activeMenu to false
      if (!activeMenuOverlay) {
        setActiveMenu(false);
      }      
    } else {
      // we always set activeMenuOverlay to false if the window size is greater than 1200px
      setActiveMenu(true);
      setActiveMenuOverlay(false);
    }
  }, [screenSize]);  

  const { isLoading, isAuthenticated, loginWithRedirect, user } = useAuth0();

  useEffect(() => {
      (async function login() {
        if (!isLoading && !user && !isAuthenticated) {
          await loginWithRedirect();
        }
      })();
    }, [isLoading, user, isAuthenticated]);


  // get the initial mode
  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(SERVER_URL + '/get-user-mode-preference?' + new URLSearchParams({
        username: user.email,
      }, {method: 'GET'}));
      const data = await response.json();
      setMode(data.mode);
    }
    if (user)
    {fetchData();}
  }, [user]);

  return (
      <div>
        {isAuthenticated && (
          <div className={mode}>
            <BrowserRouter>
              <div className="flex bg-main-bg dark:bg-main-dark-bg">

                {/* Here's the sidebar */}
                <div className={'z-40 w-60 fixed'+(activeMenu?' left-0':' -left-60')
                +((screenSize <= 1200)?' transition-all duration-300':'')
                +((zoomImage!=null)?' blur-sm pointer-events-none':'')
                }>
                  <Sidebar username={user.email} />
                </div>

                {/* Here's the main content */}
                <div className={
                  // depending on whether the menu is active or not, we need to adjust the width of the main content
                  ((activeMenu && !activeMenuOverlay)? 'dark:bg-main-dark-bg bg-main-bg min-h-screen ml-60 w-screenw_minus_60'
                  : 'dark:bg-main-dark-bg bg-main-bg min-h-screen w-full flex-2 ml-0')
                  +' transition-opacity duration-300'
                  // when the menu is overlayed, we need to blur and freeze all the elements behind the menu
                  + (activeMenuOverlay?' blur-sm pointer-events-none fixed':'')
                  + (zoomImage==null?'':' blur-sm pointer-events-none')
                }>
                  <div>
                    <Routes>
                      <Route path="/" element={ <HomePage username={user.email}/> } />
                      <Route path="/project/:project_id" element={(<ProjectPage username={user.email}/>)} />
                      <Route path="/bookmark" element={(<BookmarkPage username={user.email}/>)} />
                      <Route path="/gallery" element={(<GalleryPage username={user.email}/>)} />
                    </Routes>
                  </div>
                </div>

                {/* Here's the zoomed image */}
                {zoomImage!=null &&
                <div className='absolute z-50 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2'>
                  {zoomImage}
                </div>}

              </div>
            </BrowserRouter>
          </div>)}
      </div>
  )
}

export default App