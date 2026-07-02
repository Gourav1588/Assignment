import api from './api'

const jobService = {

    async getAllJobs() {
        const response = await api.get('/jobs')
        return response.data
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