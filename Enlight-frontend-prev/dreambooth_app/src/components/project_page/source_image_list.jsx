import React, { Component, useState } from 'react'
import { SERVER_URL } from "../../config/config"
import SourceImage from './source_image';


// An Image list is a list containing all source images
class SourceImageList extends Component {
    constructor(props) {
        super(props);
    };

    render() {
        // const {img_list, has_image} = this.state;
        const img_list = this.props.img_list;
        // check if the image list lenght is 0
        if(img_list.length === 0) 
            return null
        else
            {return (
                img_list.map((item) => {
                    return (
                        <div key={'source image ' + item + ' div'} className="flex flex-wrap lg:flex-nowrap w-200 h-200 m-1 pt-4 items-center">
                            <div>
                                <SourceImage key={'source image ' + item} image_name={item} handle_delete={this.props.handle_delete} current_project_training_started={this.props.current_project_training_started}/>
                            </div>
                        </div>
                    )
                })
            )}
    }
}

export default SourceImageList;