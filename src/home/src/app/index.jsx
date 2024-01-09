import React, { useState, useEffect} from 'react';
import { Routes, Route, useLocation, Navigate } from 'react-router-dom';

import { Nav, PrivateRoute } from '@/_components';
import { accountService } from '@/_services';
import { Home } from '@/home'
import { Account } from '@/account';
import { Profile  } from '@/profile';

function App() {
    const { pathname } = useLocation();
    const [user, setUser] = useState({});

    useEffect(
        () => {
            const subscription = accountService.user.subscribe(x => setUser(x));
            return subscription.unsubscribe;
        },
        []
    );
    return (
        <div className={'app-container' + (user && ' bg-light')}>
            <Nav/>
            <Routes>
                <Route element={<PrivateRoute/>}>
                    <Route index element={<Home />} />
                    <Route path="profile/*" element={<Profile />}/>
                    <Route path="widgets/*" element={<p>Виджеты</p>}/>
                    <Route path="analytics/*" element={<p>Аналитика</p>}/>
                </Route>
                <Route path="account/*" element={<Account />}/>
                <Route path="*" element={<Navigate to="/" />} />
            </Routes>
        </div>
    );
}

export { App };