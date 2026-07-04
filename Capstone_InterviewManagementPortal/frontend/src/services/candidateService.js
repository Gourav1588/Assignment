import api from './api'

const candidateService = {

    async getAllCandidates(status = null) {
        const params = status ? { candidate_status: status } : {}
        const response = await api.get('/candidates', { params })
        return response.data
    },

    async getCandidateById(id) {
        const response = await api.get(`/candidates/${id}`)
        return response.data
    },

    async createCandidate(payload) {
        const response = await api.post('/candidates', payload)
        return response.data
    },

    async updateCandidate(id, payload) {
        const response = await api.put(`/candidates/${id}`, payload)
        return response.data
    },
}

export default candidateService