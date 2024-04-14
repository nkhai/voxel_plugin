import { Selector } from "@fiftyone/components";
import { PluginComponentType, registerComponent } from "@fiftyone/plugins";
import { usePanelStatePartial, usePanelTitle } from "@fiftyone/spaces";
import React, { useEffect } from "react";
import styled from "styled-components";
import { scrollbarStyles } from "@fiftyone/utilities";
import {
  OperatorPlacements,
  registerOperator,
  useOperatorExecutor,
} from "@fiftyone/operators";
import Chat from "./Chat";
import { Grid, Typography, Link, colors } from "@mui/material";
import InputBar from "./InputBar";
import { ShowMessage } from "./ShowMessage";
import { SendMessageToVoxelGPT } from "./SendMessageToVoxelGPT";
import { useRecoilValue } from "recoil";
import * as state from "./state";
import { Actions } from "./Actions";
import { Intro } from "./Intro";
import { ChatGPTAvatar } from "./avatars";
import Divider from '@mui/material/Divider';
import { Height } from "@mui/icons-material";
import Paper from '@mui/material/Paper';


import { styled } from '@mui/material/styles';
import { alignProperty } from "@mui/material/styles/cssUtils";

const DemoPaper = styled(Paper)(({ theme }) => ({
  width: 400,
  height: 400,
  padding: theme.spacing(2),
  ...theme.typography.body2,
  textAlign: 'center',
  bgcolor: 'gray',
  color: 'white',
  backgroundColor:'gray',
  ml: 0
  
}));
const PLUGIN_NAME = "atlas_plugin";

const ChatPanel = () => {
  const executor = useOperatorExecutor(
    `${PLUGIN_NAME}/send_message_to_voxelgpt`
  );
  const messages = useRecoilValue(state.atoms.messages);

  const handleNameMessageSend = (message) => {
    //executor.execute({ message });
    console.log("user input some name : " + message);
  };
  const handleMessageSend = (message) => {
    executor.execute({ message });
  };
  const data = executor.execute({ 'key':'' }).result;
console.log("some data: " + JSON.stringify(data));
  const receiving = useRecoilValue(state.atoms.receiving);
  const waiting = useRecoilValue(state.atoms.waiting);
  const hasMessages = false;

  return (
    <Grid
      container
      direction="row"
      spacing={2}
      sx={{ height: "20%" , width: '60%'}}
      style={{margin: '400px 0px 0px 0px', height: '150px'}}
      justifyContent="center"
    >
      {/* {!hasMessages && <Intro />} */}
      {hasMessages && (
        <Grid item lg={12}>
          <Chat />
        </Grid>
      )}
      <Grid
        item
        container
        sx={{ marginTop: hasMessages ? "auto" : undefined }}
        justifyContent="left"
      >
        <Grid item sm={12} md={12} lg={12}>
          Update Attriute or Class
        </Grid>
        <Divider  sx={{width:'100%', height:"1px"}} style={{ background: 'white' }} />
        <Grid item sm={6} md={6} lg={6}>
          <InputBar
            hasMessages='false'
            disabled={false}
            placeHoldermsg="Enter Attribute"
            needIcon="false"
            onMessageSend={handleNameMessageSend}
          />
          {/* <Typography
            variant="caption"
            sx={{ marginTop: "8px", display: "block", textAlign: "center" }}
          >
            VoxelGPT is in beta and may not understand certain queries.{" "}
            <Link href="https://github.com/voxel51/voxelgpt" target="_blank">
              Learn more
            </Link>
          </Typography> */}
        </Grid>
        <Divider  sx={{width:'100%', height:"1px"}} style={{ background: 'white' }} />
        <Grid item sm={4} md={4} lg={4}>
          <InputBar
            hasMessages={hasMessages}
            disabled={receiving || waiting}
            placeHoldermsg="Add new class here"
            needIcon="true"
            onMessageSend={handleMessageSend}
          />
          {/* <Typography
            variant="caption"
            sx={{ marginTop: "8px", display: "block", textAlign: "center" }}
          >
            VoxelGPT is in beta and may not understand certain queries.{" "}
            <Link href="https://github.com/voxel51/voxelgpt" target="_blank">
              Learn more
            </Link>
          </Typography> */}
        </Grid>
        <Grid item sm={8} md={8} lg={8}>
          <DemoPaper elevation={3} variant="outlined" >
            <div style={{textAlign:"left"}}>X class Deine:</div>
            {JSON.stringify(data)}
          </DemoPaper>
          {/* <Typography
            variant="caption"
            sx={{ marginTop: "8px", display: "block", textAlign: "center" }}
          >
            VoxelGPT is in beta and may not understand certain queries.{" "}
            <Link href="https://github.com/voxel51/voxelgpt" target="_blank">
              Learn more
            </Link>
          </Typography> */}
        </Grid>
      </Grid>
    </Grid>
  );
};

registerComponent({
  name: "voxelgpt",
  label: "VoxelGPT",
  component: ChatPanel,
  type: PluginComponentType.Panel,
  activator: () => true,
  Icon: () => <ChatGPTAvatar size={"1rem"} style={{ marginRight: "0.5rem" }} />,
});

registerOperator(ShowMessage, PLUGIN_NAME);
registerOperator(SendMessageToVoxelGPT, PLUGIN_NAME);
