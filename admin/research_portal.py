# admin/research_portal.py
class ResearchPortal:
    def get_aggregate_insights(self):
        """Get anonymized aggregate data for research"""
        insights = {
            'demographics': self.analyze_demographics(),
            'sleep_patterns': self.analyze_sleep_patterns(),
            'risk_factors': self.identify_risk_factors(),
            'correlations': self.find_correlations(),
            'trends': self.identify_trends()
        }
        return insights
    
    def export_research_data(self, format='csv'):
        """Export anonymized data for academic research"""
        data = self.get_anonymized_dataset()
        
        if format == 'csv':
            return data.to_csv(index=False)
        elif format == 'json':
            return data.to_json(orient='records')
        elif format == 'excel':
            return data.to_excel('health_research_data.xlsx')