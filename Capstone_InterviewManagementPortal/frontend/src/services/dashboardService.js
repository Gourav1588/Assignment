import api from './api'

const dashboardService = {

    async getHRDashboard() {
        const response = await api.get('/dashboard/hr')
        return response.data
    },

    async getInterviewerDashboard() {
        const response = await api.get('/dashboard/interviewer')
        return response.data
    },

    async getAdminDashboard() {
        const response = await api.get('/dashboard/admin')
        return response.data
    },
}

export default dashboardService