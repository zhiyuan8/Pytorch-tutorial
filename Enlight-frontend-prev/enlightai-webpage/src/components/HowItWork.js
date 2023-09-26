import React from "react";



const HowItWork = ({title, description, image, isTextLeft}) => {
    if (isTextLeft){
        return (
            <div className='howitwork SizeControl'>
                <div className="description">
                    <span>{title}</span>
                    <p>{description}</p>
                </div>
                <div>
                    <img src={image} alt={title}/>
                </div>
            </div>
        )
    } else {
        return (
            <div className='howitwork SizeControl'>
                <div>
                    <img src={image} alt={title}/>
                </div>
                <div className="description">
                    <span>{title}</span>
                    <p>{description}</p>
                </div>
            </div>
        )
    }
}

export default HowItWork;