"""
CSV Export Utilities Module

This module provides utility functions for exporting data to CSV format.
"""

import csv
import io
from typing import List, Dict, Any


def results_to_csv(results: List[Dict[str, Any]], columns: List[str]) -> bytes:
    """
    Convert query results to CSV format.

    Args:
        results: List of dictionaries containing row data
        columns: List of column names

    Returns:
        bytes: CSV data encoded as UTF-8 bytes
    """
    # Create in-memory string buffer
    output = io.StringIO()

    if not columns and results:
        # If no columns provided, infer from first result
        columns = list(results[0].keys())

    if not columns:
        # Empty dataset - return CSV with single header
        columns = ['no_data']

    # Use csv.DictWriter for proper escaping and formatting
    writer = csv.DictWriter(
        output,
        fieldnames=columns,
        quoting=csv.QUOTE_MINIMAL,  # Quote only when necessary
        escapechar='\\',  # Use backslash for escaping
        lineterminator='\r\n'  # Use Windows-style line endings for compatibility
    )

    # Write header row
    writer.writeheader()

    # Write data rows if available
    if results:
        for row in results:
            # Ensure all columns are present in each row
            # Fill missing values with empty string
            row_data = {col: row.get(col, '') for col in columns}

            # Convert None values to empty string for better CSV compatibility
            row_data = {k: ('' if v is None else v) for k, v in row_data.items()}

            writer.writerow(row_data)

    # Get CSV content and encode to UTF-8 bytes
    csv_content = output.getvalue()
    output.close()

    # Return UTF-8 encoded bytes
    return csv_content.encode('utf-8')