import React from 'react';

// import the logo
import logo from '../imgs/enlight-logo-no-icon.svg';
import icon_logo from '../imgs/lightbulb-logo.svg';

const Nav = ({handleScroll}) => {
  return (
    <nav className='Nav SizeControl' >
      <div className='flex w-full justify-between flex-no-wrap items-center'>
        <div className='flex flex-no-wrap'>
          <img src={icon_logo} alt='Logo'/>
          <img src={logo} alt='Enlight AI' className='w-44 pl-4'/>
        </div>
        <p className='hand-cursor w-24 align-center' onClick={() => handleScroll("whatwedo")}>
          What we do</p>
        <p className='hand-cursor w-28 align-center' onClick={() => handleScroll("howitwork")}>
          How it works</p>
        {/* <p className='hand-cursor w-24' onClick={() => handleScroll("contactus")}>
          Try for free
          </p> */}
        <button className='boxDemo hand-cursor' onClick={() => handleScroll("contactus")}>
          Try for free
        </button>
      </div>
        <div></div>
    </nav>
  )
}

export default Nav