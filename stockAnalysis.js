// AI Analysis Service for Stock Data
import { AI_CONFIG } from './config.js';

export class StockAnalysisService {
    static async analyzeStocks(stockData, period = '7d') {
        try {
            const analysis = await this.getAIAnalysis(stockData, period);
            return {
                success: true,
                analysis: analysis
            };
        } catch (error) {
            console.error('AI Analysis Error:', error);
            return {
                success: false,
                error: 'Failed to analyze stock data'
            };
        }
    }

    static async getAIAnalysis(stockData, period) {
        const prompt = this.createAnalysisPrompt(stockData, period);
        
        const response = await fetch(AI_CONFIG.endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${AI_CONFIG.apiKey}`
            },
            body: JSON.stringify({
                model: AI_CONFIG.model,
                messages: [{
                    role: "user",
                    content: prompt
                }],
                temperature: 0.7,
                max_tokens: 500
            })
        });

        if (!response.ok) {
            throw new Error('AI API request failed');
        }

        const result = await response.json();
        return result.choices[0].message.content;
    }

    static createAnalysisPrompt(stockData, period) {
        // Calculate key metrics
        const metrics = this.calculateMetrics(stockData);
        
        return `Analyze the following stock data metrics over the last ${period}:
        
        ${Object.entries(metrics).map(([stock, data]) => `
        ${stock}:
        - Current Price: $${data.currentPrice}
        - Price Change: ${data.priceChange}%
        - Average Volume: ${data.avgVolume}
        - Volatility: ${data.volatility}
        `).join('\n')}
        
        Please provide:
        1. Key trends and patterns
        2. Notable correlations between stocks
        3. Potential risk factors
        4. Investment opportunities
        5. Market sentiment analysis`;
    }

    static calculateMetrics(stockData) {
        const metrics = {};
        const stockColumns = Object.keys(stockData[0]).filter(key => key !== 'Date' && key !== 'Unnamed: 0');
        
        stockColumns.forEach(stock => {
            const prices = stockData.map(row => Number(row[stock]));
            const currentPrice = prices[prices.length - 1];
            const startPrice = prices[0];
            const priceChange = ((currentPrice - startPrice) / startPrice * 100).toFixed(2);
            
            // Calculate volatility (standard deviation)
            const mean = prices.reduce((a, b) => a + b, 0) / prices.length;
            const variance = prices.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / prices.length;
            const volatility = Math.sqrt(variance).toFixed(2);
            
            metrics[stock] = {
                currentPrice: currentPrice.toFixed(2),
                priceChange: priceChange,
                avgVolume: '-', // Add volume data if available
                volatility: volatility
            };
        });
        
        return metrics;
    }
}