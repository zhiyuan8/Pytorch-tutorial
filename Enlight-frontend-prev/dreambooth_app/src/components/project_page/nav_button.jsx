import React, { Component, useState } from 'react'
import { TooltipComponent } from '@syncfusion/ej2-react-popups';

// Button for showing the menu when the screen size is small
const NavButton = ({ title, customFunc, icon, color, dotColor }) => {
    return (
      <TooltipComponent content={title} position="BottomCenter">
        <button type='button' onClick={customFunc} style={{ color }} className="rounded-full relative text-xl p-3 dark:hover:bg-gray-700 hover:bg-gray-200">
          <span style = {{background: dotColor}}
            className="absolute inline-flex rounded-full h-2 w-2 right-2 top-2">
          </span>
          {icon}
        </button>
      </TooltipComponent>
    );    
  }

  export default NavButton;
