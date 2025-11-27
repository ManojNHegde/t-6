# E2E Test: Export Functionality

Test CSV export functionality for both tables and query results in the Natural Language SQL Interface application.

## User Story

As a data analyst
I want to export tables and query results as CSV files
So that I can analyze data in external tools and share results with colleagues

## Test Steps

### Part 1: Table Export Testing

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. Upload a sample CSV file using the Upload Data button
5. **Verify** the uploaded table appears in the Available Tables section
6. Take a screenshot showing the Available Tables section
7. **Verify** a download button (⬇ or 📥) appears to the left of the 'x' icon for the table
8. Click the download button for the table
9. **Verify** a CSV file download is triggered with the table name in filename
10. Take a screenshot after clicking the download button
11. **Verify** the downloaded CSV contains headers and data
12. **Verify** the application continues to work normally after download

### Part 2: Query Results Export Testing

13. Enter the query: "SELECT * FROM [uploaded_table_name] LIMIT 5"
14. Click the Query button
15. **Verify** query results appear with data
16. Take a screenshot of the query results
17. **Verify** a download button (⬇ or 📥) appears to the left of the 'Hide' button in the results header
18. Click the download button for query results
19. **Verify** a CSV file download is triggered with "query_results" in the filename
20. Take a screenshot after clicking the download button
21. **Verify** the downloaded CSV contains the query results with proper headers
22. **Verify** the CSV has exactly 5 rows of data (matching the LIMIT clause)
23. Click "Hide" button to close results
24. **Verify** the results section is hidden

### Part 3: Edge Cases Testing

25. Execute an empty query: "SELECT * FROM [uploaded_table_name] WHERE 1=0"
26. **Verify** the download button still appears
27. Click the download button for empty results
28. **Verify** a CSV file is downloaded with headers only (no data rows)
29. Upload a table with special characters in data (commas, quotes, newlines)
30. Export the table and **Verify** special characters are properly escaped in CSV

## Success Criteria
- Download buttons appear in correct positions (left of 'x' for tables, left of 'Hide' for results)
- CSV files download immediately without page navigation
- Downloaded files have appropriate filenames
- CSV content matches the displayed data
- Special characters are properly escaped
- Empty results export headers only
- Application remains functional after exports
- 5 screenshots are taken at key points