import React, { useEffect, useRef } from 'react'
import { Link, NavLink, useNavigate} from 'react-router-dom'
import { MdOutlineCancel } from 'react-icons/md'
import { TooltipComponent } from '@syncfusion/ej2-react-popups'
import { links } from '../data/dummy'
import avatar from '../data/avatar.jpg';
import project_icon from '../data/project-icon.svg';
import bookmark_icon from '../data/bookmark-icon.svg';
import gallery_icon from '../data/gallery-icon.svg';

import more_button from '../data/more-button.svg';
import project_add_icon from '../data/project-add-icon.svg';
import Box from '@mui/material/Box';
import logout_icon from '../data/log-out-icon.svg';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import InputBase from '@mui/material/InputBase';
import ClickAwayListener  from '@mui/material/ClickAwayListener';
import { SERVER_URL } from '../config/config';
import close_icon from '../data/close-icon.svg';
import lightmode_icon from '../data/lightmode-icon.svg';
import darkmode_icon from '../data/darkmode-icon.svg';
import { useParams } from "react-router-dom";
import { Tooltip } from '@mui/material'
import {useAuth0} from "@auth0/auth0-react";

import "../App.css"
import "./sidebar.css"

import { useStateContext } from '../contexts/ContextProvider';


const Sidebar = (props) => {

  const { activeMenu, setActiveMenu, activeMenuOverlay, setActiveMenuOverlay, screenSize, mode, setMode, projectList, setProjectList, activeTab, setActiveTab, currentProjectId } = useStateContext();

  // the anchor for the popup menu
  const [anchorEl, setAnchorEl] = React.useState(null);

  // whether the user is renaming the active project
  const [isRenaming, setIsRenaming] = React.useState(false);

  // the new name of the project
  const [newProjectName, setNewProjectName] = React.useState('');

  // navigate allows us to redirect to a different page programmatically
  const navigate = useNavigate();

  // the input field reference for renaming the project
  const inputRef = useRef(null);

  // handle logout
  const { user, logout} = useAuth0();

  // we use this to focus on the input field when the user clicks rename
  useEffect(()=> {
    if (isRenaming) {
      inputRef.current?.focus();
    }
  }, [isRenaming]);

  // initialize the project name list
  useEffect(() => {
    const fetchData = async () => {
        const response = await fetch(SERVER_URL + '/get-project-list?' + new URLSearchParams({
          username: props.username,
        }, {method: 'GET'}));
        const data = await response.json();
        // replace the project id with its number value
        var new_project_list = data.project_list.map((item) => {
          return {
            project_id: Number(item.project_id),
            project_name: item.project_name,
          }
        });
        setProjectList(new_project_list);
      }
    fetchData();
  }, []);

  // Delete the project. This will both reset the project and delete the project from the project list
  const handleDelete = async () => {
    const response = await fetch(SERVER_URL + '/delete-project?' + new URLSearchParams({
        username: props.username,
        project_id: currentProjectId,
        }), {method: 'GET'});
    // remove the project from the project list
    var new_project_list = projectList.filter((item) => {
      return item.project_id !== currentProjectId;
    });
    // if the project list is empty, we create a new project
    if (new_project_list.length === 0) {
      const response = await fetch(SERVER_URL + '/create-new-project?' + new URLSearchParams({
          username: props.username,
        }), {method: 'GET'});
      const data = await response.json();
      // new project item is added to the project list
      var new_project_item = {
        project_id: Number(data.new_project_id),
        project_name: data.new_project_name,
      }
      // append the new project item to the project list
      new_project_list = new_project_list.concat([new_project_item]);
      // set the new project list
      setProjectList(new_project_list);
      // redirect to the new project page using react router
      navigate('/project/'+data.new_project_id);
    } else {
      // set the new project list
      setProjectList(new_project_list);
      // redirect to the home page
      navigate('/');
    }    
    // close the popup menu
    setAnchorEl(null);
  }

  // Reset the project, i.e. delete all the data in the database
  const handleNewProject = async () => {
    const response = await fetch(SERVER_URL + '/create-new-project?' + new URLSearchParams({
        username: props.username,
      }), {method: 'GET'});
    const data = await response.json();
    // new project item is added to the project list
    var new_project_item = {
      project_id: Number(data.new_project_id),
      project_name: data.new_project_name,
    }
    // append the new project item to the project list
    var new_project_list = projectList.concat([new_project_item]);
    setProjectList(new_project_list);
    setNewProjectName('');
    setIsRenaming(true);
    setAnchorEl(null);
    // redirect to the new project page using react router
    navigate('/project/'+data.new_project_id);
  }

  // handle the click event when the user clicks rename
  const handleRenaming = async () => {
      // setNewProjectName('');
      setIsRenaming(true);
      setAnchorEl(null);
      this.textInput.focus();
  }

  // Update the project name
  const updateProjectName = async () => {
    if (newProjectName === '') {
      setIsRenaming(false);
      return;
    }
    const response = await fetch(SERVER_URL + '/update-project-name?' + new URLSearchParams({
        username: props.username,
        project_id: currentProjectId,
        new_project_name: newProjectName,
    }), {method: 'GET'});
    var new_project_list = projectList.map((item) => {
      if (item.project_id === currentProjectId) {
        return {
          project_id: item.project_id,
          project_name: newProjectName,
        }
      } else {
        return item;
      }
    });
    setProjectList(new_project_list);
    setIsRenaming(false);
  }

  // MoreMenu is the popup menu that appears when you click the three dots on the right of the current project
  function MoreMenu() {
    const open = Boolean(anchorEl);
    const handleClick = (event) => {
      setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
      setAnchorEl(null);
    };
    return (
      <div className='flex flex-wrap'>
        <div className="flex rounded-md cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700" onClick={handleClick}>
                  <img src={more_button} />
        </div>
          <Menu
            sx={{ '& .MuiMenu-paper': { bgcolor: mode=='dark'?'#424242':'#e8e8e8' }, '& .MuiMenuItem-root': { color: mode=='dark'?'white':'black', "&:hover": { bgcolor: mode=='dark'?'#303030':'#ffffff' }}}}
            id="basic-menu"
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleClose}
          >
            {/* <MenuItem onClick={handleReset}>Reset</MenuItem> */}
            <MenuItem onClick={handleRenaming}>Rename</MenuItem>
            <MenuItem onClick={handleDelete}>Delete</MenuItem>
            {/* <MenuItem onClick={handleNewProject}>Add Project</MenuItem> */}
          </Menu>
      </div>
    );
  }

  // handle set mode
  const handleSetMode = (mode_str) => {
    setMode(mode_str);
    fetch(SERVER_URL + '/set-mode?' + new URLSearchParams({
      username: props.username,
      mode: mode_str,
    }), {method: 'GET'});
  }

  return (
    <div className={"h-screen overflow-hidden hover:overflow-auto pb-10 bg-secondary-light-bg dark:bg-secondary-dark-bg border-r-2 border-gray-200 dark:border-gray-800"}>
      {activeMenuOverlay && <div className="absolute top-5 -right-10 w-10 h-10 bg-white hover:bg-gray-100 dark:bg-gray-900 dark:hover:bg-gray-500 opacity-80 dark:opacity-50">
          <img src={close_icon} className="cursor-pointer" onClick={() => {setActiveMenu(false); setActiveMenuOverlay(false);}} />
        </div>}


      {/* Project list */}
      <div className='flex justify-between items-center ml-4 mt-10 mr-4 mb-3'>
        <div className="flex space-x-4">
          <img src={project_icon} />
          <p> <span className="font-light text-black dark:text-slate-50 text-16 ">Projects</span></p>
        </div>

        <img src={project_add_icon} className="w-6 h-6 hover:bg-gray-100 dark:hover:bg-gray-500 mt-1 cursor-pointer rounded-md" onClick={handleNewProject} />            
      </div>

      <div className="bg-third-light-bg dark:bg-third-dark-bg mt-2 pt-2 pb-2">
      <div className="content">
        {projectList.map((item) => (
          <div key={'sidebar project '+ item.project_id}>
              {(item.project_id === currentProjectId) && (activeTab == 'project') && !isRenaming && <div className="flex justify-between items-center rounded-lg bg-slate-100 dark:bg-gray-700 pl-4 pr-1 ml-2 mt-2 pt-2 mr-2 pb-2">
                  <span className="text-black dark:text-gray-50 text-16">
                  <Box component="div" sx={{whiteSpace: 'nowrap', fontSize: '16px', width:'160px', height:'24px', textOverflow: 'ellipsis', overflow: 'hidden'}}>{item.project_name} </Box>
                  </span>{' '}                  
                  {MoreMenu()}
                </div>}
              {(item.project_id === currentProjectId) && (activeTab == 'project') && isRenaming && <div className="flex justify-between items-center rounded-lg pl-4 pr-1 ml-2 mt-2 pt-2 mr-2 pb-2 bg-slate-100 dark:bg-gray-700">
                <ClickAwayListener onClickAway={()=>{updateProjectName();}}>
                  <span className="text-black dark:text-gray-50 text-16 "><InputBase
                        fullWidth
                        margin='dense'
                        autoFocus
                        inputRef={inputRef}
                        sx={{color:mode=='dark'?'white':'black', fontSize: '16px', width:'180px', height:'24px'}}
                        placeholder={item.project_name}
                        value={newProjectName}
                        onKeyPress={(event)=>{if(event.key === 'Enter'){updateProjectName()}}}
                        onChange={(event)=>{setNewProjectName(event.target.value)}}
                        /></span>  
                </ClickAwayListener>
              </div>}
              <Link to={'/project/'+item.project_id}>
                {((item.project_id !== currentProjectId) || (activeTab !== 'project')) && <div className="rounded-lg flex justify-between items-center  pl-4 pr-1 ml-2 mt-2 pt-2 mr-2 pb-2 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700" onClick={()=>{setActiveTab('project'); setIsRenaming(false); navigate('/project/'+item.project_id); setNewProjectName(item.project_name);}}>
                    <span className="text-font-red dark:text-gray-400 text-16 ">
                    <Box component="div" sx={{whiteSpace: 'nowrap', fontSize: '16px', width:'160px', height:'24px', textOverflow: 'ellipsis', overflow: 'hidden'}}>{item.project_name} </Box>
                    </span>{' '}
                  </div>} 
              </Link>
          </div>
        ))}
      </div>
      </div>



      {/* Mode setting */}
      {mode=='dark'?<div className="rounded-lg flex w-50 space-x-4 items-center pl-2 ml-2 mt-4 pt-2 mr-2 pb-2 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700" onClick={() =>{handleSetMode('')}}>
        <img src={lightmode_icon} />
        <p> <span className="font-light text-black dark:text-slate-50 text-16 ">Light mode</span></p>
      </div>:<div className="rounded-lg flex w-50 space-x-4 items-center pl-2 ml-2 mt-4 pt-2 mr-2 pb-2 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700" onClick={() =>{handleSetMode('dark')}}>
        <img src={darkmode_icon} />
        <p> <span className="font-light text-black dark:text-slate-50 text-16 ">Dark mode</span></p>
      </div>}


      {/* The Bookmark section */}
      <Link to='/bookmark'>
        <div className={"rounded-lg flex w-50 space-x-4 items-center pl-2 ml-2 mt-4 pt-2 mr-2 pb-2 cursor-pointer"+(activeTab=='bookmark'?' bg-slate-100 dark:bg-gray-700':' hover:bg-gray-100 dark:hover:bg-gray-700')}
              // we need to set the active tab to bookmark when we click on the bookmark section, so as to make the background color of the bookmark section change
              // we also need to set the project id to null, so as to make the project tab not active (i.e., not having lighter background color)
              onClick={()=>{setActiveTab('bookmark')}}>
            <img src={bookmark_icon} />
              <p> <span className="font-light text-black dark:text-slate-50 text-16 ">Bookmark</span></p>
        </div>
      </Link>


      {/* The Gallery section */}
       <Link to='/gallery'>
          <div className="rounded-lg flex w-50 space-x-4 items-center pl-2 ml-2 mt-4 pt-2 mr-2 pb-2 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700">
              <img src={gallery_icon} />
              <p> <span className="font-light text-black dark:text-slate-50 text-16 ">Gallery</span></p>
          </div>
       </Link>


      {/* Logout button */}
      <div className="rounded-lg flex w-50 space-x-4 items-center pl-2 ml-2 mt-4 pt-2 mr-2 pb-2 cursor-pointer dark:hover:bg-gray-700 hover:bg-gray-100" onClick={() => logout({returnTo: window.location.origin})}>
        <img src={logout_icon}/>
          <p> <span className="font-light text-black dark:text-slate-50 text-16 ">Log out</span></p>
      </div>

    </div>
  );
};

export default Sidebar