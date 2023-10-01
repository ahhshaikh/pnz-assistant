export const localStorageService = (function () {

    function _setAccessToken(tokenObj) {

        const access_token = {
            value: tokenObj.accessToken,         
            expiry: Math.floor(Date.now() / 1000) + tokenObj.expiresIn,    //epoch timestamp in seconds 
        }
        localStorage.setItem('access_token', JSON.stringify(access_token))
    }

    function _getAccessToken() {
        const accessToken = localStorage.getItem('access_token')
        if (!accessToken) {
            return null
        }
        const { expiry, value }  = JSON.parse(accessToken)
        const currentTime = Math.floor(Date.now() / 1000);
    
        // Invalidate the access token if its expiry time is within 10 seconds from the current time.
        if (expiry - currentTime < 10) {
            localStorage.removeItem('access_token')
            return null
        }
        return value

    }

    return {
        setAccessToken: _setAccessToken,
        getAccessToken: _getAccessToken
    }
})()