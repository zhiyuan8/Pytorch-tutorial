import React, { Component, useState } from 'react'
import image_download_icon from '../../data/image-download.svg';
import { SERVER_URL } from "../../config/config"
import bookmark_selected_icon from '../../data/bookmark-selected-icon.svg';
import bookmark_not_selected_icon from '../../data/bookmark-not-selected-icon.svg';
import ZoomedGeneratedImage from './zoomed_generated_image';
import cache from '../../utils/cache';
import loading_icon from '../../data/loading-icon.svg';

// A GeneratedImage is a single generated image by the model
class GeneratedImage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            img: '', // low resolution image
            img_full: '', // full resolution image
            has_image: false,
            isHovered: false,
            is_bookmarked: this.props.is_bookmarked,
        };
    };

    componentDidMount() {
        const cacheKey = 'generated image ' + this.props.file_name;
        const cachedImage = cache.get(cacheKey);
        if (cachedImage) {
            this.setState({img: cachedImage, has_image: true});
            return;
        } else {
            // Get the image from the server
            fetch(SERVER_URL + '/get-generated-image-data-low-res?'+new URLSearchParams({
                image_name: this.props.file_name
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
        const handleDownload = async () => {
            var component_props = this.props;
            var component = this;
            const cacheKey = 'full resolution generated image ' + this.props.file_name;
            const cachedImage = cache.get(cacheKey);
            if (cachedImage) {
                component.setState({img_full: cachedImage});
                console.log('using cached image');
            } else {
                // Get the image from the server
                var response = await fetch(SERVER_URL + '/get-generated-image-data?'+new URLSearchParams({
                    image_name: component.props.file_name
                }), {method: 'GET'})
                response = await response.json();
                component.setState({img_full: response.image_data});
                cache.set(cacheKey, response.image_data);
                console.log('downloaded full resolution generated image');
            }    
            // download the image
            var a = document.createElement("a");
            console.log(component.state.img_full);
            a.href = "data:image/png;base64," + component.state.img_full; 
            a.download = "image.png"; 
            a.click(); 
        };
        const handleAddBookmark = () => {
            this.setState({is_bookmarked: true})
            fetch(SERVER_URL + '/add-bookmark?'+new URLSearchParams({
                filename: this.props.file_name
            }))
        };
        const handleRemoveBookmark = () => {
            this.setState({is_bookmarked: false})
            fetch(SERVER_URL + '/remove-bookmark?'+new URLSearchParams({
                filename: this.props.file_name
            }))
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
                src={this.state.has_image?`data:image/jpeg;base64,${this.state.img}`:loading_icon}
                style={{width: 180, height: 180, borderRadius: 16}}
                onClick={() => {
                    if (!this.state.has_image) {
                        return;
                    }
                    this.props.set_zoom_image(
                        <ZoomedGeneratedImage 
                            key={'zoomed generated image '+this.props.file_name}
                            is_bookmarked={this.state.is_bookmarked} 
                            image_name={this.props.file_name} 
                            set_zoom_image={this.props.set_zoom_image}
                            handle_add_bookmark={handleAddBookmark}
                            handle_remove_bookmark={handleRemoveBookmark}
                            />);
                    }}
                />
            {this.state.isHovered && this.state.has_image && (
                <img src={image_download_icon} className="absolute bottom-7 right-2 w-5 h-5 cursor-pointer" onClick={handleDownload} /> 
                )}
            {this.state.isHovered && this.state.is_bookmarked && this.state.has_image && (
                <img src={bookmark_selected_icon} className="absolute bottom-7 right-8 w-5 h-5 cursor-pointer" onClick={handleRemoveBookmark} /> 
                )}
            {this.state.isHovered && !this.state.is_bookmarked && this.state.has_image && (
                <img src={bookmark_not_selected_icon} className="absolute bottom-7 right-8 w-5 h-5 cursor-pointer" onClick={handleAddBookmark} /> 
                )}

            </div>
        )
    }
}

export default GeneratedImage;