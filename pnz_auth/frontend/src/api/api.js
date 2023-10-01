import axios from "axios";

// Replace the URL with the deployed app's URL
const baseURL = "https://pnz-ai-assistant.azurewebsites.net/api";
// const baseURL = "http://localhost:8080/api";

export const authAPI = {
  accountconsent() {
    return axios.post(`${baseURL}/accountconsent`);
  },
  initiatecodegrant(consentId) {
    return axios.get(`${baseURL}/initiatecodegrant?consentId=${consentId}`);
  },
  accesstoken(urlCode) {
    return axios.post(`${baseURL}/accesstoken`, { code: urlCode });
  }
};
