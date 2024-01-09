import React, { useState, useEffect } from 'react';
import { NavLink} from 'react-router-dom';

import { accountService } from '@/_services';

function Nav() {
    const [user, setUser] = useState({});

    useEffect(() => {
        const subscription = accountService.user.subscribe(x => setUser(x));
        return subscription.unsubscribe;
    }, []);

    if (!user) return null;

    return (
        <div>
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <div className="navbar-nav mx-auto">
                    <NavLink to="/" className="navbar-brand">Vidos</NavLink>
                    <NavLink to="widgets" className="nav-item nav-link">Виджеты</NavLink>
                    <NavLink to="analytics" className="nav-item nav-link">Аналитика</NavLink>
                    <NavLink to="profile" className="nav-item nav-link">Личный кабинет</NavLink>
                    <a onClick={accountService.logout} className="nav-item nav-link">Выйти</a>
                </div>
            </nav>
        </div>
    );
}

export { Nav };