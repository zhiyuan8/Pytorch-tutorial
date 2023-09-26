import React from 'react'
import { SERVER_URL } from "../../config/config"
import Box from '@mui/material/Box';
import { ImageList, ImageListItem } from '@mui/material';
import BookmarkedImage from './bookmarked_image';

// Component for showing the bookmarked projects
class BookmarkComponent extends React.Component{
    state = {
        columns: 4, // number of columns in the generated images grid
        bookmarkedImages: []
    };    

    componentWillUnmount() {
        window.removeEventListener('resize', this.updateColumns);
    };

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

    // handle the deletion of a bookmarked image
    handle_delete = (filename) => {
        fetch(SERVER_URL + '/remove-bookmark?'+new URLSearchParams({
            filename: filename}));        
        // remove the image from the bookmarked images list
        this.setState({ bookmarkedImages: this.state.bookmarkedImages.filter((image) => image.filename != filename) });
    }

    componentDidMount() {
        this.setState({ bookmarkedImages: this.props.bookmarked_images });
    }

    render() {
        return (
            this.state.bookmarkedImages.length>0?
            <div className='w-full bg-no-repeat bg-main-bg dark:bg-main-dark-bg border-t-1 border-gray-300 dark:border-gray-900'>
                {/* Show project name */}

                {/* <div className="justify-center flex flex-wrap dark:text-gray-200 mt-1 w-full pt-3 pb-3">
                    <div className='w-800 flex flex-wrap justify-between items-center'>
                        <Box sx={{ml:4, pt:1, pr:2, pb:1, flex: 1}}>
                            <p><span> {this.props.project_name} </span> </p>
                        </Box>
                    </div>
                </div> */}

                {/* Show bookmarked Images */}
                <div className="flex flex-wrap justify-center dark:bg-main-dark-bg dark:text-gray-200 w-full pt-2">
                    <div className="content-center dark:text-gray-200 bg-transparent rounded-xl w-800 ml-6 mr-6 bg-no-repeat bg-cover bg-center">
                        <div className="flex flex-nowrap  ">
                            <div className="flex w-200 h-200 ml-3 mr-1 mb-2">
                                <ImageList
                                    cols={this.state.columns}
                                    rowHeight={200}
                                    margin={1}>
                                    {this.state.bookmarkedImages.map((item) => (
                                        <ImageListItem key={'bookmarked image '+item.filename} sx={{m:0.22}}>
                                            <BookmarkedImage handle_delete={this.handle_delete} image_name={item.filename} set_zoom_image={this.props.set_zoom_image}/> 
                                        </ImageListItem>
                                        ))}
                                </ImageList>
                            </div>
                        </div>
                    </div>
                </div>

            </div>:<></>);
    }
}

export default BookmarkComponent;