# Feature: One-Click Table Exports

## Metadata
issue_number: `1`
adw_id: `b19c9946`
issue_json: `{"number":1,"title":"One click table exports","body":"Using adw_plan_build_review add one click table exports and one click result export feature to get results as csv files.\n\nCreate two new endpoints to support these features. One exporting tables, one for exporting query results.\n\nPlace a download button directly to the left of the 'x' icon for available tables.\n\nPlace a download button directly to the left of the 'hide' button for query results.\n\nUse the appropriate download icon."}`

## Feature Description
This feature adds one-click export functionality to the Natural Language SQL Interface application, allowing users to download both database tables and query results as CSV files. Users will be able to export data directly from the UI through strategically placed download buttons: one next to each table's remove button in the "Available Tables" section, and another next to the hide button in the "Query Results" section. The feature includes two new API endpoints to handle table exports and query result exports, providing a seamless way for users to extract their data for offline analysis or integration with other tools.

## User Story
As a data analyst or researcher
I want to export tables and query results as CSV files with a single click
So that I can analyze the data offline, share it with colleagues, or import it into other tools

## Problem Statement
Currently, users can upload data (CSV/JSON) and query it using natural language, but there's no way to export the processed data or query results back out of the system. Users need to manually copy data from the UI tables, which is tedious for large datasets and prone to formatting issues. This limitation prevents users from:
- Saving query results for later analysis
- Sharing specific data extracts with team members
- Importing processed data into external tools like Excel or data science notebooks
- Creating data backups or archives of transformed tables

## Solution Statement
Implement a comprehensive export system that allows users to download both full tables and query results as CSV files through intuitive one-click buttons in the UI. The solution includes:
1. Two new API endpoints (`/api/export/table/{table_name}` and `/api/export/query`) for generating CSV exports
2. Download buttons with appropriate icons placed strategically in the UI (next to existing control buttons)
3. Client-side functionality to trigger downloads and handle file naming
4. Proper CSV formatting with headers, escaped values, and appropriate content types
5. Error handling for edge cases like empty results or missing tables

## Relevant Files
Use these files to implement the feature:

- `README.md` - Project overview and instructions to understand the application structure
- `app/server/server.py` - FastAPI application where new export endpoints will be added
- `app/server/core/sql_processor.py` - SQL execution module to fetch table data for export
- `app/server/core/data_models.py` - Pydantic models, may need new export-related models
- `app/client/src/main.ts` - Client logic where export button handlers and UI updates will be added
- `app/client/src/style.css` - Styles for the new export buttons
- `app/client/src/api/client.ts` - API client to add new export endpoint calls
- `app/client/src/types.d.ts` - TypeScript interfaces for export-related types
- `app/client/index.html` - HTML structure where export buttons will be placed
- `.claude/commands/test_e2e.md` - E2E test runner documentation to understand testing approach
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test structure for reference

### New Files
- `app/server/core/export_processor.py` - New module to handle CSV generation and export logic
- `.claude/commands/e2e/test_export_functionality.md` - New E2E test file for export functionality

## Implementation Plan
### Phase 1: Foundation
Create the backend infrastructure for data export, including CSV generation utilities and core export logic that will be used by both table and query result export endpoints.

### Phase 2: Core Implementation
Implement the two API endpoints for exporting tables and query results, add the export buttons to the UI with proper positioning and styling, and connect the frontend to the backend through API calls.

### Phase 3: Integration
Integrate the export functionality seamlessly with existing UI components, ensure proper error handling and user feedback, and validate that exports work correctly with various data types and edge cases.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Create Export Processor Module
- Create `app/server/core/export_processor.py` with CSV generation utilities
- Implement functions to convert SQLite query results to CSV format
- Add proper escaping for CSV special characters (commas, quotes, newlines)
- Include timestamp in generated filenames for uniqueness

### Add Export API Endpoints
- Add `/api/export/table/{table_name}` endpoint in `server.py` for table exports
- Add `/api/export/query` endpoint in `server.py` for query result exports
- Implement proper content-type headers (text/csv) and content-disposition for file downloads
- Add error handling for missing tables or invalid queries
- Use `sql_security.py` validation for table names to prevent SQL injection

### Create E2E Test Specification
- Create `.claude/commands/e2e/test_export_functionality.md` following the pattern from `test_basic_query.md`
- Define test steps for both table export and query result export
- Include verification of download button presence and functionality
- Specify screenshot capture points for test validation

