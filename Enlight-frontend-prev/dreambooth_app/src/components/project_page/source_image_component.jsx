import React, { Component, useState } from 'react'
import Box from '@mui/material/Box';
import { SERVER_URL } from "../../config/config"
import LinearProgressWithLabel from './linear_progress.jsx';
import IconButton from '@mui/material/IconButton';
import Avatar from '@mui/material/Avatar';
import add_image_icon from '../../data/add-image-icon.svg';
import InputBase from '@mui/material/InputBase';
import send_icon from '../../data/send-icon.svg';
import send_icon_light from '../../data/send-icon-light.svg';
import SourceImageList from './source_image_list';
import cache from '../../utils/cache';
import CropComponent from './crop_component';

// A SourceImageComponent contains source images and original category input
class SourceImageComponent extends React.Component {
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
        current_project_training_started: false, // whether the project is being trained
        current_project_training_ended: false, // whether the project has finished training
        category_name: '', // category name
        training_progress: 0, // training progress
        current_project_image_counter: 0, // number of source images uploaded for the project
        source_image_data: [], // source images
        cropped_image: null, // cropped image
    };    

    // connect to socket to listen for training progress
    componentDidUpdate(prevProps, prevState, snapshot) {
        var set_state = this.setState.bind(this);
        var component_props = this.props;
        if (this.state.current_project_training_started != prevState.current_project_training_started) {
            // if training has started and not ended, connect to socket
            if (this.state.current_project_training_started && ! this.state.current_project_training_ended){
                const projectid = this.props.project_id;
                const username = this.props.username;
                const loop_and_listen = async () => {
                    var is_tracking = true;
                    // track for 24 hours, if not finished, stop tracking.
                    var time_started_tracking = Date.now();
                    while (is_tracking && (Date.now() - time_started_tracking < 1000 * 60 * 60 * 24)) {
                        console.log("Getting new progress result...");
                        await fetch(SERVER_URL + '/get-training-progress?' + new URLSearchParams({
                            username: username,
                            projectid: projectid,
                        }), {method: 'GET'})
                        .then(response => response.json())
                        .then(data => {
                            console.log(data.progress);
                            set_state({training_progress: Math.floor(data.progress * 0.99)});
                            if (data.progress == 101) {
                                console.log("Got 101 from socket: ");
                                set_state({current_project_training_ended: true});
                                component_props.set_current_project_training_ended(true);
                                is_tracking = false;
                            } 
                        });
                        await new Promise(r => setTimeout(r, 5000));
                    }
                };
                loop_and_listen();
            }
        }
        if (this.state.cropped_image!=null && prevState.cropped_image==null) {
            // upload cropped image
            fetch(
                SERVER_URL + '/upload-source-image?'  + new URLSearchParams({
                    username: this.props.username,
                    project_id: this.props.project_id,
                }),
                {
                    method: 'POST',
                    body: this.state.cropped_image,
                }
            )
            .then(response => response.json())
            .then(data => {
                // turn formData into base64 and store it in cache. Then update the source image list. 
                const imageData = this.state.cropped_image.get('file');
                const reader = new FileReader();
                reader.onload = () => {
                    const base64 = reader.result;
                    // store the image in cache using the image name as the key. Here we remove the 'data:image/png;base64,' part because it will be added back when we retrieve the image from cache
                    cache.set('source image ' + data.image_name, base64.replace(/^data:image\/(png|jpg|jpeg);base64,/, ""));
                    console.log('cached image here !');
                    console.log('source image ' + data.image_name);
                    this.setState({current_project_image_counter: this.state.current_project_image_counter + 1});
                    this.setState({source_image_data: [...this.state.source_image_data, data.image_name]});
                    console.log('uploaded image!');
                };
                reader.readAsDataURL(imageData);
            })
            .then(() => {
                console.log('resetting cropped image');
                this.setState({cropped_image: null});
            })
                          
        }
    }

    componentDidMount() {
        // get category name
        this.setState({category_name: this.props.category_name});
        // the number of source images uploaded for the project
        this.setState({current_project_image_counter: this.props.current_project_image_counter});
        // get source images
        this.setState({source_image_data: this.props.source_image_data});
        // training started
        this.setState({current_project_training_started: this.props.current_project_training_started});
        // training ended
        this.setState({current_project_training_ended: this.props.current_project_training_ended});
    }

    // handle image upload
	handleImageUpload = (e) => {
        const file = e.target.files[0];
        const formData = new FormData();
        formData.append('file', file);

        // create image URL from the file
        const reader = new FileReader();
        reader.onload = () => {
            const base64 = reader.result;
            // pop out the image cropping modal
            this.props.set_zoom_image(
                <CropComponent 
                    set_zoom_image={this.props.set_zoom_image}
                    set_cropped_image={c=>{this.setState({cropped_image: c})}}
                    // image_src={'https://cdn.enlight-ai.com/landpage-perfume.png'}
                    image_src={base64}
                    />);
            // clear the file input
            e.target.value = null;
        };
        reader.readAsDataURL(file);
    };


    // handle training
    handleTraining = async () => {
        this.setState({current_project_training_started: true});
        const response = await fetch(SERVER_URL + '/train?' + new URLSearchParams({
            username: this.props.username,
            category_name: this.state.category_name,
            project_id: this.props.project_id,
        }), { method: 'GET'});
        console.log("training ended")
    }
    
    handle_delete = (filename) => {
        // delete the image from the server
        fetch(SERVER_URL + '/delete-source-image?'+new URLSearchParams({
            username: this.props.username,
            project_id: this.props.project_id,
            image_name: filename
        }), {method: 'GET'})
        .then(() => {
            console.log('deleted image ' + filename);
            // delete the image from the image list
            let new_img_list = this.state.source_image_data.filter((item) => item !== filename);
            this.setState({source_image_data: new_img_list});
        }
        );
    }


    render() {    
        return (
            <div className="flex flex-wrap lg:flex-nowrap justify-center mb-4">
                <div className='w-full bg-no-repeat bg-main-bg dark:bg-main-dark-bg border-t-1 border-gray-300 dark:border-gray-900'>
                    {/* First line of text */}
                    <div className="justify-center flex flex-wrap dark:text-gray-200  mt-1 w-full pt-3">
                        <div className='w-800 flex flex-wrap justify-between items-center'>
                            {!this.state.current_project_training_started && <Box sx={{ml:4, pt:1, pr:2, pb:1, flex: 1}}> <p><span>Let's start by uploading a few images:</span></p></Box>}
                            {this.state.current_project_training_started && !this.state.current_project_training_ended && <Box sx={{ml:4, pt:1, pr:2, pb:1, flex: 1}}> <p><span>Our model is learning from the following images of “{this.state.category_name}”:</span></p></Box>}
                            {this.state.current_project_training_started && this.state.current_project_training_ended &&<Box sx={{ml:4, pt:1, pr:2, pb:1, flex: 1}}>  <p><span>Our model has learned from the following images of “{this.state.category_name}”: </span></p> </Box> }                        
                        </div>
                    </div>

                    {/* Image uploaded */}
                    <div className="flex flex-wrap justify-center dark:bg-main-dark-bg dark:text-gray-200 w-full">
                        <div className="content-center dark:text-gray-200 bg-transparent rounded-xl w-800 ml-6 mr-6 bg-no-repeat bg-cover bg-center">
                            <div className="flex flex-nowrap">
                                <div className="flex flex-wrap ml-3 mr-1 mb-2">
                                    {/* Show existing uploaded images */}
                                    <SourceImageList key={'source image list ' + this.props.project_id} project_id={this.props.project_id} username={this.props.username} num_images={this.state.current_project_image_counter} img_list={this.state.source_image_data} handle_delete={this.handle_delete} current_project_training_started={this.state.current_project_training_started}/>

                                    {/* Allow uploading new images if training hasn't started yet */}
                                    {!this.state.current_project_training_started && <div className="flex flex-wrap lg:flex-nowrap m-1 pt-4">
                                        <IconButton
                                                component="label"
                                                sx={{ opacity:0.5, backgroundColor: this.props.mode=='dark'?"#47494D":'#ffffff', width: 180, height: 180, 
                                                        '&:hover': {opacity: 1, backgroundColor: this.props.mode=='dark'?"#47494D":'#ffffff'}, borderRadius: 16,                                               
                                                    }}
                                                >
                                                <Avatar variant='square' src={add_image_icon} sx={{width:180, height:180}} />
                                                <input
                                                    type="file"
                                                    accept=".jpg,.jpeg,.png"
                                                    hidden
                                                    onChange={this.handleImageUpload}
                                                />
                                        </IconButton>
                                    </div>}

                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Input box for the category name */}
                    {!this.state.current_project_training_started && this.state.current_project_image_counter > 0 && <div className="justify-center flex flex-wrap lg:flex-nowrap w-full pt-5 pb-2">
                        <div className='w-800 flex flex-wrap justify-between items-center'>
                            <InputBase
                                    fullWidth
                                    sx={{pl:2, pr:2, pt: 1, pb: 1, mr:2, ml:1, flex: 4, borderRadius: '20px', backgroundColor: this.props.mode=='dark'?'#636468':'white', height:40, color: this.props.mode=='dark'?'white':'black', 
                                        border: this.props.mode=='dark'?"1px solid #888888":"1px solid #cccccc"}}
                                    placeholder="What's the product? (describe it with one word, e.g., shoe)"
                                    onChange={(e) => {
                                        this.setState({category_name: e.target.value});
                                        }}/>
                            <div className={"rounded-md mt-0 mr-2 p-1 w-10 h-10" + (this.state.category_name==''?" opacity-50":" cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-700")} 
                                onClick={(this.state.category_name==''?null:this.handleTraining)}>
                                <img src={this.props.mode=='dark'?send_icon:send_icon_light} />
                            </div>
                        </div>
                    </div>}

                    {/* Show training progress during training */}
                    {this.state.current_project_training_started && !this.state.current_project_training_ended && 
                        <div className="justify-center flex flex-wrap dark:text-gray-200  mt-1 w-full pt-3">
                            <div className='content-center dark:text-gray-200 bg-transparent rounded-xl w-800 mt-4 ml-2 pl-6 mr-2 pr-6 mb-6 bg-no-repeat bg-cover bg-center'>
                                    <LinearProgressWithLabel value={this.state.training_progress} color={this.props.mode=='dark'?'white':'black'}/>
                            </div>
                        </div>
                    }

                </div>
            </div>
        );
    }
}

export default SourceImageComponent;