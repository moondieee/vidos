import { fetchWrapper, history } from '@/_helpers';
import {LocalStorageBehaviorSubject} from './storage';

const userSubject = new LocalStorageBehaviorSubject(null);
const ACCOUNTS_API_URL = process.env.ACCOUNTS_API_URL;

export const accountService = {
    ACCOUNTS_API_URL,
    authByAuthToken,
    logout,
    login,
    user: userSubject.asObservable(),
    get userValue () { return userSubject.value }
};

function login(email, password) {
    return fetchWrapper.post(`${ACCOUNTS_API_URL}/token/login/`, { email, password })
        .then(result => {
            var user = userSubject.asObservable();
            user.jwtToken = result.auth_token;
            userSubject.next(user);
            return user;
        })
        .then(authByAuthToken)
        .catch(error => {
            console.error('Error during login:', error);
            throw error;
        });
}

function logout() {
    // revoke token, stop refresh timer, publish null to user subscribers and redirect to login page
    fetchWrapper.post(`${ACCOUNTS_API_URL}/token/logout/`, {});
    userSubject.next(null);
    history.push('/account/login');
}

function authByAuthToken() {
    return fetchWrapper.get(`${ACCOUNTS_API_URL}/users/me/`, {})
        .then(user => {
            const userFull = { ...user, ...accountService.userValue };
            userSubject.next(userFull);
            return userFull;
        });
}