import React from "react";
import {
    Streamlit,
    StreamlitComponentBase,
    withStreamlitConnection,
  } from "streamlit-component-lib"
import { authAPI } from "./api/api";
import PopupWindow from "./components/PopupWindow";
import LoginButton from "./components/LoginButton";

class MyComponent extends StreamlitComponentBase {
    
    onBtnClick = async () => {
        try {
          const accountconsent = await authAPI.accountconsent();
          const initiatecodegrant = await authAPI.initiatecodegrant(
            accountconsent.data.consentId
          );
          const redirectUri = initiatecodegrant.data.redirect;
          const left = window.screen.width / 2 - 300;
          const top = window.screen.height / 2 - 500;
          const popup = (this.popup = PopupWindow.open(
            "pnz-oauth-authorize",
            `${redirectUri}`,
            { height: 1000, width: 600, left, top }
          ));
    
          popup.then(
            (data) => this.onSuccess(data),
            (error) => this.onFailure(error)
          );
        } catch (error) {
          this.onFailure();
        }
      };
    
      onSuccess = async (data) => {
        if (!data.code) {
          return this.onFailure(new Error("'code' not found"));
        }
        try {
          const accessToken = await authAPI.accesstoken(data.code);
          Streamlit.setComponentValue(accessToken.data.accessTokenObject)
        //   localStorageService.setAccessToken(accessToken.data.accessTokenObject);
        } catch (error) {
          this.onFailure(error);
        }
      };
    
      onFailure = (error) => {
        console.log(error);
      };
    
      render() {
        const attrs = { onClick: this.onBtnClick };
        return <LoginButton at={attrs} />;
      }  
}
 

export default withStreamlitConnection(MyComponent);
