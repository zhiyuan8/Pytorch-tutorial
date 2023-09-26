import React from 'react';
import arrowlogo1 from '../imgs/arrow_logo1.svg';
import arrowlogo2 from '../imgs/arrow_logo2.svg';
import voicelogobefore from '../imgs/voice_box_before.svg';
import voicelogoafter from '../imgs/voice_box_after.svg';

const WhatWeDo = ({handleScroll}) => {
    return (
        <div className='whatwedo SizeControl'>
            <div className='whatwedo-box'>
                <p id="whatwedo">Create product images easily and creatively</p>
                <img src={arrowlogo1} alt='arrowlogo1' /> 
                <p className='hand-cursor' 
                   onClick={() => handleScroll("contactus")}>
                    Try it now
                </p>
            </div>

            <div className='whatwedo-image'>
                <img  className="imageSizeControl"
                      src={voicelogobefore}
                      alt='voicelogobefore'
                />
                <img  src={arrowlogo2} 
                      alt='arrowlogo2'
                      className='logoSizeControl'
                />
                <img  className="imageSizeControl"
                      src={voicelogoafter}
                      alt='voicelogoafter'
                />
            </div>
        </div>
    )
}

export default WhatWeDo;