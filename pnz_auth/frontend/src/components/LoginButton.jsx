import React from "react";
import Button from "@mui/material/Button";
import { createTheme, ThemeProvider } from '@mui/material/styles';
const theme = createTheme({
  palette: {
    primary: {
      main: '#ffc428'
    }
  }
});

const LoginButton = ({ at }) => {
  return (
    <ThemeProvider theme={theme}>
      <Button
        variant="contained"
        {...at}
        color="primary"
        sx={{ my: 2, color: "#1A2238", fontWeight: 700, textTransform: 'none' }}
      >
      Login 
      </Button>
    </ThemeProvider>
  );
};

export default LoginButton;
