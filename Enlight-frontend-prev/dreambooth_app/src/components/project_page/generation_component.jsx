import React, { Component, useState } from 'react'
import Box from '@mui/material/Box';
import repeat_icon from '../../data/repeat-icon.svg';
import repeat_icon_light from '../../data/repeat-icon-light.svg';
import delete_prompt_icon from '../../data/delete-prompt-icon.svg';
import delete_prompt_icon_light from '../../data/delete-prompt-icon-light.svg';
import { SERVER_URL } from "../../config/config"
import GeneratedImage from './generated_image';
import { ImageList } from '@mui/material';
import { ImageListItem } from '@mui/material';
import LinearProgressWithLabel from './linear_progress.jsx';

// A GenerationComponent contains one prompt and its generated images
class GenerationComponent extends React.Component {
    state = {
        promptText: '', // prompt text
        isButtonDisabled: false, // whether the repeat button is disabled (this button is disabled when the prompt is being generated)
        beforeGeneration: true, // whether the prompt hasn't been generated yet
        prompt_id: this.props.prompt_id, // prompt id
        generationProgress: 0, // generation progress
        columns: 4, // number of columns in the generated images grid
        generatedImagesData: [], // generated images
        generatedImagesDataLength: 0, // number of generated images
        isLoading: true, // whether the generated component is loading
        isReseting: false, // whether we are resetting the generated progress
    };    

    componentWillUnmount() {
    window.removeEventListener('resize', this.updateColumns);
    }

    updateColumns = () => {
    const width = window.innerWidth;
    let columns = 4;
    if (width >= 815) {
        columns = 4;
    } else if (width >= 635) {
        columns = 3;
    } else if (width >= 455) {
        columns = 2;
    } else {
        columns = 1;
    }
    this.setState({ columns });
    };

    // handle the repeat button click
    handleGenerating = async () => {
        this.setState({ isReseting: true });
        this.setState({ generationProgress: 0 });

        var response = await fetch(SERVER_URL + '/reset-generating-progress?'+new URLSearchParams({
            username: this.props.username,
            projectid: this.props.project_id,
            promptid: this.props.prompt_id,
        }), {method: 'GET'})
        response = await response.json();
        // wait for 1 second to make sure the server has received the reset request
        await new Promise(r => setTimeout(r, 1000));

        this.setState({ isButtonDisabled: true });
        this.setState({ isReseting: false });

        await fetch(SERVER_URL + '/generate?'+new URLSearchParams({
                username: this.props.username,
                project_id: this.props.project_id,
                prompt_id: this.props.prompt_id,
                num_images_to_generate: this.props.num_images_to_generate,
            }), {method: 'GET'})
    }

    componentDidUpdate(prevProps, prevState, snapshot)   {
        // when the generation button is clicked, we need to connect to listen for the generation progress
        if (this.state.isButtonDisabled && !prevState.isButtonDisabled) {
            const projectid = this.props.project_id;
            const promptid = this.props.prompt_id;
            const username = this.props.username;
            const setStateFunc = this.setState.bind(this);
            const loop_and_listen = async () => {
                var is_tracking = true;
                // track for 24 hours, if not finished, stop tracking.
                var time_started_tracking = Date.now();
                while (is_tracking && Date.now() - time_started_tracking < 1000 * 60 * 60 * 24) {
                    await fetch(SERVER_URL + '/get-generating-progress?' + new URLSearchParams({
                        username: username,
                        projectid: projectid,
                        promptid: promptid,
                    }), {method: 'GET'})
                    .then(response => response.json())
                    .then(data => {
                        if (data.progress == 101) {
                            setStateFunc({ isButtonDisabled: false });
                            setStateFunc({ beforeGeneration: false });
                            is_tracking = false;
                        } else {
                            setStateFunc({ generationProgress: Math.floor(data.progress * 0.99)});
                        }
                    });
                    await new Promise(r => setTimeout(r, 5000));
                }
            }
            loop_and_listen();        
        }
        // when the generation button turn from disabled to enabled, which happens when a generating is finished, we need to refresh the generated images data
        if (!this.state.isButtonDisabled && prevState.isButtonDisabled) {
            fetch(SERVER_URL + '/get-generated-image?'+new URLSearchParams({
                        username: this.props.username,
                        project_id: this.props.project_id,
                        prompt_id: this.props.prompt_id,
                    }), {method: 'GET'})
                    .then(response => {
                        var ret = response.json();
                        return ret;
                    })
                    .then(data => {
                        this.setState({ generatedImagesData: data.generated_images_data });
                        this.setState({ generatedImagesDataLength: data.generated_images_data.length });
                    });
        }
    }

