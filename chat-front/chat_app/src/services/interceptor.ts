import { api } from '@/api_env/api';
import axios from 'axios';

// Créer une instance Axios
const apiClient = axios.create({
  baseURL: api.url,
  timeout: 1000,
});

// Ajouter un intercepteur pour les requêtes
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token'); // Récupérer le token depuis localStorage
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;
