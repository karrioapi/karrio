
When a request fail no exceptions are raised but all requests return a tuple of:
`Tuple[ResponseType, List[Messages]]`.

Here, the `List[Messages]` will contain the **errors**, **notes** or **messages** returned
by the process

## Examples

### Processing Error

```python
response = (
    [],
    [
        Message(
            carrier_name="canadapost",
            carrier_id="canadapost",
            message="Invalid request payload",
            code="PURPLSHIP_FIELD_ERROR",
            details={
                "parcel[0].weight": {
                    "code": "required",
                    "message": "This field is required",
                }
            },
        )
    ],
)
```

### Carrier Error

```python
response = (
    [],
    [
        Message(
            carrier_name="canadapost",
            carrier_id="canadapost",
            message="You cannot mail on behalf of the requested customer.",
            code="AA004",
            details=None,
        )
    ],
)
```
