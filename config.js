// API Configuration
export const AI_CONFIG = {
    baseUrl: 'http://localhost:8000',
    endpoints: {
        analyze: '/analyze',
        health: '/health'
    },
    settings: {
        model: 'gpt-3.5-turbo'
    }
};