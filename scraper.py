"""
NIT Hamirpur Results Scraper

This module handles web scraping functionality for the NIT Hamirpur results website.
It provides functions to retrieve and parse student results based on roll numbers.
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from typing import Dict, List, Any, Optional, Union

# Constants
RESULTS_URL = "http://results.nith.ac.in/scheme22/studentresult/index.asp"
RESULTS_SUBMIT_URL = "http://results.nith.ac.in/scheme22/studentresult/result.asp"

class NITHResultsScraper:
    """
    A class to handle scraping of student results from the NIT Hamirpur results website.
    """
    
    def __init__(self):
        """Initialize the scraper with a new session."""
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': RESULTS_URL,
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def get_student_result(self, roll_number: str) -> Dict[str, Any]:
        """
        Retrieve and parse student results for the given roll number.
        
        Args:
            roll_number: The student's roll number
            
        Returns:
            A dictionary containing the parsed student results
            
        Raises:
            ValueError: If the roll number is invalid or results cannot be retrieved
        """
        try:
            # Validate roll number format
            if not self._validate_roll_number(roll_number):
                raise ValueError(f"Invalid roll number format: {roll_number}")
            
            # Get the results page
            html_content = self._fetch_results_page(roll_number)
            if not html_content:
                raise ValueError(f"Could not retrieve results for roll number: {roll_number}")
            
            # Parse the results
            parsed_results = self._parse_results_page(html_content, roll_number)
            return parsed_results
            
        except Exception as e:
            # Re-raise with more context
            raise ValueError(f"Error retrieving results for {roll_number}: {str(e)}")
    
    def _validate_roll_number(self, roll_number: str) -> bool:
        """
        Validate the format of the roll number.
        
        Args:
            roll_number: The roll number to validate
            
        Returns:
            True if the roll number is valid, False otherwise
        """
        # Basic validation - can be expanded based on actual roll number format
        if not roll_number or len(roll_number) < 5:
            return False
        
        # Check if roll number follows expected pattern (e.g., 22BEC025)
        # This pattern can be adjusted based on actual roll number format
        pattern = r'^\d{2}[A-Z]{2,3}\d{3}$'
        return bool(re.match(pattern, roll_number))
    
    def _fetch_results_page(self, roll_number: str) -> Optional[str]:
        """
        Fetch the results page for the given roll number.
        
        Args:
            roll_number: The student's roll number
            
        Returns:
            The HTML content of the results page, or None if retrieval fails
        """
        try:
            # First, visit the main page to get any cookies/session data
            self.session.get(RESULTS_URL, headers=self.headers)
            
            # Prepare form data
            form_data = {
                'RollNumber': roll_number,
                'B1': 'Submit'
            }
            
            # Submit the form
            response = self.session.post(
                RESULTS_SUBMIT_URL,
                data=form_data,
                headers=self.headers,
                allow_redirects=True
            )
            
            # Check if the response is valid
            if response.status_code != 200:
                print(f"Error: Received status code {response.status_code}")
                return None
            
            # Check if the response contains actual results (not an error page)
            if "Regular Result" not in response.text:
                print("Error: Results page does not contain expected content")
                return None
                
            return response.text
            
        except requests.RequestException as e:
            print(f"Request error: {str(e)}")
            return None
    
    def _parse_results_page(self, html_content: str, roll_number: str) -> Dict[str, Any]:
        """
        Parse the HTML content of the results page.
        
        Args:
            html_content: The HTML content of the results page
            roll_number: The student's roll number
            
        Returns:
            A dictionary containing the parsed student results
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Initialize the results dictionary
        results = {
            "student_info": {
                "roll_number": roll_number,
                "name": "",
                "father_name": ""
            },
            "semesters": [],
            "cgpi": 0.0,
            "total_grade_points": 0,
            "total_credits": 0
        }
        
        # Extract student information
        try:
            # Find student name and father name from p tags
            student_name_p = soup.find('p', string=lambda s: s and 'STUDENT NAME' in s)
            if student_name_p:
                # Get the next p tag which contains the actual name
                name_p = student_name_p.find_next('p')
                if name_p:
                    results["student_info"]["name"] = name_p.text.strip()
            
            father_name_p = soup.find('p', string=lambda s: s and 'FATHER NAME' in s)
            if father_name_p:
                # Get the next p tag which contains the actual father's name
                father_p = father_name_p.find_next('p')
                if father_p:
                    results["student_info"]["father_name"] = father_p.text.strip()
        except Exception as e:
            print(f"Error extracting student information: {str(e)}")
        
        # Extract semester-wise results
        try:
            # Find all semester headers
            semester_headers = soup.find_all('td', string=lambda s: s and 'Semester' in s)
            
            for header in semester_headers:
                semester_id = header.text.strip().split(':')[-1].strip()
                
                # Find the table containing this semester's subjects
                semester_table = header.find_parent('table')
                if not semester_table:
                    continue
                
                # Initialize semester data
                semester_data = {
                    "semester": semester_id,
                    "subjects": [],
                    "sgpi": 0.0,
                    "total_grade_points": 0,
                    "credits_attempted": 0
                }
                
                # Extract subject data
                rows = semester_table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 6:  # Subject rows have at least 6 cells
                        # Check if this is a subject row (has a number in the first cell)
                        first_cell_text = cells[0].text.strip()
                        if first_cell_text.isdigit():
                            try:
                                subject_data = {
                                    "name": cells[1].text.strip(),
                                    "code": cells[2].text.strip(),
                                    "credits": int(cells[3].text.strip()),
                                    "grade": cells[4].text.strip(),
                                    "grade_points": int(cells[5].text.strip())
                                }
                                semester_data["subjects"].append(subject_data)
                            except (ValueError, IndexError) as e:
                                print(f"Error parsing subject row: {str(e)}")
                
                # Find the SGPI/CGPI table which follows the semester table
                next_table = semester_table.find_next_sibling('table')
                if next_table:
                    # Look for the row with SGPI/CGPI information (has background color)
                    sgpi_row = next_table.find('tr', {'style': lambda value: value and 'background-color' in value})
                    if sgpi_row:
                        cells = sgpi_row.find_all('td')
                        if len(cells) >= 5:
                            try:
                                # Extract SGPI
                                sgpi_p_tags = cells[1].find_all('p')
                                if len(sgpi_p_tags) >= 2:
                                    sgpi_text = sgpi_p_tags[1].text.strip()
                                    sgpi_match = re.search(r'(\d+)/(\d+)=(\d+\.\d+)', sgpi_text)
                                    if sgpi_match:
                                        semester_data["total_grade_points"] = int(sgpi_match.group(1))
                                        semester_data["credits_attempted"] = int(sgpi_match.group(2))
                                        semester_data["sgpi"] = float(sgpi_match.group(3))
                                
                                # Extract CGPI
                                cgpi_p_tags = cells[3].find_all('p')
                                if len(cgpi_p_tags) >= 2:
                                    cgpi_text = cgpi_p_tags[1].text.strip()
                                    cgpi_match = re.search(r'(\d+)/(\d+)=(\d+\.\d+)', cgpi_text)
                                    if cgpi_match:
                                        results["total_grade_points"] = int(cgpi_match.group(1))
                                        results["total_credits"] = int(cgpi_match.group(2))
                                        results["cgpi"] = float(cgpi_match.group(3))
                            except (ValueError, IndexError) as e:
                                print(f"Error parsing SGPI/CGPI: {str(e)}")
                
                # Calculate SGPI manually if it's still 0.0 (fallback method)
                if semester_data["sgpi"] == 0.0 and semester_data["subjects"]:
                    total_grade_points = 0
                    total_credits = 0
                    for subject in semester_data["subjects"]:
                        total_grade_points += subject["grade_points"]
                        total_credits += subject["credits"]
                    
                    if total_credits > 0:
                        semester_data["total_grade_points"] = total_grade_points
                        semester_data["credits_attempted"] = total_credits
                        semester_data["sgpi"] = round(total_grade_points / total_credits, 2)
                
                # Add semester data to results
                results["semesters"].append(semester_data)
        except Exception as e:
            print(f"Error extracting semester results: {str(e)}")
        
        return results

# Function to get results for a specific roll number
def get_student_results(roll_number: str) -> Dict[str, Any]:
    """
    Get student results for the specified roll number.
    
    Args:
        roll_number: The student's roll number
        
    Returns:
        A dictionary containing the parsed student results
        
    Raises:
        ValueError: If the roll number is invalid or results cannot be retrieved
    """
    scraper = NITHResultsScraper()
    return scraper.get_student_result(roll_number)

# Function to test the scraper with a sample roll number
def test_scraper(roll_number: str) -> None:
    """
    Test the scraper with a sample roll number and print the results.
    
    Args:
        roll_number: The roll number to test with
    """
    try:
        results = get_student_results(roll_number)
        print(json.dumps(results, indent=2))
        print("Scraping successful!")
    except Exception as e:
        print(f"Scraping failed: {str(e)}")

if __name__ == "__main__":
    # Test the scraper with a sample roll number
    test_scraper("22BEC025")
