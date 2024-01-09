import React from 'react';
import { Navigate, useLocation, Outlet } from 'react-router-dom';

import { accountService } from '@/_services';

function PrivateRoute({ path, element, ...rest }) {
    const user = accountService.userValue;
    const location = useLocation();

    return (
        user
            ? <Outlet/>
            : <Navigate to="account/login" state={{ from : location }} replace/>
    );
}

export { PrivateRoute };