    // before rendering the component, fetch the prompt text and the number of existing generated images from the server
    componentDidMount() {
        // update the number of columns in the generated images grid
        this.updateColumns();
        window.addEventListener('resize', this.updateColumns);    

        fetch(SERVER_URL + '/get-prompt-init-state?'+new URLSearchParams({
            username: this.props.username,
            project_id: this.props.project_id,
            prompt_id: this.props.prompt_id,
        }), {method: 'GET'})
        .then(response => {
            // log the memory size of the response
            return response.json()})
        .then(
            data => {
            this.setState({ promptText: data.prompt_text });
            this.setState({ isButtonDisabled: data.is_button_disabled });
            this.setState({ beforeGeneration: data.before_generation });
            // if the prompt is newly created, call handleGenerating() to kickstart the first generation
            if (data.before_generation){
                this.handleGenerating();
                // finish loading
                this.setState({ isLoading: false });
            }
            else {
                fetch(SERVER_URL + '/get-generated-image?'+new URLSearchParams({
                    username: this.props.username,
                    project_id: this.props.project_id,
                    prompt_id: this.props.prompt_id,
                }), {method: 'GET'})
                .then(response => {
                    var ret = response.json();
                    return ret;
                })
                .then(data => {
                    this.setState({ generatedImagesData: data.generated_images_data });
                    this.setState({ generatedImagesDataLength: data.generated_images_data.length });
                    // finish loading
                    this.setState({ isLoading: false });
                });
            }
        })   
    }

    render() {
        return (
            // only render the component when the data is loaded
            !this.state.isLoading &&
            <div className='w-full bg-no-repeat bg-main-bg dark:bg-main-dark-bg border-t-1 border-gray-300 dark:border-gray-900'>
                <div className="justify-center flex flex-wrap dark:text-gray-200 mt-1 w-full pt-3 pb-3">
                    <div className='w-800 flex flex-wrap justify-between items-center'>
                        {/* Text Prompt */}
                        <Box sx={{ml:4, pt:1, pr:2, pb:1, flex: 1}}>
                            <p><span> {this.state.promptText} </span> </p>
                        </Box>
                        {/* If no generation process is ongoing, show the repeat and delete button. Otherwise, show a loading icon. */}
                        {!this.state.isButtonDisabled && !this.state.isReseting && <div className="flex justify-center p-2 h-9 w-40 items-center"> 
                            {/* The repeat button */}
                            <div className="hover:bg-gray-200 dark:hover:bg-gray-700 rounded-md cursor-pointer p-2 w-9 h-9" onClick={this.handleGenerating}>
                                <img src={this.props.mode=='dark'?repeat_icon:repeat_icon_light} />
                            </div>
                            {/* The delete button */}
                            <div className="hover:bg-gray-200 dark:hover:bg-gray-700 rounded-md cursor-pointer p-2 w-9 h-9" onClick={()=>{this.props.delete_prompt(this.props.prompt_id)}}>
                                <img src={this.props.mode=='dark'?delete_prompt_icon:delete_prompt_icon_light} />
                            </div>
                        </div>}
                        {(this.state.isButtonDisabled || this.state.isReseting) &&  <div className="p-2 h-9 w-40">
                            <LinearProgressWithLabel value={this.state.generationProgress} color={this.props.mode=='dark'?'white':'black'} size="30px" />
                        </div>}
                    </div>
                </div>

                {/* Show generated Images if there exists any */}
                <div className="flex flex-wrap justify-center dark:bg-main-dark-bg dark:text-gray-200 w-full pt-2">
                    <div className="content-center dark:text-gray-200 bg-transparent rounded-xl w-800 ml-6 mr-6 bg-no-repeat bg-cover bg-center">
                        {this.state.generatedImagesDataLength>0 && <div className="flex flex-nowrap  ">
                            <div className="flex w-200 ml-3 mr-1 mb-2">
                                <ImageList
                                    cols={this.state.columns}
                                    rowHeight={200}
                                    margin={1}>
                                    {this.state.generatedImagesData.slice(0, this.props.num_images_to_generate).reverse().map((item) => {
                                        return (
                                        <ImageListItem key={'generated image ' + item.file_name} sx={{m:0.22}}>
                                            <GeneratedImage file_name={item.file_name} is_bookmarked={item.is_bookmarked} prompt_id={this.props.prompt_id} project_id={this.props.project_id} username={this.props.username} set_zoom_image={this.props.set_zoom_image}/> 
                                        </ImageListItem>)})}
                                </ImageList>
                            </div>
                        </div>}
                    
                    </div>
                </div>

            </div>);
    }
}

export default GenerationComponent;