// contact information including first name, last name,
// email, phone number and a message.
import React from 'react';
import { useState } from 'react';
import api from '../api/contact';

const ContactForm = ({handScroll}) => {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [submited, setSubmited] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try{
            setSubmited(true);
            // eslint-disable-next-line
            const _ = await api.post("/contact-save",
                {
                    "firstname": firstName,
                    "lastname": lastName,
                    "email": email,
                    "message": message
                }
            )
            // handScroll('whatwedo');
        } catch (err) {
            console.log(err);
            console.log(firstName, lastName, email, message);
            // handScroll('whatwedo');
        }
        
    }

    const handleReset = async (e) => {
        setFirstName('');
        setLastName('');
        setEmail('');
        setMessage('');
        setSubmited(false);    
    }

    return (
        <div className='ContactDiv SizeControl'>
            <div>
                <form className='ContactForm' onSubmit={handleSubmit} onReset={handleReset}>
                    <div className='ColumnInput'>
                        <input type='text' 
                            placeholder='First Name'
                            required = {true} 
                            disabled={submited}
                            onChange={(e) => setFirstName(e.target.value)}
                        />
                        <input type='text' placeholder='Last Name'
                            required = {true}
                            disabled={submited}
                            onChange={(e) => setLastName(e.target.value)}
                        />
                        <input className="EmailInput" type='email' placeholder='Email'
                            required = {true}
                            disabled={submited}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <textarea placeholder='What are you using it for?'
                        disabled={submited}
                              onChange={(e) => setMessage(e.target.value)}
                    />
                    <button type='reset'>Reset</button>

                    {!submited && <button type='submit'>Submit</button>}
                    {submited && <button disabled={true}>Submitted!</button>}
                </form>
            </div>
            <div className='ContactPara'>
                <p>Enlight is an AI platform that helps e-commerce businesses 
                    generate engaging product images.</p>
                
                <p>Contact us to learn more about how 
                    Enlight can help your business. </p>
            </div>
        </div>
    )
}

export default ContactForm;