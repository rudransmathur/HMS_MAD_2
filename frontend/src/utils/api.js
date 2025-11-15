const BaseURL = 'http://localhost:5000/api';

const api = {
    async request(endpoint, options = {}){
        const path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
        const url = `${BaseURL.replace(/\/$/, '')}${path}`;
        const token = localStorage.getItem('access_token');

        const headers = {"Content-Type": "application/json", ...option.headers};
        
        if (token){
            headers["Authoriztion"] = token;
        };

        const config = {...options, headers};

        try{
            response = await fetch(url, config);

            if (response.status == 401){
                aleart("Please login first.");
                throw new Error("Unauthorized");
            };

            if (!response.ok) {
                let body = null;
                try{
                    body = await response.text();
                }catch(e){
                    //console.log("Error reading response body", e);
                }
                const message = body 
                ? `${response.status} - ${body}` 
                : `HTTP error! status: ${response.status}`;

                const err = new Error(message);
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