import axios from 'axios';
import { access_token } from '../constants/token';
import { BASE_HTTP_URL } from '../constants/baseURL';

export const instance = axios.create({
  baseURL: BASE_HTTP_URL,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access_token}`
  }
});

export default instance;