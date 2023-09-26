import React, { Component, useEffect, useState } from 'react'
import { SERVER_URL } from "../../config/config"
import image_download_icon from '../../data/image-download.svg';
import ZoomedBookmarkedComponent from './zoomed_bookmarked_image';
import bookmark_delete_icon from '../../data/bookmark-delete-icon.svg';
import cache from '../../utils/cache';
import loading_icon from '../../data/loading-icon.svg';

// A BookmarkedImage is a single bookmarked image by the model
class BookmarkedImage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isHovered: false,
            img: '',
            has_image: false,
        };
    };

    componentDidMount() {
        const cacheKey = 'generated image ' + this.props.image_name;
        const cachedImage = cache.get(cacheKey);
        console.log(cachedImage);
        console.log(cacheKey);
        console.log(this.props.image_name);
        if (cachedImage) {
            this.setState({img: cachedImage, has_image: true});
        } else {
            console.log('not cached bookmarked image');
            console.log(this.props.image_name);
            // Get the image from the server
            fetch(SERVER_URL + '/get-generated-image-data-low-res?'+new URLSearchParams({
                image_name: this.props.image_name
            }), {method: 'GET'})
            .then(response => response.json())
            .then(data => {
                console.log(data);
                this.setState({img: data.image_data, has_image: true});
                cache.set(cacheKey, data.image_data);
            }
            );
        }
    }

    render() {
        const handleDownload = async () => {
            var component = this;
            const cacheKey = 'full resolution generated image ' + this.props.image_name;
            const cachedImage = cache.get(cacheKey);
            if (cachedImage) {
                component.setState({img_full: cachedImage});
                console.log('using cached image');
            } else {
                // Get the image from the server
                var response = await fetch(SERVER_URL + '/get-generated-image-data?'+new URLSearchParams({
                    image_name: component.props.image_name
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
        const handleMouseEnter = () => {
            this.setState({ isHovered: true });
        };
    
        const handleMouseLeave = () => {
            this.setState({ isHovered: false });
        };
        return (
            <div className='image-container' onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
            <img
                src={this.state.has_image ? `data:image/jpeg;base64,${this.state.img}` : loading_icon}
                style={{width: 180, height: 180, borderRadius: 16}}
                alt='Helpful alt text'
                onClick={() => {
                    this.props.set_zoom_image(<ZoomedBookmarkedComponent handle_delete={this.props.handle_delete} image_name={this.props.image_name} set_zoom_image={this.props.set_zoom_image}/>); 
                    }}
                />
            {this.state.isHovered && (
                <img src={image_download_icon} className="absolute bottom-7 right-2 w-5 h-5 cursor-pointer" onClick={handleDownload} /> 
                )}
            {this.state.isHovered && (
                <img src={bookmark_delete_icon} className="absolute bottom-7 right-8 w-5 h-5 cursor-pointer" onClick={()=>{this.props.handle_delete(this.props.image_name)}} /> 
            )}

            </div>
        )
    }
}

export default BookmarkedImage;