"""
Routes for handling result search and display functionality.
"""

from flask import Blueprint, render_template, request, jsonify
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from scraper import get_student_results

# Create a Blueprint for results routes
results_bp = Blueprint('results', __name__)

@results_bp.route('/search', methods=['GET', 'POST'])
def search_results():
    """
    Handle the search form submission and display results.
    """
    if request.method == 'POST':
        # Get the roll number from the form
        roll_number = request.form.get('roll_number', '').strip()
        
        # Validate roll number (basic validation)
        if not roll_number:
            return render_template('search.html', error="Please enter a roll number")
        
        try:
            # Get the results using the scraper
            results = get_student_results(roll_number)
            
            # Render the results template with the data
            return render_template('results.html', results=results)
        
        except ValueError as e:
            # Handle errors from the scraper
            return render_template('search.html', error=str(e))
        
        except Exception as e:
            # Handle unexpected errors
            return render_template('search.html', 
                                  error=f"An unexpected error occurred: {str(e)}")
    
    # For GET requests, just show the search form
    return render_template('search.html')

@results_bp.route('/api/results/<roll_number>', methods=['GET'])
def get_results_api(roll_number):
    """
    API endpoint to get results for a roll number.
    """
    try:
        # Get the results using the scraper
        results = get_student_results(roll_number)
        return jsonify(results)
    
    except ValueError as e:
        # Handle errors from the scraper
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500
