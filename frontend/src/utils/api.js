const BaseURL = 'http://localhost:5000/api';

const api = {
    async request(endpoint, options{}){
        const path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
        const url = `${BaseURL.replace(/\/$/, '')}${path}`;
        const token = localStorage.getItem('access_token');
    }
};