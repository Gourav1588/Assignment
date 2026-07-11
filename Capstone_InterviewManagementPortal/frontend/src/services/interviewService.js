import api from './api'

const interviewService = {

    async getAllInterviews(page = 1, page_size = 10) {
        const response = await api.get('/interviews', {
            params: { page, page_size }
        })
        return response.data
    },

    async getMyInterviews(page = 1, page_size = 10) {
        const response = await api.get('/interviews/my', {
            params: { page, page_size }
        })
        return response.data
    },

    async getInterviewById(id) {
        const response = await api.get(`/interviews/${id}`)
        return response.data
    },

    async scheduleInterview(payload) {
        const response = await api.post('/interviews', payload)
        return response.data
    },

    async updateInterview(id, payload) {
        const response = await api.put(`/interviews/${id}`, payload)
        return response.data
    },

    async submitFeedback(id, payload) {
        const response = await api.post(`/interviews/${id}/feedback`, payload)
        return response.data
    },

    async getFeedback(id) {
        try {
            const response = await api.get(`/interviews/${id}/feedback`)
            return response.data
        } catch (err) {
            const detail = err.response?.data?.detail

            if (
                err.response?.status === 404 &&
                typeof detail === 'string' &&
                detail.toLowerCase().includes('no feedback')
            ) {
                return null
            }
            throw err
        }
    },

    async getAllInterviewersForDropdown() {
        const response = await api.get('/users', {
            params: { page: 1, page_size: 100 }
        })
        return response.data.items.filter(c => c.status !== 'SELECTED' && c.status !== 'REJECTED')
    },

}

export default interviewService