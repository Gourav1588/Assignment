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

    async createCandidate(formData) {
        const response = await api.post('/candidates', formData)
        return response.data
    },

    async updateCandidate(id, payload) {
        const response = await api.put(`/candidates/${id}`, payload)
        return response.data
    },

    async updateStatus(id, status) {
        const response = await api.patch(`/candidates/${id}/status`, { status })
        return response.data
    },

    async viewResume(id) {
        const response = await api.get(`/candidates/${id}/resume`, {
            responseType: 'blob',
        })
        const blob = new Blob([response.data], { type: 'application/pdf' })
        const url = URL.createObjectURL(blob)
        window.open(url, '_blank')
    },

    async getStatusHistory(id) {
        const response = await api.get(`/candidates/${id}/status-history`)
        return response.data
    },



}

export default candidateService