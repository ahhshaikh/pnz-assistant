// import AuthApp from './AuthApp'
import NavBar from './NavBar';

export default function Home() {

    console.log('======== Home ========')

    // // const user = session?.user
    // const accessToken = session?.accessToken
    // const accessTokenExpiresAt = session?.accessTokenExpiresAt

    // // console.log(user ? user : 'Null user')
    // console.log(accessToken ? accessToken : 'Null token')
    // console.log(accessTokenExpiresAt ? accessTokenExpiresAt : 'Null token expiry')

    return (
        <div >                  
            <NavBar/>
        </div>
    );
}

