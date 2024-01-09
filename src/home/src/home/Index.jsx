import React from 'react';

import { accountService } from '@/_services';

function Home() {
    const user = accountService.userValue;
    
    return (
        <div className="p-4">
            <div className="container">
                <h1>Привет {user.full_name}!</h1>
                <p>Добро пожаловать в Vidos</p>
            </div>
        </div>
    );
}

export { Home };