# Chit Chats API Tests

This directory contains tests for the Chit Chats connector in Karrio.

## Requirements

The tests require the following packages:

-   pytest
-   requests

Install them using pip:

```bash
pip install pytest requests
```

## Running the Tests

### Using the test runner script

The easiest way to run all tests is using the included runner script:

```bash
python modules/connectors/chitchats/tests/run_tests.py
```

Or if you're in the tests directory:

```bash
./run_tests.py
```

This script will run both unittest and pytest tests if pytest is available.

### Running tests manually

You can also run the tests manually:

#### Using pytest:

```bash
pytest modules/connectors/chitchats/tests/
```

#### Using unittest:

```bash
python modules/connectors/chitchats/tests/test_integration.py
```

## Test Files

-   `test_api.py`: Pytest-based tests for the Chit Chats API
-   `test_integration.py`: Unittest-based integration tests
-   `conftest.py`: Pytest fixtures for test configuration
-   `run_tests.py`: Script to run all tests

## Environment Variables

The following environment variables can be configured for the tests:

-   `CHITCHATS_CLIENT_ID` - Default: "208472"
-   `CHITCHATS_API_KEY` - Default: "test_api_key"
-   `CHITCHATS_BASE_URL` - Default: "https://staging.chitchats.com/api/v1"

Example:

```bash
CHITCHATS_API_KEY="your_actual_api_key" python modules/connectors/chitchats/tests/run_tests.py
```

## Test Coverage

The tests verify the following functionalities:

-   Listing shipments
-   Creating a shipment
-   Requesting rates for a shipment
-   Tracking a shipment

Note: When using a test API key, some assertions may be skipped as the test API environment may not return real data.
