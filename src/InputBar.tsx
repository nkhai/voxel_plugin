import React, { useState, useRef, useEffect } from "react";
import {
  TextField,
  InputAdornment,
  OutlinedInput,
  IconButton,
} from "@mui/material";
import SubdirectoryArrowLeftIcon from '@mui/icons-material/SubdirectoryArrowLeft';
import { useRecoilState } from "recoil";
import { atoms } from "./state";

const InputBar = ({ hasMessages, disabled, onMessageSend,placeHoldermsg, needIcon ,bottomRef }) => {
  const [waiting, setWaiting] = useRecoilState(atoms.waiting)
  const [message, setMessage] = useRecoilState(atoms.input)
  const inputRef = useRef(null)

  function sendMessage() {
    if (message.trim()) {
      setWaiting(true)
      onMessageSend(message)
      setMessage('')
    }
  }

  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      sendMessage();
    }
  };

  useEffect(() => {
    if (!disabled && inputRef.current) {
      inputRef.current.focus();
    }
  }, [disabled]);

  const showAdornment = !disabled && message.trim().length > 0;

  return (
    <div style={{ padding: "0.5rem" }}>
      {needIcon === "true" ?
      <OutlinedInput
        ref={inputRef}
        autofocus
        fullWidth
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        variant="outlined"
        disabled={disabled}
        size="large"
        placeholder={placeHoldermsg}
        endAdornment={
          <IconButton disabled={!showAdornment} onClick={sendMessage}>
            <SubdirectoryArrowLeftIcon style={{ opacity: showAdornment ? 1 : 1 }} />
          </IconButton>}
        
      /> :
      <OutlinedInput
      ref={inputRef}
      autofocus
      fullWidth
      value={message}
      onChange={(e) => setMessage(e.target.value)}
      onKeyPress={handleKeyPress}
      variant="outlined"
      disabled={disabled}
      size="large"
      placeholder={placeHoldermsg}
      
    />
        }
      <div ref={bottomRef} />
    </div>
  );
};

export default InputBar;
