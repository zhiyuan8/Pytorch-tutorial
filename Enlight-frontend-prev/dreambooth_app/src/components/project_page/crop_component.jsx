import React, { Component, useState } from 'react'
import { SERVER_URL } from "../../config/config"
import close_icon from '../../data/close-icon.svg';
import check_icon from '../../data/check-icon-green.svg';
import cancel_icon from '../../data/cancel-icon-gray.svg';
import loading_icon from '../../data/loading-icon.svg';
import cache from '../../utils/cache';
import ReactCrop from 'react-image-crop';
import 'react-image-crop/dist/ReactCrop.css'

// A CropComponent is a component that helps a user to crop an uploaded image
class CropComponent extends Component {
    constructor(props) {
        super(props);
        this.state = {
            has_image: false,
            img: '',
            crop: {
                unit: '%', // Can be 'px' or '%'
                x: 0,
                y: 0,
                width: 50,
                height: 50
              }
        };
    };

    componentDidMount() {
        const img = new Image();
        img.src = this.props.image_src;
        img.onload = () => {
            if (img.height < img.width) {
                this.setState({crop: {
                    unit: '%', // Can be 'px' or '%'
                    x: 0 * img.height / img.width + 100 * (1 - img.height/img.width) / 2,
                    y: 0,
                    width: 100 * img.height / img.width,
                    height: 100
                  }})
            }
            else {
                this.setState({crop: {
                    unit: '%', // Can be 'px' or '%'
                    x: 0,
                    y: 0 * img.width / img.height + 100 * (1 - img.width/img.height) / 2,
                    width: 100,
                    height: 100 * img.width / img.height
                  }})
            }
        }
    }
    
    render() {
        return (
            <div className='image-container'>
                <ReactCrop crop={this.state.crop} aspect={1} keepSelection={true} className="max-h-screenh_80 max-w-screenw_80"
                    onChange={(crop, percentCrop) => {this.setState({crop: percentCrop});}}>
                    <img src={this.props.image_src} className="max-h-full max-w-full"
                    />
                </ReactCrop>
                <div className="flex absolute -bottom-16 right-0 w-32 h-16 bg-white hover:bg-gray-100 dark:bg-gray-900 dark:hover:bg-gray-800 cursor-pointer rounded-xl place-content-center items-center" 
                    onClick={() => {
                        // get the cropped image, note that the crop can be in percentage or in pixels
                        const img = new Image();
                        img.setAttribute('crossOrigin', 'anonymous');
                        img.src = this.props.image_src;
                        img.onload = () => {
                            // get the cropped image, note that the crop is in percentage
                            const canvas = document.createElement('canvas');
                            canvas.width = this.state.crop.width / 100 * img.width;
                            canvas.height = this.state.crop.height / 100 * img.height;
                            const ctx = canvas.getContext('2d');
                            ctx.drawImage(
                                img,
                                this.state.crop.x / 100 * img.width,
                                this.state.crop.y / 100 * img.height,
                                this.state.crop.width / 100 * img.width,
                                this.state.crop.height / 100 * img.height,
                                0,
                                0,
                                this.state.crop.width / 100 * img.width,
                                this.state.crop.height / 100 * img.height
                            );
                            const base64Image = canvas.toDataURL('image/jpeg');

                            // turn base64 image into blob
                            const splitDataURI = base64Image.split(',')
                            const byteString = splitDataURI[0].indexOf('base64') >= 0 ? atob(splitDataURI[1]) : decodeURI(splitDataURI[1])
                            const mimeString = splitDataURI[0].split(':')[1].split(';')[0]
                    
                            const ia = new Uint8Array(byteString.length)
                            for (let i = 0; i < byteString.length; i++)
                                ia[i] = byteString.charCodeAt(i)
                    
                            const blob = new Blob([ia], { type: mimeString })

                            // turn base64 image into form data
                            const formData = new FormData();
                            formData.append('file', blob);
                            this.props.set_cropped_image(formData);
                        }
                        // close the crop component
                        this.props.set_zoom_image(null);}}> 
                    <img src={check_icon} className="w-10 h-10" />
                </div>

                <div className="flex absolute -bottom-16 left-0 w-32 h-16 bg-white hover:bg-gray-100 dark:bg-gray-900 dark:hover:bg-gray-800 cursor-pointer rounded-xl place-content-center items-center" 
                    onClick={() => {this.props.set_zoom_image(null);}}> 
                    <img src={cancel_icon} className="w-10 h-10" />
                </div>
            </div>
        )
    }
}

export default CropComponent;
