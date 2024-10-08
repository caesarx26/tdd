"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

import pytest

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status 

@pytest.fixture()
def client():
  return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndPoints:
    """Test cases for Counter-related endpoints"""

    def test_create_a_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED
    
    def test_duplicate_a_counter(self, client):
        """It should return an error for duplicates"""
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_201_CREATED
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_409_CONFLICT
        
    def test_update_a_counter(self, client):
        """It should update a counter value"""
        # Create the counter
        result = client.post('/counters/zen')
        assert result.status_code == status.HTTP_201_CREATED
    
        # Check the initial counter value
        initial_value = result.json['zen']
        
        assert initial_value == 0
    
        # Update the counter
        result = client.put('/counters/zen')
        assert result.status_code == status.HTTP_200_OK
    
        # Check the updated counter value
        updated_value = result.json['zen']
        assert updated_value == initial_value + 1
    
    def test_delete_a_counter(self, client):
        """It should update a counter value"""
        # Create the counter
        result = client.post('/counters/ben')
        assert result.status_code == status.HTTP_201_CREATED
    
        # delete the counter
        result = client.delete('/counters/ben')
        assert result.status_code == status.HTTP_204_NO_CONTENT
        
        # try to update counter was deleted and see if 404 is returned 
        result = client.put('/counters/ben')
        assert result.status_code == status.HTTP_404_NOT_FOUND
        
        # then test if the deleted counter can be deleted again shoud not be allowed
        result = client.delete('/counters/ben')
        assert result.status_code == status.HTTP_404_NOT_FOUND
      
    

    
    