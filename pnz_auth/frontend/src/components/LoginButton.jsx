import React from "react";
import Button from "@mui/material/Button";

const LoginButton = ({ at }) => {
  return (
    <Button
      variant="contained"
      {...at}
      color="primary"
      sx={{ my: 2, display: "block", color: "black", fontWeight: 700 }}
    >
      Login
    </Button>
  );
};

export default LoginButton;
