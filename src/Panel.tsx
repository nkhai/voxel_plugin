// import React from 'react';
import { registerComponent, PluginComponentType } from "@fiftyone/plugins";
import * as fos from "@fiftyone/state";
import { useRecoilValue } from "recoil";
// import { Box } from '@mui/material/Box';
// import { TextField } from '@mui/material/TextField';
import { Box, Typography, TextField , InputAdornment} from "@mui/material";
import { VerticalAlignBottom } from '@mui/icons-material/VerticalAlignBottom';
export function Panel() {
  const dataset = useRecoilValue(fos.dataset);
  return (
    <div>
      <Box
      component="form"
      sx={{
        '& > :not(style)': { m: 1, width: '25ch' },
      }}
      noValidate
      autoComplete="off"
    >
      <div>Enter Attribute Name: *</div>
      <TextField id="outlined-basic" label="Outlined" variant="outlined" />
    </Box>
    <Box
      component="form"
      sx={{
        '& > :not(style)': { m: 1, width: '25ch' },
      }}
      noValidate
      autoComplete="off"
    >
      <div>Define class for Attribute: </div>
      <TextField
        id="input-with-icon-textfield"
        label="TextField"
        InputProps={{
          startAdornment: (
            <InputAdornment position="end">
              <VerticalAlignBottomIcon />
            </InputAdornment>
          ),
        }}
        variant="standard"
      />
    </Box>

  </div>
  );
}

registerComponent({
  name: "atlas_voxel",
  label: "atlas_voxel",
  component: Panel,
  type: PluginComponentType.Panel,
  activator,
});

function activator({ dataset }) {
  return true;
}
