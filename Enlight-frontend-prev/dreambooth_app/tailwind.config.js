module.exports = {
    content: ['./src/**/*.{js,jsx,ts,tsx}'],
    darkMode: 'class',
    theme: {
      fontFamily: {
        serif: ['ui-serif', 'Georgia'],
        inter: ['Inter'],
        display: ['Inter'],
        body: ['Inter'],
        // display: ['Open Sans', 'sans-serif'],
        // body: ['Open Sans', 'sans-serif'],
      },
      extend: {
        transitionProperty: {
          'margin': 'margin',
        },
        fontSize: {
          14: '14px',
          16: '16px',
          20: '20px',
          24: '24px',
        },
        backgroundColor: {
          'main-bg': '#FAFBFB',
          'main-dark-bg': '#47494D',
          'secondary-dark-bg': '#232323',
          'secondary-light-bg': '#ffffff',
          'third-dark-bg': '#090909',
          'third-light-bg': '#e8e8e8',
          'generation-component-dark-bg': "#2C2F39",
          'generation-component-light-bg': "#cccccc",
          'light-gray': '#F7F7F7',
          'half-transparent': 'rgba(0, 0, 0, 0.5)',
        },
        borderWidth: {
          1: '1px',
        },
        borderColor: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
        width: {
          30: '30px',
          100: '100px',
          400: '400px',
          600: '600px',
          700: '700px',
          760: '760px',
          780: '780px',
          800: '800px',
          1000: '1000px',
          1200: '1200px',
          1400: '1400px',
          screenw_minus_240: 'calc(100vw - 240px)',
          screenw_80: '80vw',
          screenw: '100vw',
        },
        height: {
          50: '50px',
          60: '60px',
          80: '80px',
          100: '100px',
          screenh_80: '80vh',
          screen: '100vh',
          screen_minus_50: 'calc(100vh - 50px)',
          screen_minus_60: 'calc(100vh - 60px)',
          screen_minus_80: 'calc(100vh - 80px)',
          screen_minus_100: 'calc(100vh - 100px)',
          screen_minus_120: 'calc(100vh - 120px)',
          screen_minus_130: 'calc(100vh - 130px)',
          screen_minus_140: 'calc(100vh - 140px)',
        },
        minHeight: {
          590: '590px',
        },
        maxHeight: {
          100: '100px',
          200: '260px',
          590: '590px',
          screenh_80: '80vh',
          screenh: '100vh',
        },
        maxWidth: {
          screenw_80: '80vw',
          screenw: '100vw',
        }
      }, 
    },
    plugins: [],
  };