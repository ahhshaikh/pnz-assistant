import React, { useState } from "react";
import "./NavBar.css";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import Menu from "@mui/material/Menu";
import MenuIcon from "@mui/icons-material/Menu";
import Container from "@mui/material/Container";
// import Button from "@mui/material/Button";
import MenuItem from "@mui/material/MenuItem";
import PNZLogin from "../components/PNZLogin";

const theme = createTheme({
  palette: {
    primary: {
      main: "#ffffff",
    },
    secondary: {
      main: "#000000",
    },
    bg:{
      main: '#1A2238'
    }
  },
});

function NavBar() {
  const [anchorElNav, setAnchorElNav] = useState(null);

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  return (
    <>
      <ThemeProvider theme={theme}>
        <AppBar position="static" sx={{ backgroundColor: "#1A2238" }}>
          <Container maxWidth="xl">
            <Toolbar
              disableGutters
              sx={{
                display: { xs: "flex" },
                flexDirection: "row",
                backgroundColor: "#1A2238",
                justifyContent: "space-between",
              }}
            >
              <div style={{ display: "flex" }}>
                <Typography
                  variant="h6"
                  color="primary"
                  sx={{
                    display: { xs: "none", md: "flex" },
                    fontFamily: "monospace",
                    fontWeight: 700,
                    letterSpacing: ".3rem",
                    textDecoration: "none",
                  }}
                  noWrap
                >
                  payments
                </Typography>
                <Typography
                  variant="h6"
                  color="orange"
                  sx={{
                    display: { xs: "none", md: "flex" },
                    fontFamily: "monospace",
                    fontWeight: 700,
                    letterSpacing: ".3rem",
                    textDecoration: "none",
                  }}
                  noWrap
                >
                  nz
                </Typography>
              </div>
              <Box sx={{ flexGrow: 1, display: { xs: "flex", md: "none" } }}>
                <IconButton
                  size="large"
                  aria-label="account of current user"
                  aria-controls="menu-appbar"
                  aria-haspopup="true"
                  onClick={handleOpenNavMenu}
                  color="inherit"
                >
                  <MenuIcon />
                </IconButton>

                <Menu
                  id="menu-appbar"
                  anchorEl={anchorElNav}
                  anchorOrigin={{
                    vertical: "bottom",
                    horizontal: "left",
                  }}
                  keepMounted
                  transformOrigin={{
                    vertical: "top",
                    horizontal: "left",
                  }}
                  open={Boolean(anchorElNav)}
                  onClose={handleCloseNavMenu}
                  sx={{
                    display: { xs: "block", md: "none" },
                  }}
                >
                  <MenuItem className="menuitem">                  
                    <PNZLogin />
                  </MenuItem>
                </Menu>
              </Box>

              {/*samll screen */}
              <div style={{ display: "flex" }}>
                <Typography
                  variant="h5"
                  color="white"
                  sx={{
                    flexGrow: 1,
                    display: { xs: "flex", md: "none" },
                    fontFamily: "monospace",
                    fontWeight: 700,
                    letterSpacing: ".3rem",
                    textDecoration: "none",
                  }}
                  noWrap
                >
                  payments
                </Typography>
                <Typography
                  variant="h5"
                  color="orange"
                  sx={{
                    flexGrow: 1,
                    display: { xs: "flex", md: "none" },
                    fontFamily: "monospace",
                    fontWeight: 700,
                    letterSpacing: ".3rem",
                    textDecoration: "none",
                  }}
                  noWrap
                >
                  nz
                </Typography>
              </div>
              <Box
                sx={{
                  display: { xs: "none", md: "flex" },
                }}
              >
                <PNZLogin />
              </Box>
            </Toolbar>
          </Container>
        </AppBar>
      </ThemeProvider>
    </>
  );
}
export default NavBar;
