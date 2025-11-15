import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import api from '@/utils/api';

const useUserStore = defineStore('user',{
    state: () => ({
        token: localStorage.getItem('token') || '',
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
        role:(state) => state.user && state.user.role ? state.user.role : null,
        isAdmin:(state) => state.user && state.user.role === 'admin'
    },
    actions: {
        setToken(token){
            this.token = token;
            localStorage.setItem('access_token', token);
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
            const res = await api.post(endpoint, credentials);
            const token = res && 
                        (res.access_token 
                        || res.token 
                        || (res.data && (res.data.access_token || res.data.token)));
            const user = res && (res.user || (res.data && res.data.user) || res);
            if (!token) {
                throw new Error("No token received from login response");
            }
            this.setToken(token);
            this.setUser(user);
            return {token, user};
        }
    }
});

export default useUserStore;