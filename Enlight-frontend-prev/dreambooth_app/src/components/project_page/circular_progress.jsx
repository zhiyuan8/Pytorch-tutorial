import React, { Component, useState } from 'react'
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import Typography from '@mui/material/Typography';

// Generation circular progress bar
function CircularProgressWithLabel(props) {
return (
    <Box sx={{ position: 'relative', display: 'inline-flex' }}>
    <CircularProgress variant="determinate" {...props} />
    <Box
        sx={{
        top: 0,
        left: 0,
        bottom: 0,
        right: 0,
        position: 'absolute',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        }}
    >
        <Typography variant="caption" component="div" color="white"  sx={{fontSize: 10}}>
        {`${Math.round(props.value)}%`}
        </Typography>
    </Box>
    </Box>
);
}

export default CircularProgressWithLabel;