import pytest
from pydantic import ValidationError
from User_Signup_Schema_fastApi import UserSignupSchema  # Import your schema class

def test_user_schema_valid_data():
    """Ensure valid dictionary parses correctly into the schema model."""
    valid_payload = {
        "email": "alex@example.com",
        "username": "alex_dev",
        "password": "supersecure123",
        "age": 25
    }
    # Pass dictionary as keyword arguments
    user = UserSignupSchema(**valid_payload)
    
    # Assertions prove data parsed cleanly into objects
    assert user.email == "alex@example.com"
    assert user.age == 25
    assert user.password == "supersecure123"

def test_user_schema_invalid_email():
    """Ensure Pydantic blocks malformed emails."""
    invalid_payload = {
        "email": "not-an-email-address",  # Missing @ and domain
        "username": "alex_dev",
        "password": "supersecure123"
    }
    # Assert that a ValidationError is thrown instantly
    with pytest.raises(ValidationError) as exc_info:
        UserSignupSchema(**invalid_payload)
    
    # You can inspect the error structure to verify what failed
    assert "value is not a valid email address" in str(exc_info.value)

def test_user_schema_underage_constraint():
    """Ensure Field(ge=18) constraints are active."""
    underage_payload = {
        "email": "kid@example.com",
        "username": "gamerkid",
        "password": "mypassword123",
        "age": 16  # Field rule states ge=18 (greater than or equal to 18)
    }
    with pytest.raises(ValidationError) as exc_info:
        UserSignupSchema(**underage_payload)
        
    assert "Input should be greater than or equal to 18" in str(exc_info.value)

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])