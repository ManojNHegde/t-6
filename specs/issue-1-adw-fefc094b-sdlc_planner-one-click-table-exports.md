# Feature: One-Click Table Exports

## Metadata
issue_number: `1`
adw_id: `fefc094b`
issue_json: `{"number":1,"title":"One click table exports","body":"Using adw_plan_build_review add one click table exports and one click result export feature to get results as csv files.\n\nCreate two new endpoints to support these features. One exporting tables, one for exporting query results.\n\nPlace a download button directly to the left of the 'x' icon for available tables.\n\nPlace a download button directly to the left of the 'hide' button for query results.\n\nUse the appropriate download icon."}`

## Feature Description
This feature enables users to export table data and query results as CSV files with a single click. The feature adds download buttons to the user interface that allow immediate CSV export of any table in the database or any query results displayed on screen. The CSV files will be properly formatted with headers, escaped special characters, and appropriate filenames. This enhancement significantly improves data portability and allows users to extract their data for analysis in external tools like Excel, Python, or R.

## User Story
As a data analyst
I want to export tables and query results as CSV files with a single click
So that I can analyze data in external tools, create reports, and share results with colleagues without manual copying

## Problem Statement
Currently, users who want to analyze data from the Natural Language SQL Interface in external tools must manually copy and paste data from the web interface. This is time-consuming, error-prone for large datasets, and doesn't preserve proper CSV formatting. Users need a quick, reliable way to export their data while maintaining data integrity and proper formatting. Additionally, sharing query results with team members requires screenshots or manual data transfer, which is inefficient and limits collaboration.

## Solution Statement
Implement one-click CSV export functionality by adding download buttons to both the Available Tables section and Query Results section. These buttons will trigger immediate CSV downloads through dedicated API endpoints that handle proper CSV formatting, character escaping, and file generation. The solution will create two new API endpoints, integrate download buttons with precise positioning as specified, and ensure all data exports maintain integrity with proper escaping and formatting.

## Relevant Files
Use these files to implement the feature:

- `README.md` - Project overview to understand the application structure and development workflow
- `app/server/server.py` - Backend FastAPI server where the export endpoints are already partially implemented (lines 274-374)
- `app/server/core/csv_exporter.py` - CSV export utility module that handles CSV generation (already exists with 63 lines)
- `app/server/core/data_models.py` - Pydantic models including ExportQueryResultsRequest (already exists)
- `app/server/core/sql_security.py` - SQL security module for validating table names and preventing injection
- `app/server/core/sql_processor.py` - SQL execution module for fetching table data
- `app/client/src/main.ts` - Main frontend logic where download buttons are already partially implemented (lines 323-333 and 216-239)
- `app/client/src/api/client.ts` - API client with export functions already implemented (lines 85-163)
- `app/client/src/style.css` - Styling for download buttons already defined (lines 337-363)
- `app/client/src/types.d.ts` - TypeScript type definitions
- `app/client/index.html` - HTML structure to understand UI layout
- `.claude/commands/test_e2e.md` - E2E test runner documentation to understand test creation
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test for reference
- `.claude/commands/e2e/test_export_functionality.md` - Existing E2E test for export functionality

### New Files
- `.claude/commands/e2e/test_one_click_table_exports.md` - New E2E test file to validate the specific requirements of this feature

## Implementation Plan
### Phase 1: Foundation
Verify and complete the existing backend infrastructure for CSV exports. Based on the exploration, the endpoints exist but need verification that they meet all requirements including proper positioning of buttons and correct icon usage.

### Phase 2: Core Implementation
Complete or verify the frontend UI components including download buttons with exact positioning as specified: directly to the left of the 'x' icon for tables and directly to the left of the 'Hide' button for query results.

### Phase 3: Integration
Ensure seamless integration between frontend and backend components, comprehensive error handling, and validation that all edge cases are properly handled including special characters, empty results, and large datasets.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Create E2E Test Specification
- Create `.claude/commands/e2e/test_one_click_table_exports.md` based on existing patterns
- Define user story specific to the exact requirements in the issue
- Include test steps that verify button positioning (left of 'x' for tables, left of 'Hide' for results)
- Specify verification of download icon usage
- Include edge cases: empty results, special characters, NULL values
- Define success criteria matching the issue requirements

### 2. Verify Backend Table Export Endpoint
- Read `app/server/server.py` lines 274-332 to verify `/api/export/table/{table_name}` endpoint
- Confirm it validates table names using `sql_security.validate_identifier`
- Verify CSV generation with proper headers and escaping
- Test endpoint manually with curl or browser
- Ensure StreamingResponse returns proper Content-Disposition header

### 3. Verify Backend Query Results Export Endpoint
- Read `app/server/server.py` lines 334-374 to verify `/api/export/query-results` endpoint
- Confirm it accepts ExportQueryResultsRequest model
- Verify CSV generation with timestamp in filename
- Test endpoint manually with sample POST request
- Ensure proper handling of empty results

