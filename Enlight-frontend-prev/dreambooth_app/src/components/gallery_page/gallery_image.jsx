import React, { Component, useEffect, useState } from 'react'
import { SERVER_URL } from "../../config/config"
import image_download_icon from '../../data/image-download.svg';
import east_white from '../../data/east_white_48dp.svg';
import east_black from '../../data/east_black_48dp.svg';
import ZoomedBookmarkedComponent from './zoomed_bookmarked_image';
import CopyAllRoundedIcon from '@mui/icons-material/CopyAllRounded';
import ContentCopyRoundedIcon from '@mui/icons-material/ContentCopyRounded';
import bookmark_delete_icon from "../../data/bookmark-delete-icon.svg";
import "../../App.css"


// A BookmarkedImage is a single bookmarked image by the model
class GalleryImage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isHovered: false,
            copied: false
        };
    };

    render() {
        const {img, has_image} = this.state;
        const handleDownload = () => {
            // get the image name from the image url
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

        const copyToClipboard = (textToCopy) => {
            navigator.clipboard.writeText(textToCopy).then(
              () => {
                this.setState({ copied: true });
                // changing back to default state after 2 seconds.
                setTimeout(() => {
                  this.setState({ copied: false});
                }, 20000);
              },
            );
        };

        const extractPrompt = (prompt) => {
            return prompt.split("/")[6].split('.')[0].replace(/%20/g, ' ').replace(/%2C/g, ' ').replace(/%3A/g, ' ').replace('sks', '').replace(/  /g, ' ')
        }

        return (
            <div className='image-container' onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
            <img
            src={this.props.image}
            style={{width: this.props.img_size, height: this.props.img_size, borderRadius: 12}}
            alt='Helpful alt text'
            onClick={() => {
                this.props.set_zoom_image(<ZoomedBookmarkedComponent image_name={this.props.image_name} set_zoom_image={this.props.set_zoom_image}/>);
                }}
            />

            {this.state.isHovered && this.props.index % 5 > 0 && (
                <div className="gallery-dark-overlay" style={{borderRadius: 12}}>
                <div className="absolute top-5 bottom-0 left-2 cursor-pointer">
                    <div className="overflow-y-auto h-32 ...">
                         <p className="fontsize-11 text-white">
                             {extractPrompt(this.props.image)}
                         </p>
                    </div>
                </div>
                <div className="absolute bottom-3 right-3 w-5 h-5 cursor-pointer">
                  <button onClick={() => copyToClipboard(extractPrompt(this.props.image))}>
                      {this.state.copied ?
                          <ContentCopyRoundedIcon sx={{color: "white"}}/> :
                          <CopyAllRoundedIcon sx={{color: "white"}}/>}

                  </button>
                </div>
                </div>
            )}

            {/*Fixme: remove the hardcoding of #colums=5*/}
            {this.props.index % 5 == 0 && (
                <div className="gallery-arrow">
                    <img src={east_black}/>
                </div>
                )}
            </div>

        )
    }
}

export default GalleryImage;