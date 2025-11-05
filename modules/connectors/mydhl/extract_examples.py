#!/usr/bin/env python3
import yaml
import json
import os

# Read the OpenAPI spec
with open('/Users/anshdevnagar/Desktop/PROJECT/karrio/modules/connectors/mydhl/vendors/open-api.yaml', 'r') as f:
    spec = yaml.safe_load(f)

# Create output directory
output_dir = '/Users/anshdevnagar/Desktop/PROJECT/karrio/modules/connectors/mydhl/schemas'
os.makedirs(output_dir, exist_ok=True)

# Extract examples from the spec
examples = spec.get('components', {}).get('examples', {})

print("Found examples:", list(examples.keys()))

# Map examples to output files
example_mappings = {
    # Rate examples
    'nonDocInternationalShipmentRates': 'rate_request.json',
    'nonDocInternationalShipmentRatesResponse': 'rate_response.json',

    # Shipment examples
    'nonDocInternationalShipmentRequest': 'shipment_request.json',
    'nonDocInternationalShipmentResponse': 'shipment_response.json',

    # Pickup examples
    'nonDocRequestPickup': 'pickup_create_request.json',
    'nonDocRequestPickupResponse': 'pickup_create_response.json',
}

# Save the mapped examples
for example_key, filename in example_mappings.items():
    if example_key in examples:
        example_data = examples[example_key].get('value', {})
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w') as f:
            json.dump(example_data, f, indent=2)
        print(f"Created {filename}")
    else:
        print(f"Warning: {example_key} not found in examples")

# Look at error response example from paths
paths = spec.get('paths', {})
error_found = False

# Extract error response from rates endpoint
for path, methods in paths.items():
    if '/rates' in path:
        post_method = methods.get('post', {})
        responses = post_method.get('responses', {})
        error_400 = responses.get('400', {})
        content = error_400.get('content', {}).get('application/json', {})
        error_examples = content.get('examples', {})
        if error_examples:
            # Get first error example
            first_error = list(error_examples.values())[0]
            error_data = first_error.get('value', {})
            output_path = os.path.join(output_dir, 'error_response.json')
            with open(output_path, 'w') as f:
                json.dump(error_data, f, indent=2)
            print(f"Created error_response.json")
            error_found = True
            break

if not error_found:
    print("Warning: Error response example not found")

print("\nAll available examples in spec:")
for key in examples.keys():
    print(f"  - {key}")
