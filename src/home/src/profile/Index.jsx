import React from 'react';
import { Routes, Route, useNavigate} from 'react-router-dom';

import { Details } from './Details';
import { Update } from './Update';

function Profile() {
    const navigate = useNavigate();
    return (
        <div className="p-4">
            <div className="container">
                <Routes>
                    <Route path="" element={<Details/>} />
                    <Route path="update" element={<Update/>} />
                </Routes>
            </div>
        </div>
    );
}

export { Profile };