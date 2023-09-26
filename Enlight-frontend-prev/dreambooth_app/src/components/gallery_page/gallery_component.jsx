import React from 'react'
import { SERVER_URL } from "../../config/config"
import Box from '@mui/material/Box';
import { ImageList, ImageListItem } from '@mui/material';
import GalleryImage from './gallery_image';
var listOfImages = [];
// Component for showing the bookmarked projects
class GalleryComponent extends React.Component{
    state = {
        bookmarkedImageCounter: 0, // number of existing bookmarked images
        columns: 5, // number of columns in the generated images grid
        bookmarkedImages: [], // list of bookmarked images
    };
    importAll(r) {

        return r.keys().map(r);
    }

    updateImgSize = () => {
        const width = window.innerWidth;
        console.log('window size');

        let img_size = 180.0;

        if (width >= 1400) {
            img_size = 180.0;
        } else if (width >= 1260) {
            img_size = 160.0;
        } else if (width >= 1000) {
            img_size = 140.0;
        } else if (width >= 800) {
            img_size = 120.0;
        } else if (width >= 700) {
            img_size = 100.0;
        } else {
            img_size = 80.0;
        }
        console.log(width, img_size);

        // if (img_size < 100.0) {
        //     img_size = 100.0;
        // }
        this.setState({ img_size });

    };

    componentWillUnmount() {
        window.removeEventListener('resize', this.updateImgSize);
    };


    componentWillMount() {
        this.updateImgSize();
        window.addEventListener('resize', this.updateImgSize);

        const product_name = this.props.product;
        console.log(product_name);

        //listOfImages = this.importAll(require.context(`../../gallery/`, true, /\.(png|jpe?g|svg)$/));
        listOfImages = [
            'https://storage.googleapis.com/landingpage-images/gallery_page/0-hats/1.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/0-hats/a%20photo%20of%20sks%20wool%20brim%20hat%20on%20a%20asian%20female%20fashion%20model%2C%20fashion%2C%20photography%20style%2C%20high-resolution.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/0-hats/a%20photo%20of%20sks%20wool%20brim%20hat%20on%20a%20black%20african%20female%20fashion%20model%2C%20fashion%2C%20photography%20style%2C%20high-resolution.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/0-hats/a%20photo%20of%20sks%20wool%20brim%20hat%20on%20a%20blonde%20female%20fashion%20model%2C%20fashion%2C%20photography%20style%2C%20high-resolution.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/0-hats/a%20photo%20of%20sks%20wool%20brim%20hat%20on%20a%20female%20fashion%20model%2C%20fashion%2C%20photography%20style%2C%20high-resolution.png',

            'https://storage.googleapis.com/landingpage-images/gallery_page/1-shoes/0.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/1-shoes/a%20photo%20of%20a%20sks%20running%20shoes%20on%20the%20moon%20surface%2C%20high-resolution%2C%20moon%20crater%2C%20digital%20art%2C%20super%20realistic.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/1-shoes/a%20photo%20of%20a%20sks%20running%20shoes%2C%20a%20giant%20iceberg%2C%20the%20frozen%20artic%20ocean%2C%20ice%20splashing%2C%20photography%20style%2C%20super-realistic.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/1-shoes/a%20photo%20of%20a%20sks%20running%20shoes%2C%20a%20nebula%20in%20space%2C%20dreamlike%2C%20symbolism%2C%20surrealism%2C%20symbol%2C%20surreal%2C%20abstract%2C%20texture%2C%20concept%20art%2C%208k%2C%20shadowed%2C%20lightrays%2C%20atmospheric%2C%20octane%20render%2C%20nebula%2C%20stars%20--uplight.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/1-shoes/a%20photo%20of%20a%20sks%20running%20shoes%2C%20beautiful%20winter%20night%20landscape%20with%20mountains%20and%20trees%20in%20snow%2C%20wide%20angle%2C%20crystal%3A%3A4%20emitting%20glitter%3A%3A1%20global%20illumination%2C%20path%20landscape%20Asher%20brown%20Durand%2C%20rendered%20in%20octane%20.png',

            'https://storage.googleapis.com/landingpage-images/gallery_page/2-perfume/0.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/2-perfume/A%20photo%20of%20a%20sks%20dior%20perfume%20in%20a%20garden%20of%20white%20rose%2C%20hyper-realistic%2C%20high%20resolution%2C%20warm%20sunshine%2C%20elegant%2C%208k%2C%20cinematic%20light%2C%20photography%20style.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/2-perfume/A%20photo%20of%20a%20sks%20dior%20perfume%20on%20the%20beach%2C%20beautiful%20sunset%20and%20sea%20in%20the%20background%2C%20hyper-realistic%2C%20high%20resolution%2C%20elegant%2C%208k%2C%20cinematic%20light%2C%20photography%20style.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/2-perfume/A%20photo%20of%20a%20sks%20dior%20perfume%2C%20Eiffel%20tower%2C%20city%20light%2C%20night%2C%20romantic%2C%20photography%20style.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/2-perfume/A%20photo%20of%20a%20sks%20dior%20perfume%2C%20blue%20dorm%20churchs%2C%20view%20of%20oia%20town%20in%20santorini%20island%20in%20greece%2C%20cinamatic%20light%2C%20super%20detailed%2C%20hyper-realistic%2C%208k%2C%20photography%2C%20high-resolution.png',

            'https://storage.googleapis.com/landingpage-images/gallery_page/3-grill/0.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/3-grill/A%20photo%20of%20a%20sks%20charcoal%20grill%2C%20in%20the%20backyard%2C%20photorealistic%2C%20high-resolution.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/3-grill/a%20photo%20of%20a%20sks%20charcoal%20grill%20near%20a%20lake%2C%20photography%20style%2C%20high-resolution.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/3-grill/a%20photo%20of%20a%20sks%20charcoal%20grill%2C%20on%20the%20beach%2C%20ocean%2C%20sunset%2C%20photography%20style.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/3-grill/a%20photo%20of%20a%20sks%20charcoal%20grill%2C%20woods%2C%20beautiful%20forest%2C%20photography%20style.png',

            'https://storage.googleapis.com/landingpage-images/gallery_page/4-shelf/0.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/4-shelf/a%20photo%20of%20a%20sks%20shelf%2C%20european%20style%20living%20room%2C%20interior%20design%2C%20photography%20style.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/4-shelf/a%20photo%20of%20sks%20bookshelf%20in%20a%20sunny%20living%20room%2C%20reading%20couch%2C%20%20photography%20style%2C%20high-resolution%2C.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/4-shelf/a%20photo%20of%20sks%20bookshelf%20in%20a%20sunny%20living%20room%2C%20reading%20couch%2C%20%20photography%20style%2C%20high-resolution.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/4-shelf/a%20photo%20of%20sks%20bookshelf%20in%20a%20sunny%20living%20room%2C%20red-brick%20wall%2C%20%20photography%20style%2C%20high-resolution.png',

            'https://storage.googleapis.com/landingpage-images/gallery_page/5-table/0.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/5-table/a%20photo%20of%20a%20coffee%20table%2C%20interior%20design%2C%20high-resolution%2C%20brighe%20sunlight.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/5-table/a%20photo%20of%20a%20coffee%20table%2C%20interior%20design%2C%20high-resolution%2C%20warm%20sunlight.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/5-table/a%20photo%20of%20a%20coffee%20table%2C%20interior%20design%2C%20high-resolution%2C%20wooden%20floor.png',
            'https://storage.googleapis.com/landingpage-images/gallery_page/5-table/a%20photo%20of%20a%20coffee%20table%2C%20interior%20design%2C%20high-resolution.png',



        ]

    }

