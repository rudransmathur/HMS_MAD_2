const BaseURL = 'http://localhost:5000/api';

const api = {
    async request(endpoint, options = {}){
        const path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
        const url = `${BaseURL}${path}`;
        const token = localStorage.getItem('access_token') || localStorage.getItem('token');

        const headers = {"Content-Type": "application/json", ...(options.headers || {})};
        
        if (token){
            // include a bearer token; server may accept raw token as well
            headers['Authorization'] = `Bearer ${token}`;
            // Also provide Flask-Security's default token header so token auth works
            headers['Authentication-Token'] = token;
        }

        // Ensure CORS mode is set and cookies are included (helps if backend uses session cookies)
        const config = {
            mode: 'cors',
            credentials: options.credentials || 'include',
            ...options,
            headers
        };

        // Helpful debug: show whether a token will be sent (remove in production if noisy)
        // eslint-disable-next-line no-console
        console.debug('[api] request', endpoint, 'tokenPresent=', !!token);

        try{
            const response = await fetch(url, config);

            if (response.status == 401){
                alert("Please login first.");
                throw new Error("Unauthorized");
            };

            if (!response.ok) {
                let errorMessage = `HTTP error! status: ${response.status}`;
                try{
                    const body = await response.text();
                    // try to parse as JSON and extract 'message' field from backend
                    if (body) {
                        try {
                            const json = JSON.parse(body);
                            if (json.message) {
                                errorMessage = json.message;
                            }
                        } catch (e) {
                            // not JSON, use raw text
                            errorMessage = body || errorMessage;
                        }
                    }
                }catch(e){
                    //console.log("Error reading response body", e);
                }

                const err = new Error(errorMessage);
                err.status = response.status;
                throw err;
            };

            if (response.status === 204) return null;

            const text = await response.text();
            if (!text) return null;

            try{
                return JSON.parse(text);
            }catch(e){
                return text;
            }
        }catch(e){
            return Promise.reject(e);
        }
    },

    get(endpoint, options = {}){
        return this.request(endpoint, {...options, method: 'GET'});
    },

    post(endpoint, data, options={}){
        return this.request(endpoint, {...options, method: 'POST', body: JSON.stringify(data)});
    },

    delete(endpoint, options = {}){
        return this.request(endpoint, {...options, method: 'DELETE'});
    }
};

export default api;