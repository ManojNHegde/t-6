# Feature: One-Click Table and Query Results Export

## Metadata
issue_number: `1`
adw_id: `fefc094b`
issue_json: `{"number":1,"title":"One click table exports","body":"Using adw_plan_build_review add one click table exports and one click result export feature to get results as csv files.\n\nCreate two new endpoints to support these features. One exporting tables, one for exporting query results.\n\nPlace a download button directly to the left of the 'x' icon for available tables.\n\nPlace a download button directly to the left of the 'hide' button for query results.\n\nUse the appropriate download icon."}`

## Feature Description
This feature adds one-click export functionality to the Natural Language SQL Interface application, allowing users to easily download table data and query results as CSV files. The feature provides instant access to data export through strategically placed download buttons in the user interface - one for each available table in the tables section and one for query results. This enables users to quickly extract and share data from the application without requiring additional steps or navigation.

## User Story
As a data analyst or user of the Natural Language SQL Interface
I want to export table data and query results with a single click
So that I can analyze the data offline, share it with others, or import it into other tools

## Problem Statement
Currently, users can view and query their data in the web interface but have no way to export or download the results. This limitation prevents users from:
- Sharing query results with team members who don't have access to the application
- Performing additional analysis in spreadsheet applications like Excel or Google Sheets
- Creating data backups or archives
- Integrating the data with other tools in their workflow

## Solution Statement
Implement a one-click export system that adds download buttons to both the tables section and query results section. When clicked, these buttons will trigger server endpoints that generate CSV files from the data and send them to the user's browser for immediate download. The solution will:
- Add a download button next to each table's remove button for exporting entire tables
- Add a download button in the query results header for exporting query results
- Create two new API endpoints to handle table and query result exports
- Generate properly formatted CSV files with appropriate headers and data
- Use intuitive download icons for clear user understanding

## Relevant Files
Use these files to implement the feature:

- `README.md` - Project overview and architecture understanding
- `app/client/src/main.ts` - Main client application where UI elements and event handlers will be added
- `app/client/src/api/client.ts` - API client where export methods will be added
- `app/client/src/types.d.ts` - TypeScript type definitions for export request/response
- `app/client/src/style.css` - Styling for the new download buttons
- `app/server/server.py` - FastAPI server where new export endpoints will be added
- `app/server/core/data_models.py` - Pydantic models for export requests/responses
- `app/server/core/sql_processor.py` - SQL execution functions for fetching table data
- `app/server/core/sql_security.py` - Security validation for table names
- `.claude/commands/test_e2e.md` - E2E test runner documentation
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test format

### New Files
- `app/server/core/export_processor.py` - New module for CSV generation logic
- `.claude/commands/e2e/test_export_functionality.md` - New E2E test file for export feature validation

## Implementation Plan
### Phase 1: Foundation
Set up the server-side infrastructure for data export functionality, including the core CSV generation logic and data models. This phase establishes the backend foundation that will power both table and query result exports.

### Phase 2: Core Implementation
Implement the API endpoints and client-side functionality for both table exports and query result exports. This includes adding the download buttons to the UI, connecting them to the API endpoints, and handling the file download process.

### Phase 3: Integration
Ensure the export feature integrates seamlessly with existing functionality, including proper error handling, security validation, and user feedback. Add comprehensive testing to validate the feature works correctly.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Create E2E Test Specification
- Create `.claude/commands/e2e/test_export_functionality.md` with comprehensive test steps
- Define user story for export functionality testing
- Include test steps for both table export and query result export
- Specify screenshot capture points for validation
- Define success criteria for the export feature

### Implement Export Processor Module
- Create `app/server/core/export_processor.py` with CSV generation functions
- Implement `generate_csv_from_data(data: List[Dict], columns: List[str]) -> str` function
- Add proper CSV escaping for special characters (commas, quotes, newlines)
- Implement `generate_filename(base_name: str) -> str` function with timestamp
- Add unit tests for CSV generation functions

### Add Export Data Models
- Update `app/server/core/data_models.py` with export request/response models
- Create `ExportTableRequest` model with table_name and format fields
- Create `ExportQueryRequest` model with results, columns, and format fields
- Create `ExportResponse` model with file content, filename, and mime_type fields
- Ensure all models include optional error field for consistency

