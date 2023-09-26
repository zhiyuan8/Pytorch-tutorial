import React, { Component, useState } from 'react'
import Box from '@mui/material/Box';
import LinearProgress from '@mui/material/LinearProgress';
import Typography from '@mui/material/Typography';

// Progress bar
function LinearProgressWithLabel(props) {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', mt: 0
       }}>
        <Box sx={{ width: '100%', mr: 1 }}>
          <LinearProgress variant="determinate" value={props.value} />
        </Box>
        <Box sx={{ minWidth: 35 }}>
          <Typography variant="body2" color={props.color}>{`${Math.round(
            props.value,
          )}%`}</Typography>
        </Box>
      </Box>
    );
}

export default LinearProgressWithLabel;