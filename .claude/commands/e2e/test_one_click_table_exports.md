# E2E Test: One-Click Table Exports

## User Story
As a data analyst
I want to export tables and query results as CSV files with a single click
So that I can analyze data in external tools and share results with colleagues

## Test Objective
Verify that users can export both database tables and query results as CSV files using download buttons that are properly positioned and use the correct download icon.

## Prerequisites
- Application is running
- Sample CSV file available for upload
- Browser with download capability

## Test Steps

### Setup
1. Start the application
2. Navigate to the main interface
3. Upload a sample CSV file containing:
   - Multiple columns with various data types
   - Special characters (commas, quotes, newlines)
   - NULL values
   - Unicode characters

### Test Case 1: Table Export Button Position and Functionality
1. **Verify Button Position**
   - Observe the Available Tables section
   - Confirm download button (⬇) appears DIRECTLY to the left of the 'x' (remove) icon
   - Take screenshot for verification

2. **Test Table Export**
   - Click the download button for the uploaded table
   - Verify CSV file downloads immediately
   - Confirm filename matches table name
   - Open CSV and verify:
     - All columns present with headers
     - Data matches original upload
     - Special characters properly escaped
     - NULL values represented as empty strings

### Test Case 2: Query Results Export Button Position and Functionality
1. **Execute Query**
   - Enter natural language query: "Show all data from the uploaded table"
   - Wait for results to display

2. **Verify Button Position**
   - Observe the Query Results header
   - Confirm download button (⬇) appears DIRECTLY to the left of 'Hide' button
   - Take screenshot for verification

3. **Test Results Export**
   - Click the download button for query results
   - Verify CSV file downloads immediately
   - Confirm filename contains timestamp
   - Open CSV and verify:
     - Column headers match displayed results
     - Data rows match displayed results
     - Formatting preserved

### Test Case 3: Edge Cases
1. **Empty Results**
   - Execute query: "Show data where 1=0"
   - Click download button
   - Verify CSV downloads with headers only

2. **Special Characters**
   - Execute query selecting rows with special characters
   - Export results
   - Verify proper escaping in CSV

3. **Large Dataset**
   - Upload larger CSV (>1000 rows)
   - Export entire table
   - Verify complete data export

### Test Case 4: Error Handling
1. **Network Error Simulation**
   - Attempt export with network throttled
   - Verify appropriate error message displays

2. **Invalid Table Name**
   - Attempt to export non-existent table (if applicable)
   - Verify error handling

## Expected Results
- ✅ Download button for tables positioned directly left of 'x' icon
- ✅ Download button for results positioned directly left of 'Hide' button
- ✅ Both buttons display ⬇ download icon
- ✅ Table exports use table name as filename
- ✅ Query result exports include timestamp in filename
- ✅ All data exported correctly with proper CSV formatting
- ✅ Special characters escaped properly
- ✅ NULL values handled as empty strings
- ✅ Downloads start immediately without navigation
- ✅ Error messages display for failed exports
- ✅ Application remains responsive during exports

## Pass/Fail Criteria
Test PASSES if all expected results are met.
Test FAILS if:
- Buttons are not in specified positions
- Wrong icon is used
- CSV data is corrupted or incomplete
- Downloads don't trigger immediately
- Special characters break CSV format
- Application becomes unresponsive

## Notes
- Use browser developer tools to verify network requests
- Check browser console for JavaScript errors
- Save exported CSV files for comparison
- Document any unexpected behavior