    updateColumns = () => {
    const width = window.innerWidth;
    let columns = 5;
    this.setState({ columns });
    };


    // before rendering the component, fetch the existing bookmarked images from the server
    componentDidMount() {
        // update the number of columns in the generated images grid
        this.updateColumns();
        window.addEventListener('resize', this.updateColumns);

        console.log('In GalleryComponent');
        console.log(listOfImages)
    }

    render() {
        return (

            <div className='w-full bg-no-repeat bg-main-bg dark:bg-main-dark-bg border-t-1 border-gray-300 dark:border-gray-900'>

                {/* Show bookmarked Images */}
                <div className="flex flex-wrap justify-center dark:bg-main-dark-bg dark:text-gray-200 w-full pt-2">
                    <div className="content-center dark:text-gray-200 bg-transparent rounded-xl w-810 ml-6 mr-6 bg-no-repeat bg-cover bg-center">
                        <div className="flex flex-nowrap  ">
                            <div className="flex w-200 h-200 ml-10 mr-10 mt-10 mb-2">
                                <ImageList
                                    cols={this.state.columns}
                                    rowHeight={this.state.img_size * 1.1}
                                    margin={1}
                                    style={{ overflow: "hidden" }}>
                                    {/*Fixme: remove the hardcoding of #colums=5*/}
                                    {listOfImages.map((image, index) => (

                                        <ImageListItem key={'gallery image '+index} sx={{ml:(index % 5 > 0)?2.0:0.0}}>

                                            <GalleryImage image={image} index={index} img_size={this.state.img_size} coloums={this.state.columns} set_zoom_image={this.props.set_zoom_image}/>
                                        </ImageListItem>
                                        ))}
                                </ImageList>

                            </div>
                        </div>
                    </div>
                </div>

            </div>);
    }
}

export default GalleryComponent;