### 4. Verify CSV Export Utilities
- Read `app/server/core/csv_exporter.py` to understand CSV generation
- Verify `results_to_csv` function handles NULL values correctly
- Confirm proper escaping of special characters
- Test with data containing commas, quotes, and newlines
- Ensure UTF-8 encoding for international characters

### 5. Verify Frontend API Client Functions
- Read `app/client/src/api/client.ts` lines 85-163
- Verify `exportTable` function implementation
- Confirm `exportQueryResults` function implementation
- Check blob handling and download triggering
- Ensure proper error handling with user-friendly messages

### 6. Verify Table Export Button Position and Icon
- Read `app/client/src/main.ts` lines 323-333 for table download button
- Verify button is created with download icon (⬇)
- Confirm button is positioned DIRECTLY to the left of remove button
- Check button has className 'download-table-button'
- Ensure onclick handler calls `api.exportTable(table.name)`
- If position is incorrect, update the code to place it left of 'x' button

### 7. Verify Query Results Export Button Position and Icon
- Read `app/client/src/main.ts` lines 216-239 for results download button
- Verify button is created with download icon (⬇)
- Confirm button is positioned DIRECTLY to the left of 'Hide' button
- Check button has className 'download-results-button'
- Ensure onclick handler calls `api.exportQueryResults`
- If position is incorrect, update the code to place it left of 'Hide' button

### 8. Verify Button Styling
- Read `app/client/src/style.css` lines 337-363
- Confirm `.download-table-button` styles exist
- Verify `.download-results-button` styles exist
- Check hover effects provide visual feedback
- Ensure buttons are properly sized and aligned

### 9. Test Table Export Functionality
- Start the application using `./scripts/start.sh`
- Upload a sample CSV file
- Verify download button appears left of 'x' icon
- Click the download button for the table
- Verify CSV downloads with table name as filename
- Open CSV in Excel to verify formatting

### 10. Test Query Results Export Functionality
- Execute a natural language query
- Verify results display with download button left of 'Hide'
- Click the download button for query results
- Verify CSV downloads with timestamp in filename
- Open CSV to verify data matches displayed results

### 11. Test Edge Cases
- Test export of empty query results (WHERE 1=0)
- Test tables with special characters in data
- Test NULL values in data
- Test Unicode characters
- Test large result sets (>1000 rows)
- Verify all special characters properly escaped

### 12. Run E2E Test
- Read `.claude/commands/test_e2e.md` to understand test execution
- Read and execute `.claude/commands/e2e/test_one_click_table_exports.md`
- Verify all test steps pass
- Review screenshots to confirm UI elements properly positioned
- Ensure no regressions in existing functionality

### 13. Run Validation Commands
Execute all validation commands to ensure zero regressions.

## Testing Strategy
### Unit Tests
- Backend: Test CSV export functions handle NULL values correctly
- Backend: Test proper escaping of special characters in CSV
- Backend: Test security validation for table names
- Frontend: Test download triggering with different browsers
- Frontend: Test error handling when export fails

### Edge Cases
- Empty query results (0 rows but with column headers)
- Tables with special characters in names
- Data containing commas, quotes, newlines, tabs
- NULL values in data
- Very large result sets (>10,000 rows)
- Unicode characters and emojis in data
- Malformed table names (SQL injection attempts)
- Network errors during download
- Concurrent export requests

## Acceptance Criteria
- Download button appears DIRECTLY to the left of 'x' icon for each table in Available Tables section
- Download button appears DIRECTLY to the left of 'Hide' button in Query Results header
- Both buttons use the ⬇ download icon as specified
- Clicking table download button exports entire table as CSV
- Clicking results download button exports current query results as CSV
- CSV files have appropriate filenames (table name for tables, timestamp for query results)
- Special characters are properly escaped in CSV output
- NULL values are represented as empty strings in CSV
- Downloads start immediately without page navigation
- Error messages display if export fails
- Application remains responsive during and after export
- All existing functionality continues to work without regression

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/server && uv run pytest tests/test_sql_injection.py -v` - Verify security is maintained
- `cd app/client && bun tsc --noEmit` - Run frontend TypeScript compilation to validate no type errors
- `cd app/client && bun run build` - Run frontend build to validate production build works
- Read `.claude/commands/test_e2e.md`, then read and execute the new E2E `.claude/commands/e2e/test_one_click_table_exports.md` test file to validate this functionality works
- Manual test: Upload a CSV, verify download button is left of 'x', click it, verify CSV downloads
- Manual test: Run a query, verify download button is left of 'Hide', click it, verify results export

## Notes
- Based on exploration, the feature is partially implemented in commits 749dbe8 and aba4387
- Focus on verifying exact button positioning as specified in the issue
- Ensure the appropriate download icon (⬇) is used consistently
- The existing `.claude/commands/e2e/test_export_functionality.md` test validates general export but a new test should validate exact requirements
- Performance consideration: Current implementation handles datasets efficiently with streaming responses
- Security: Table name validation through sql_security module is critical
- Future enhancement: Consider adding export format options (JSON, Excel) in later iterations