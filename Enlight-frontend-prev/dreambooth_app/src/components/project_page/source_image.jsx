import React, { Component, useState } from 'react'
import { SERVER_URL } from "../../config/config"
import cache from '../../utils/cache';
import loading_icon from '../../data/loading-icon.svg';
import delete_icon from '../../data/source-image-delete-icon.svg';
import { Box } from '@mui/system';

// An Image is a single uploaded image by the user
class SourceImage extends Component {
    constructor(props) {
        super(props);
    };

    state = {
        img: '',
        has_image: false,
    };

    componentDidMount() {
        const cacheKey = 'source image ' + this.props.image_name;
        const cachedImage = cache.get(cacheKey);
        if (cachedImage) {
            this.setState({img: cachedImage, has_image: true});
            return;
        } else {
            // Get the image from the server
            fetch(SERVER_URL + '/get-source-image-data-low-res?'+new URLSearchParams({
                image_name: this.props.image_name
            }), {method: 'GET'})
            .then(response => response.json())
            .then(data => {
                this.setState({img: data.image_data, has_image: true});
                cache.set(cacheKey, data.image_data);
            }
            );
        }
    }

    render() {
            const handleMouseEnter = () => {
                this.setState({ isHovered: true });
            };        
            const handleMouseLeave = () => {
                this.setState({ isHovered: false });
            };
            return (
                <div className='image-container relative' onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
                {/* use loading icon if the image is not loaded, otherwise use the image */}
                <img
                    src={this.state.has_image ? `data:image/jpeg;base64,${this.state.img}` : loading_icon}
                    style={{width: 180, height: 180, borderRadius: 16}}/>
                {this.state.isHovered && !this.props.current_project_training_started && (
                    <img src={delete_icon} className="absolute bottom-2 right-2 w-5 h-5 cursor-pointer" onClick={()=>{this.props.handle_delete(this.props.image_name)}} /> 
                )}
                </div>
            )}    
}

export default SourceImage;