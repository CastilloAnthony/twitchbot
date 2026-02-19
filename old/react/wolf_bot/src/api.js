// @ts-check

import axios from 'axios';

const api = axios.create({
    baseURL: 'http://192.168.0.11:8888'
});

export default api;