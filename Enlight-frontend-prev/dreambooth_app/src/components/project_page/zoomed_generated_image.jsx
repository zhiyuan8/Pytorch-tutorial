import React, { Component, useState } from 'react'
import image_download_icon from '../../data/image-download.svg';
import { SERVER_URL } from "../../config/config"
import close_icon from '../../data/close-icon.svg';
import loading_icon from '../../data/loading-icon.svg';
import cache from '../../utils/cache';
import bookmark_selected_icon from '../../data/bookmark-selected-icon.svg';
import bookmark_not_selected_icon from '../../data/bookmark-not-selected-icon.svg';

// A ZoomedGeneratedImage is a single generated image that is zoomed in
class ZoomedGeneratedImage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isHovered: false,
            has_image: false,
            img: '',
        };
    };

    componentDidMount() {
        this.setState({ is_bookmarked: this.props.is_bookmarked});
        var component_props = this.props;
        const cacheKey = 'full resolution generated image ' + this.props.image_name;
        const cachedImage = cache.get(cacheKey);
        if (cachedImage) {
            this.setState({img: cachedImage, has_image: true});
            return;
        } else {
            // Get the image from the server
            fetch(SERVER_URL + '/get-generated-image-data?'+new URLSearchParams({
                image_name: component_props.image_name
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
        const handleDownload = () => {
            // download the image
            var a = document.createElement("a");
            a.href = "data:image/png;base64," + this.state.img; 
            a.download = "image.png"; 
            a.click(); 
          };
        const handleMouseEnter = () => {
            this.setState({ isHovered: true });
        };
    
        const handleMouseLeave = () => {
            this.setState({ isHovered: false });
        };
        return (
            <div className='image-container' onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
                <img
                    src={this.state.has_image? `data:image/jpeg;base64,${this.state.img}`: loading_icon}
                    style={{width: '100%', borderRadius: 16}}
                    alt='Helpful alt text'
                    />

                {this.state.isHovered && this.state.has_image && (
                    <img src={image_download_icon} className="absolute bottom-3 right-3 w-5 h-5 cursor-pointer" onClick={handleDownload} /> 
                    )}
                {this.state.isHovered && this.state.is_bookmarked && this.state.has_image && (
                    <img src={bookmark_selected_icon} className="absolute bottom-3 right-10 w-5 h-5 cursor-pointer" 
                        onClick={()=>{
                            this.props.handle_remove_bookmark();
                            this.setState({is_bookmarked: false})
                        }} /> 
                    )}
                {this.state.isHovered && !this.state.is_bookmarked && this.state.has_image && (
                    <img src={bookmark_not_selected_icon} className="absolute bottom-3 right-10 w-5 h-5 cursor-pointer" 
                        onClick={()=>{
                            this.props.handle_add_bookmark();
                            this.setState({is_bookmarked: true})
                        }} /> 
                    )}
                <div className="absolute top-3 -right-10 w-10 h-10 bg-white hover:bg-gray-100 dark:bg-gray-900 dark:hover:bg-gray-500 opacity-80 dark:opacity-50">
                    <img src={close_icon} className="cursor-pointer" onClick={() => {this.props.set_zoom_image(null);}} />
                </div>
            </div>
        )
    }
}

export default ZoomedGeneratedImage;