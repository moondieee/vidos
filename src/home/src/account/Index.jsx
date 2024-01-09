import React, { useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';

import { accountService } from '@/_services';

import { Login } from './Login';


function Account({ history }) {
    const navigate = useNavigate();

    useEffect(() => {
        // redirect to home if already logged in
        if (accountService.userValue) {
            navigate.push('/');
        }
    }, [navigate]);

    return (
        <div className="container">
            <div className="row">
                <div className="col-sm-8 offset-sm-2 mt-5">
                    <div className="card m-3">
                        <Routes>
                            <Route path="login" element={<Login/>} />
                        </Routes>
                    </div>
                </div>
            </div>
        </div>
    );
}

export { Account };