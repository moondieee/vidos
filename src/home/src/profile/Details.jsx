import React from 'react';
import { Link } from 'react-router-dom';

import { accountService } from '@/_services';

function Details() {
    const user = accountService.userValue;

    return (
        <div>
            <h1>Ваш профиль</h1>
            <p>
                <strong>Name: </strong> {user.title} {user.full_name}<br />
                <strong>Email: </strong> {user.email}
            </p>
            <p><Link to="update">Update Profile</Link></p>
        </div>
    );
}

export { Details };