import api from './api'

const jobService = {

    async getAllJobs(page = 1, page_size = 10) {
        const response = await api.get('/jobs', {
            params: { page, page_size }
        })
        return response.data
    },

    async getAllJobsForDropdown() {
        const response = await api.get('/jobs', {
            params: { page: 1, page_size: 100 }
        })
        return response.data.items
    },

    async getJobById(id) {
        const response = await api.get(`/jobs/${id}`)
        return response.data
    },

    async createJob(payload) {
        const response = await api.post('/jobs', payload)
        return response.data
    },

    async updateJob(id, payload) {
        const response = await api.put(`/jobs/${id}`, payload)
        return response.data
    },
}

export default jobService