### Implement Table Export Endpoint
- Add `POST /api/export/table` endpoint to `app/server/server.py`
- Validate table name using `sql_security.validate_identifier()`
- Fetch table data using `sql_processor.execute_sql_safely()`
- Generate CSV using export processor functions
- Return CSV file with proper headers (Content-Disposition, Content-Type)
- Add comprehensive error handling and logging

### Implement Query Export Endpoint
- Add `POST /api/export/query` endpoint to `app/server/server.py`
- Accept query results and columns from client
- Generate CSV using export processor functions
- Return CSV file with proper headers
- Add error handling for empty results or invalid data
- Implement file size validation to prevent excessive memory usage

### Update Client API Module
- Add `exportTable(tableName: string)` method to `app/client/src/api/client.ts`
- Add `exportQueryResults(results: any[], columns: string[])` method
- Implement blob download logic using fetch API
- Handle Content-Disposition header for filename extraction
- Add proper error handling with existing displayError pattern

### Add TypeScript Types
- Update `app/client/src/types.d.ts` with export interfaces
- Define `ExportTableRequest` and `ExportQueryRequest` interfaces
- Define `ExportResponse` interface
- Ensure types align with server-side Pydantic models

### Implement Table Export UI
- Add download button to each table item in `app/client/src/main.ts`
- Position button to the left of the remove (×) button
- Use download icon (⬇ or appropriate Unicode/SVG)
- Apply consistent button styling (reuse `.remove-table-button` pattern)
- Add hover effect for visual feedback
- Implement click handler to call exportTable API

### Implement Query Export UI
- Add download button to query results header in `app/client/src/main.ts`
- Position button to the left of the Hide button
- Use consistent download icon
- Apply appropriate button styling (`.primary-button` or `.toggle-button`)
- Show/hide button based on results visibility
- Implement click handler to call exportQueryResults API

### Style Export Buttons
- Update `app/client/src/style.css` with export button styles
- Create `.export-button` class with appropriate styling
- Add hover effects consistent with existing buttons
- Ensure buttons are properly aligned and spaced
- Add loading state styles for export operations

### Add Loading States
- Implement loading spinner during export operations
- Disable buttons during export to prevent duplicate requests
- Show success messages after successful exports
- Display error messages for failed exports
- Use existing loading and message display patterns

### Implement Security Validations
- Validate all table names through sql_security module
- Prevent SQL injection in table export endpoint
- Validate data size limits to prevent memory issues
- Add rate limiting considerations for export endpoints
- Ensure proper error messages don't expose sensitive information

### Add Unit Tests
- Write tests for export_processor.py functions
- Test CSV generation with various data types
- Test special character escaping in CSV
- Test error handling in export endpoints
- Validate security measures are working correctly

### Run Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend tests to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- Read `.claude/commands/test_e2e.md`, then read and execute the new E2E `.claude/commands/e2e/test_export_functionality.md` test file to validate this functionality works

## Testing Strategy
### Unit Tests
- CSV generation with normal data
- CSV generation with special characters (commas, quotes, newlines)
- Empty dataset handling
- Large dataset handling (performance testing)
- Filename generation with timestamps
- Security validation for table names
- Error response handling

### Edge Cases
- Empty query results or tables
- Tables with special characters in names
- Very large datasets (memory limits)
- Columns with null or undefined values
- Unicode characters in data
- Concurrent export requests
- Network interruptions during download
- Tables that no longer exist when export is requested

## Acceptance Criteria
- Download buttons appear next to each table's remove button
- Download button appears next to the Hide button for query results
- Clicking download button triggers immediate CSV file download
- CSV files contain proper headers matching column names
- CSV files properly escape special characters
- Downloaded files have descriptive names with timestamps
- Export operations show loading states
- Success messages appear after successful exports
- Error messages display for failed exports
- All existing functionality continues to work without regression
- Export works for both small and reasonably large datasets
- Security validations prevent SQL injection attacks
- E2E tests pass successfully

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend tests to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_export_functionality.md` test file to validate this functionality works.

## Notes
- Consider adding JSON export format in future iterations if users request it
- The export functionality uses streaming for large datasets to prevent memory issues
- CSV format was chosen as primary export format due to universal compatibility with spreadsheet applications
- Download buttons use standard browser download behavior, no external libraries needed
- The feature follows existing UI patterns and error handling conventions for consistency
- Consider implementing batch export functionality in the future for multiple tables at once
- Rate limiting may be needed if export functionality is heavily used to prevent server overload