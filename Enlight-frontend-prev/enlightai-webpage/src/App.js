// import Header and Footer
import Footer from './components/Footer';
import Nav from './components/Nav';
import ContactForm from './components/ContactForm';
import WhatWeDo from './components/WhatWeDo';
import HowItWork from './components/HowItWork';


function App() {
  // define three titles as an array
  const titles = ['Diverse Environments', 'Tailored Generation', 'Creative Visuals'];
  // define three descriptions as an array
  const descriptions = ["Unlock unlimited product backgrounds by simply changing text prompts.",
                        "Customize project images based on current events and customer preferences.",
                        "Generate high-quality visual effects instantly with unlimited imagination."];
  // define three images as an array
  const images = [
    "https://cdn.enlight-ai.com/landpage-perfume.png",
    "https://cdn.enlight-ai.com/landpage-hat.png",
    "https://cdn.enlight-ai.com/landpage-shoes.png"
  ]

  /* Now, define scroll functions to different element by id */
  const handleScroll = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth'});
    }
  }


  return (
    <div className='overflow-x-hidden'>
      <main >
          <div className='background-image'>
              <Nav handleScroll={handleScroll}/>
              <WhatWeDo handleScroll={handleScroll}/>
          </div>
          
          <div>
              <h3 id="howitwork" className='text-4xl'>How can Enlight AI enhance product imagery?</h3>
              {titles.map((title, index) => {
                  return  <HowItWork title={title}
                                    description={descriptions[index]} 
                                    image={images[index]}
                                    key={index} isTextLeft={
                                        index % 2 === 0 ? true : false
                          }/>
              })}
          </div>

          <div>
              <h3 id="contactus" className='text-4xl'>Get access to our product now.</h3>
              <ContactForm handScroll={handleScroll}/>
          </div>
      </main>
      <Footer handleScroll={handleScroll}/>
    </div>
  );
}

export default App;
