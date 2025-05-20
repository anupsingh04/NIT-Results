# NIT Hamirpur Results Website - User Guide

## Overview

This web application allows you to search for and view student academic results from the NIT Hamirpur results website. The application uses web scraping to retrieve data from the official results portal and presents it in a user-friendly interface with additional features like performance visualization.

## Features

1. **Search by Roll Number**: Enter any valid NIT Hamirpur roll number to retrieve student results
2. **Comprehensive Results Display**: View complete academic information including:
   - Student details (name, roll number, father's name)
   - Semester-wise subject details with grades
   - SGPI and CGPI calculations
3. **Performance Analysis**: Visual representation of academic performance trends
4. **Responsive Design**: Works on both desktop and mobile devices

## How to Use

### Accessing the Website

The website is deployed and accessible at:
[https://5000-iof0flcwwavne9z1mpy8o-2bdba362.manus.computer](https://5000-iof0flcwwavne9z1mpy8o-2bdba362.manus.computer)

### Searching for Results

1. Enter a valid roll number in the search box (e.g., 22BEC025)
2. Click the "Search Results" button
3. Wait for the results to be retrieved and displayed

### Viewing Results

Once results are retrieved, you can:

1. **View Basic Information**: Student name, roll number, father's name, and current CGPI are displayed at the top
2. **Navigate Between Semesters**: Use the tabs to switch between different semesters
3. **View Subject Details**: Each semester tab shows detailed subject information including:
   - Subject name and code
   - Credits
   - Grade
   - Grade points
4. **Analyze Performance**: The "Performance" tab provides:
   - A graph showing SGPI progression across semesters
   - Tables comparing semester performance
   - Overall academic summary

## Technical Details

### Implementation

The website is built using:
- **Backend**: Flask (Python) with BeautifulSoup for web scraping
- **Frontend**: HTML, CSS, JavaScript with Bootstrap for responsive design
- **Data Visualization**: Chart.js for performance graphs

### Source Code Structure

The application follows a standard Flask project structure:
- `src/main.py`: Main entry point for the Flask application
- `src/scraper.py`: Web scraping module for retrieving results
- `src/routes/results.py`: Routes for handling result search and display
- `src/templates/`: HTML templates for the user interface
- `src/static/`: Static assets (CSS, JavaScript, images)

### Limitations

1. The application relies on the structure of the official NIT Hamirpur results website. If that website changes significantly, the scraper may need to be updated.
2. Results are retrieved in real-time and are not stored in a database, so search performance depends on the response time of the official website.
3. This is a temporary deployment for demonstration purposes.

## Troubleshooting

If you encounter any issues:

1. **Invalid Roll Number**: Ensure you're entering a valid NIT Hamirpur roll number in the correct format
2. **No Results Found**: Verify that the roll number exists in the official system
3. **Slow Response**: The application may take a moment to retrieve and process results, especially during high traffic periods
4. **Display Issues**: Try refreshing the page or using a different browser

## Credits

This application was developed as a student project and is not affiliated with the official NIT Hamirpur website. All data is scraped from [results.nith.ac.in](http://results.nith.ac.in/scheme22/studentresult/index.asp).
