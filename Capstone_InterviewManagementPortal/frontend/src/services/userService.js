import api from './api'

const userService = {

    async getAllUsers(page = 1, page_size = 10) {
        const response = await api.get('/users', {
            params: { page, page_size }
        })
        return response.data
    },

    async getUserById(id) {
        const response = await api.get(`/users/${id}`)
        return response.data
    },

    async createUser(payload) {
        const response = await api.post('/users', payload)
        return response.data
    },

    async updateUser(id, payload) {
        const response = await api.put(`/users/${id}`, payload)
        return response.data
    },

    async disableUser(id) {
        const response = await api.patch(`/users/${id}/disable`)
        return response.data
    },

    async activateUser(id) {
        const response = await api.patch(`/users/${id}/activate`)
        return response.data
    },

    async getAllInterviewersForDropdown() {
        const response = await api.get('/users', {
            params: { page: 1, page_size: 1000 }
        })
        return response.data.items.filter(u => u.role === 'Interviewer')
    },
}

export default userService