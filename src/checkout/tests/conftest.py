from random import randint

import pytest
import faker


@pytest.fixture
def user(mixer):
    fake = faker.Faker()
    return mixer.blend("users.User", phone_number=fake.phone_number()[:randint(7, 15)])
    # This fixure slices a number because faker sometimes can
    # generate number with more than 15 digits, and it conflicts
    # with my User's model constraint for the phone_number length
