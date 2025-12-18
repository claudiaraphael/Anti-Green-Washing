"""
notes

Uses Kwargs to transfer data.

    It's commonly used in APIs with Flask when you want flexibility in parameters without having to explicitly define them.

    Creates an instance of the SQLAlchemy Product model. The model_dump(exclude_unset=True) converts the validated Pydantic object back to a dictionary, excluding fields that weren't set in the request. The ** unpacks the dictionary as named arguments.

    Converts the SQLAlchemy `new_product` object to the Pydantic `ProductResponseSchema` (validating the response structure) and then transforms it into a dictionary with `model_dump()`.

    Returns JSON with success message and product data, with HTTP status 201 (Created).

    If any error occurs (Pydantic validation, database error, etc.), rolls back any pending changes in the SQLAlchemy session.

    Returns formatted error as JSON with status 400 (Bad Request).

    Flow summary: receives JSON → validates with Pydantic → creates SQLAlchemy model → saves to database → formats response with Pydantic → returns JSON.


"""