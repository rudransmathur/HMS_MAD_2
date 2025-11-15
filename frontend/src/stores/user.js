import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import api from '@/utils/api';

export const useUserStore = defineStore('user',{
    state: () => ({
        token: localStorage.getItem('access_token') || localStorage.getItem('token') || '',
        user: (()=>{
            try{
                const raw = localStorage.getItem('user');
                return raw ? JSON.parse(raw) : null;
            }catch(e){
                console.log("Error parsing user from localStorage", e);
                return null;
            }
        })(),    
    }),
    getters: {
        isAuthenticated:(state)=> !!state.token,
        role:(state) => state.user && state.user.role ? state.user.role.toLowerCase() : null,
        isAdmin:(state) => (state.user && state.user.role && state.user.role.toLowerCase() === 'admin'),
        isDoctor:(state) => (state.user && state.user.role && state.user.role.toLowerCase() === 'doctor'),
        isPatient:(state) => (state.user && state.user.role && state.user.role.toLowerCase() === 'patient')
    },
    actions: {
        setToken(token){
            this.token = token || '';
            if (token) {
                try{
                    localStorage.setItem('access_token', token);
                    localStorage.setItem('token', token);
                }catch(e){ console.warn('Could not persist token', e); }
            } else {
                localStorage.removeItem('access_token');
                localStorage.removeItem('token');
            }
        },
        setUser(user){
            this.user = user;
            if (user) {
                try{
                    localStorage.setItem('user', JSON.stringify(user));
                }catch(e){
                    console.log("Error saving user to localStorage", e);
                }
            }else{
                localStorage.removeItem('user');
            }
        },
        logout(){
            this.setToken(null);
            this.setUser(null);
        },
        async loginWithCredentials(endpoint='/auth/login', credentials={}){
            try {
                const res = await api.post(endpoint, credentials);

                // backend may return token in `token` or `access_token`, and user either
                // as `user` object or individual fields. Normalize both.
                console.log("Login response:", res);
                const token = (res && (res.access_token || res.token));

                let user = null;
                if (res && res.user) {
                    user = res.user;
                } else if (res && (res.id || res.username || res.name)) {
                    user = {
                        id: res.id,
                        name: res.username ,
                        fullname: res.name || res.fullname,
                        email: res.email,
                        phone: res.phone,
                        role: res.role // may be undefined
                    };
                }

                if (!token) {
                    throw new Error("No token received from login response");
                }

                this.setToken(token);
                this.setUser(user);
                return {token, user};
            } catch (e) {
                // re-throw with server message intact (api.js extracts it from response body)
                throw e;
            }
        }
    }
});

export default useUserStore;