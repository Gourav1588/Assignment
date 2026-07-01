import axios from 'axios'
import api from './api'
import { buildBasicAuthHeader } from '../utils/auth'

const BASE_URL = '/api/v1'

const authService = {

  // Login — cannot use api instance because session doesn't exist yet
  async login(email, password) {
    const response = await axios.post(`${BASE_URL}/auth/login`, null, {
      headers: {
        'Authorization': buildBasicAuthHeader(email, password),
        'Content-Type': 'application/json',
      },
    })
    return response.data
  },

  async changePassword(oldPassword, newPassword) {
    const response = await api.post('/auth/change-password', {
      old_password: oldPassword,
      new_password: newPassword,
    })
    return response.data
  },


}

export default authService