import React, { Component, useState } from 'react'
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import { useStateContext } from '../../contexts/ContextProvider';
import { useEffect } from 'react';
import InputBase from '@mui/material/InputBase';
import send_icon from '../../data/send-icon.svg';
import send_icon_light from '../../data/send-icon-light.svg';
import suggest_icon from '../../data/suggest-icon.svg';
import suggest_icon_light from '../../data/suggest-icon-light.svg';
import { SERVER_URL } from "../../config/config"
import { AiOutlineMenu } from 'react-icons/ai';
import GenerationComponent from './generation_component';
import NavButton from './nav_button';
import { useParams } from "react-router-dom";
import SourceImageComponent from './source_image_component';
import "./ButtonWithHoverText.css";

// number of images to generate for each prompt
const num_images_to_generate = 20;


const ProjectPage = (props) => {
    // To store the number of source images uploaded for a project
    const [currentProjectImageCounter, setCurrentProjectImageCounter] = useState(0);

    // to store whether the project is being trained or have been trained
    const [currentProjectTrainingStarted, setCurrentProjectTrainingStarted] = useState(false);

    // to store whether the project has finished training
    const [currentProjectTrainingEnded, setCurrentProjectTrainingEnded] = useState(false);

    // to store the current prompt text
    const [ currentPromptText, setCurrentPromptText ] = useState('');

    // The number of generation components that has ever been created, including the deleted ones
    const [generationComponentNumber, setGenerationComponentNumber] = useState(0);

    // The list of prompt ids
    const [promptIdList, setPromptIdList] = useState([]);

    // The category name of the project
    const [currentProjectCategoryName, setCurrentProjectCategoryName] = useState('');

    // source image list
    const [sourceImageData, setSourceImageData] = useState([]);

    // import the global state
    const { activeMenu, setActiveMenu, activeMenuOverlay, setActiveMenuOverlay, setZoomImage, mode, setCurrentProjectId } = useStateContext();

    // the project_id should come from the url
    let { project_id } = useParams();

    // whether the current page is being loaded
    const [pageLoading, setPageLoading] = useState(false);

    // tooltip text for the suggest button
    const [showSuggestionText, setShowSuggestionText] = useState(false);

    // initialize project
    useEffect(() => {
        async function initProject() {
            setPageLoading(true);
            setCurrentProjectId(Number(project_id));
            var res = await fetch(SERVER_URL + '/get-project-init-state?' + new URLSearchParams({
                username: props.username,
                project_id: project_id,   
            }));
            var res_json = await res.json();
            setCurrentProjectTrainingEnded(res_json.training_ended);
            setCurrentProjectTrainingStarted(res_json.training_started);
            setCurrentProjectCategoryName(res_json.category_name);                
            setGenerationComponentNumber(res_json.prompt_counter);
            setPromptIdList(res_json.prompt_ids);
            // get the source image list
            var res = await fetch(SERVER_URL + '/get-source-image?'+new URLSearchParams({
                username: props.username,
                project_id: project_id}));
            var res_json = await res.json();
            var file_names = res_json.file_names;
            setSourceImageData(file_names);
            setCurrentProjectImageCounter(file_names.length);
            setPageLoading(false);
        };
        initProject();
    }, [project_id]);

    // handle new prompt
    const handleNewGenerating = async () => {
        // send the prompt to the backend
        await fetch(SERVER_URL + '/add-new-prompt?' + new URLSearchParams({
            username: props.username,
            project_id: project_id,
            prompt: currentPromptText,
        }), {method: 'GET'});  
        // increment the number of generation components
        setPromptIdList((prevPromptIdList) => [...prevPromptIdList, generationComponentNumber]);
        setGenerationComponentNumber(generationComponentNumber+1)
        // clear the prompt text in the input box
        setCurrentPromptText('')
    };

    // handle the prompt suggestion
    const handlePromptSuggestion = async () => {
        // send the prompt to the backend
        var res = await fetch(SERVER_URL + '/suggest-prompt?' + new URLSearchParams({
            username: props.username,
            project_id: project_id,
        }), {method: 'GET'});
        var res_json = await res.json();
        // set the prompt text
        setCurrentPromptText(res_json.prompt);
    };

    // handle the prompt deletion
    const handlePromptDeletion = async (prompt_id) => {
        // send the prompt to the backend
        await fetch(SERVER_URL + '/delete-prompt?' + new URLSearchParams({
            username: props.username,
            project_id: project_id,
            prompt_id: prompt_id,
        }), {method: 'GET'});
        // remove the prompt id from the list
        setPromptIdList((prevPromptIdList) => prevPromptIdList.filter((item) => item != prompt_id));
    };

    return (
    // pageLoading ? null :
    <div className={'h-screen bg-main-bg dark:bg-main-dark-bg fixed '+((activeMenu && !activeMenuOverlay)?'w-screenw_minus_240':'w-full')}>

        {/* Show the menu button if the menu is not active */}
        {(!activeMenu || activeMenuOverlay) && <div className="flex justify-between items-center h-50 w-full bg-generation-component-light-bg dark:bg-generation-component-dark-bg">
            <NavButton key="nav_button" title="Menu" color={mode=='dark'?'white':'black'}  customFunc={() => {setActiveMenuOverlay(true); setActiveMenu((prevActiveMenu) => !prevActiveMenu )}} icon={<AiOutlineMenu />} />
        </div>}

        {/* The main body of the page */}
        <div className={'mt-0 bg-main-bg dark:bg-main-dark-bg overflow-y-auto overflow-x-hidden '+((activeMenu && !activeMenuOverlay)?'h-screen_minus_80':'h-screen_minus_130')}>   
            {/* Show the image uploading and training component */}
            {!pageLoading && <SourceImageComponent 
                key={'project '+project_id+' source image component'}
                project_id={project_id}
                username={props.username}
                category_name={currentProjectCategoryName}
                current_project_image_counter={currentProjectImageCounter}
                source_image_data={sourceImageData}
                current_project_training_started={currentProjectTrainingStarted}
                current_project_training_ended={currentProjectTrainingEnded}
                mode={mode}
                set_zoom_image={setZoomImage}
                set_current_project_training_ended={setCurrentProjectTrainingEnded}/>}

            {/* Show the generation components */}
            {currentProjectTrainingEnded && promptIdList.map((i) => {
                return (<div key={'project '+project_id+' prompt '+i+' div'} className={"flex flex-wrap lg:flex-nowrap justify-center "}>
                        <GenerationComponent key={'project '+project_id+' prompt '+i} num_images_to_generate={num_images_to_generate} prompt_id={i} project_id={project_id} username={props.username} set_zoom_image={setZoomImage} mode={mode} delete_prompt={handlePromptDeletion}/>
            </div>)})}
        </div>

        {/* Show the input box for new prompts */}
        {currentProjectTrainingEnded && <div className='bg-generation-component-light-bg dark:bg-generation-component-dark-bg w-full h-80'>            
            <div className="justify-center flex flex-wrap lg:flex-nowrap bg-generation-component-light-bg dark:text-gray-200 dark:bg-generation-component-dark-bg w-full pt-5 pb-2">
                <div className='w-800 flex flex-wrap justify-between items-center'>
                    <div className={"container rounded-md mt-0 mr-2 p-2 w-10 h-10 cursor-pointer hover:bg-gray-300 hover:dark:bg-gray-700"} 
                         onClick={handlePromptSuggestion} onMouseEnter={() => setShowSuggestionText(true)} onMouseLeave={() => setShowSuggestionText(false)}>
                        <img src={mode=='dark'?suggest_icon:suggest_icon_light} />
                        {showSuggestionText && (
                            <div className={mode=='dark'?"tooltip":"tooltip-light"}>Suggest an image idea</div>
                        )}
                    </div>
                    <InputBase 
                            fullWidth
                            sx={{pl:2, pr:2, pt: 1, pb: 1, mr:2, ml:1, flex: 4, borderRadius: '20px', backgroundColor: mode=='dark'?'#636468':'white', height:40, color: mode=='dark'?'white':'black' }}
                            placeholder="What do you want to generate?"
                            value={currentPromptText}
                            onChange={(event)=>{setCurrentPromptText(event.target.value)}}/>
                    <div className={"rounded-md mt-0 mr-2 p-1 w-10 h-10"+(currentPromptText==''?" opacity-50":" cursor-pointer hover:bg-gray-300 hover:dark:bg-gray-700")} 
                         onClick={(currentPromptText=='')?null:handleNewGenerating}>
                        <img src={mode=='dark'?send_icon:send_icon_light} />
                    </div>
                </div>
            </div>            
        </div>}
    </div>
      )
}

export default ProjectPage;