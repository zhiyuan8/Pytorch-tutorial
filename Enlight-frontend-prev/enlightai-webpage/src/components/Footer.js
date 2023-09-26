import React from 'react'
import { SocialIcon } from 'react-social-icons';
import logo from '../imgs/enlight-logo-no-icon.svg';

const Footer = ({handleScroll}) => {
    const today = new Date();

    const logosize = 40;

    return (
        <footer>
            <div className = 'gridabove SizeControl pt-2'>
                <img src={logo} alt='EnlightAI Logo'/>
                <span className='hand-cursor' onClick={() => handleScroll("whatwedo")}>
                    What we do
                </span>
                <span className='hand-cursor' onClick={() => handleScroll("howitwork")}>
                    How it works
                </span>
                <span className='hand-cursor' onClick={() => handleScroll("contactus")}>
                    Try for free
                </span>
            </div>
            <div className='gridbox SizeControl relative ' style={{ height: logosize}}>
                {/* <SocialIcon url="https://www.facebook.com/" 
                fgColor='#818286' bgColor='#181C1E' style={{ height: logosize, width: logosize }}/> */}
                {/* <SocialIcon url="https://twitter.com/" 
                fgColor='#818286' bgColor='#181C1E' style={{ height: logosize, width: logosize }}
                /> */}
                {/* <SocialIcon url="https://www.instagram.com/" 
                fgColor='#818286' bgColor='#181C1E' style={{ height: logosize, width: logosize }}
                /> */}
                <p className='absolute right-0 top-1'>
                    Copyright @ EnlightAI. All rights reserved
                </p>
            </div>
        </footer>
    )
}

export default Footer