### Update TypeScript Interfaces
- Add export-related types to `app/client/src/types.d.ts`
- Define interfaces for export API responses if needed
- Update existing interfaces to include export button references

### Add Export API Client Functions
- Add `exportTable(tableName: string)` function to `app/client/src/api/client.ts`
- Add `exportQueryResults(sql: string, results: any[])` function to `app/client/src/api/client.ts`
- Implement blob download handling for CSV files
- Add proper error handling and user feedback

### Update UI Styles
- Add `.export-button` class to `app/client/src/style.css`
- Style buttons to match existing UI patterns (similar to toggle/remove buttons)
- Add hover effects and appropriate cursor styles
- Ensure buttons are properly sized and positioned

### Add Export Button to Table Headers
- Modify table item creation in `app/client/src/main.ts` (around lines 253-323)
- Add export button element to the left of the remove button (×)
- Use appropriate download icon (⬇ or similar Unicode character)
- Attach click handler to trigger table export

### Add Export Button to Query Results
- Modify results section in `app/client/index.html` (around line 35)
- Add export button to the left of the hide button in results header
- Update `app/client/src/main.ts` to handle export button visibility
- Ensure button is only shown when results are available

### Implement Export Button Handlers
- Add `exportTable(tableName: string)` function in `main.ts`
- Add `exportQueryResults()` function in `main.ts`
- Implement file download triggering using blob URLs
- Add loading states during export operations
- Display success/error messages to users

### Test Export Functionality
- Test table export with various data types (text, numbers, dates, nulls)
- Test query result export with complex queries
- Verify CSV formatting is correct (proper escaping, headers)
- Test edge cases (empty tables, no results, special characters)
- Ensure downloaded files have appropriate names with timestamps

### Run Validation Commands
Execute the `Validation Commands` to validate the feature works correctly with zero regressions.

## Testing Strategy
### Unit Tests
- Test CSV generation with various data types and special characters
- Test export endpoints with valid and invalid table names
- Test query result export with different result sets
- Verify proper HTTP headers and content types
- Test error handling for missing tables or failed queries
- Validate SQL injection protection in export endpoints

### Edge Cases
- Empty tables or query results (should export CSV with headers only)
- Tables with special characters in names
- Very large datasets (performance and memory considerations)
- Null values in data (should be represented as empty cells)
- Unicode characters in data
- CSV injection prevention (values starting with =, @, +, -)
- Concurrent export requests
- Missing or deleted tables during export

## Acceptance Criteria
- Export buttons appear to the left of the × button for each table in "Available Tables"
- Export button appears to the left of the Hide button in "Query Results"
- Clicking table export button downloads a CSV file with table name and timestamp
- Clicking query export button downloads a CSV file with query results and timestamp
- CSV files contain proper headers matching column names
- Special characters in data are properly escaped in CSV format
- Download starts immediately without page refresh or navigation
- Error messages display if export fails
- Loading indicators show during export operations
- All existing functionality continues to work without regression
- Server tests pass with `cd app/server && uv run pytest`
- Frontend TypeScript compilation succeeds with `cd app/client && bun tsc --noEmit`
- Frontend build completes successfully with `cd app/client && bun run build`
- E2E test for export functionality passes

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest -xvs` - Run all server tests including new export functionality tests
- `cd app/server && uv run pytest tests/test_sql_injection.py -v` - Verify SQL injection protection still works
- `cd app/client && bun tsc --noEmit` - Validate TypeScript types are correct
- `cd app/client && bun run build` - Ensure frontend builds successfully
- `bash scripts/start.sh` - Start the application to test manually
- Manual test: Upload a CSV file and verify export button appears next to × button
- Manual test: Run a query and verify export button appears next to Hide button
- Manual test: Click table export and verify CSV downloads with correct data
- Manual test: Click query export and verify CSV downloads with query results
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_export_functionality.md` test file to validate export functionality works end-to-end

## Notes
- Consider adding additional export formats (JSON, Excel) in future iterations
- The timestamp in filenames prevents overwriting and helps users track exports
- CSV format chosen for initial implementation due to universal compatibility
- Export buttons use download icon for intuitive user experience
- Backend implementation leverages existing SQL security measures to prevent injection attacks
- The feature respects the existing UI/UX patterns and styling conventions
- Consider implementing progress indicators for very large exports in future enhancements
- May want to add configuration for CSV delimiter preferences (comma vs. semicolon) in the future