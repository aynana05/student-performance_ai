import joblib
import pandas as pd
import os
from datetime import datetime

class StudentPerformancePredictor:
    def __init__(self):
        # Use paths relative to backend folder - go up one level to access model and data
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(base_path, 'model', 'best_model.pkl')
        self.data_path = os.path.join(base_path, 'data', 'predictions.csv')
        self.features = [
            'Attendance',
            'Internal Test 1',
            'Internal Test 2',
            'Assignment',
            'Study Hours'
        ]
        self.model = self._load_model()
        self._init_storage()
    
    def _load_model(self):
        if os.path.exists(self.model_path):
            model = joblib.load(self.model_path)
            print(f"✓ ML Model loaded successfully from {self.model_path}")
            return model
        else:
            raise FileNotFoundError(f"Model not found at {self.model_path}")
    
    def _init_storage(self):
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        if not os.path.exists(self.data_path):
            df = pd.DataFrame(columns=[
                'timestamp', 'student_id', 'attendance', 'test1', 'test2',
                'assignment', 'study_hours', 'predicted_score', 'category'
            ])
            df.to_csv(self.data_path, index=False)
            print(f"✓ Created predictions storage")
    
    def predict(self, student_data):
        input_df = pd.DataFrame([student_data], columns=self.features)
        
        # Model predicts binary: 0 or 1
        # 0 = Lower performance (Poor/Average)
        # 1 = Higher performance (Good/Excellent)
        encoded_prediction = self.model.predict(input_df)[0]
        
        # Calculate a refined score based on actual values
        attendance = student_data['Attendance']
        test1 = student_data['Internal Test 1']
        test2 = student_data['Internal Test 2']
        assignment = student_data['Assignment']
        study_hours = student_data['Study Hours']
        
        # Calculate weighted score
        test_avg = (test1 + test2) / 2
        test_score = (test_avg / 40) * 35
        assignment_score = (assignment / 10) * 15
        attendance_score = (attendance / 100) * 25
        study_score = min((study_hours / 8), 1) * 25
        
        calculated_score = test_score + assignment_score + attendance_score + study_score
        
        # Determine category based on both model output and calculated score
        if encoded_prediction == 1:
            # Model says "Good/Excellent"
            if calculated_score >= 85:
                category = 'Excellent'
                predicted_score = 92
            else:
                category = 'Good'
                predicted_score = 82
        else:
            # Model says "Poor/Average"
            if calculated_score >= 60:
                category = 'Average'
                predicted_score = 72
            else:
                category = 'Poor'
                predicted_score = 55
        
        contributions = self._calculate_contributions(student_data)
        
        result = {
            'predicted_score': predicted_score,
            'category': category,
            'contributions': contributions,
            'confidence': self._get_confidence(predicted_score)
        }
        return result
    
    def _classify_performance(self, score):
        if score >= 90:
            return 'Excellent'
        elif score >= 80:
            return 'Good'
        elif score >= 70:
            return 'Average'
        else:
            return 'Poor'
    
    def _calculate_contributions(self, data):
        attendance_contrib = (data['Attendance'] / 100) * 25
        tests_contrib = ((data['Internal Test 1'] + data['Internal Test 2']) / 80) * 35
        assignment_contrib = (data['Assignment'] / 10) * 15
        study_contrib = min((data['Study Hours'] / 8), 1) * 25
        
        return {
            'attendance': round(attendance_contrib, 2),
            'tests': round(tests_contrib, 2),
            'assignment': round(assignment_contrib, 2),
            'study_hours': round(study_contrib, 2)
        }
    
    def _get_confidence(self, score):
        if score >= 85:
            return 'High'
        elif score >= 70:
            return 'Medium'
        else:
            return 'Low'
    
    def save_prediction(self, student_data, prediction):
        try:
            df = pd.read_csv(self.data_path)
            new_record = pd.DataFrame([{
                'timestamp': datetime.now().isoformat(),
                'student_id': student_data.get('student_id', 'N/A'),
                'attendance': student_data['Attendance'],
                'test1': student_data['Internal Test 1'],
                'test2': student_data['Internal Test 2'],
                'assignment': student_data['Assignment'],
                'study_hours': student_data['Study Hours'],
                'predicted_score': prediction['predicted_score'],
                'category': prediction['category']
            }])
            df = pd.concat([df, new_record], ignore_index=True)
            df.to_csv(self.data_path, index=False)
            return True
        except Exception as e:
            print(f"Error saving: {e}")
            return False
    
    def get_all_predictions(self):
        try:
            df = pd.read_csv(self.data_path)
            return df.to_dict('records')
        except:
            return []
    
    def get_statistics(self):
        try:
            df = pd.read_csv(self.data_path)
            if df.empty:
                return {'total': 0, 'by_category': {}, 'average_score': 0}
            
            stats = {
                'total': len(df),
                'by_category': df['category'].value_counts().to_dict(),
                'average_score': round(df['predicted_score'].mean(), 2)
            }
            return stats
        except:
            return {'total': 0, 'by_category': {}, 'average_score': 0}
        