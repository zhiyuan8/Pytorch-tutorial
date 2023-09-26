import React, { Component } from 'react'
import { SERVER_URL } from "../../config/config"
import close_icon from '../../data/close-icon.svg';
import image_download_icon from '../../data/image-download.svg';


// A ZoomedBookmarkedComponent is a single generated image that is zoomed in
class ZoomedBookmarkedComponent extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isHovered: false
        };
    };

    render() {
        const handleDownload = () => {
            // get the image
            fetch(SERVER_URL + '/get-image?'+new URLSearchParams({
                image_name: this.props.image_name
            }), {method: "GET"})
            .then(res => res.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(new Blob([blob]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute("download", "image.png");
                document.body.appendChild(link);
                link.click();
            })
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
                    src={SERVER_URL + "/get-image?"+new URLSearchParams({
                        image_name: this.props.image_name
                    })}
                    style={{width: '100%', borderRadius: 16}}
                    alt='Helpful alt text'
                    />
                {this.state.isHovered && (
                    <img src={image_download_icon} className="absolute bottom-3 right-3 w-5 h-5 cursor-pointer" onClick={handleDownload} />
                    )}
                <div className="absolute top-3 -right-10 w-10 h-10 bg-white hover:bg-gray-100 dark:bg-gray-900 dark:hover:bg-gray-500 opacity-80 dark:opacity-50">
                    <img src={close_icon} className="cursor-pointer" onClick={() => {this.props.set_zoom_image(null);}} />
                </div>
            </div>
        )
    }
}

export default ZoomedBookmarkedComponent;