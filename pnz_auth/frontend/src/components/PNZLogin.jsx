import React, { Component } from "react";
import PopupWindow from "./PopupWindow";
import LoginButton from "./LoginButton";
import { authAPI } from "../api/api";
import { localStorageService } from "../utils/localStorageService";

class PNZLogin extends Component {

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
      // localStorageService.setAccessToken(accessToken.data.accessTokenObject);
      Streamlit.setComponentValue(accessToken.data.accessTokenObject)
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

export default PNZLogin;
