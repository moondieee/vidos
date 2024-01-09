import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom';

import { App } from './app';
import { accountService } from '@/_services';

accountService.authByAuthToken()
    .then(() => {
        startApp();
    })
    .catch((error) => {
        console.debug('Error during authentication:', error);
        startApp();
});

function startApp() {
    const domNode = document.getElementById('app');
    const root = createRoot(domNode);

    root.render(
        <Router>
            <App />
        </Router>,
    );
}