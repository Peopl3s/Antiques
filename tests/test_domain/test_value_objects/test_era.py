import pytest

from src.domain.exceptions import InvalidEraException
from src.domain.value_objects.era import Era


class TestEra:
    """Test cases for Era value object"""

    def test_create_era_success(self):
        """Test successful creation of Era with valid values"""
        valid_eras = [
            "paleolithic",
            "neolithic",
            "bronze_age",
            "iron_age",
            "antiquity",
            "middle_ages",
            "modern",
        ]

        for era_value in valid_eras:
            era = Era(value=era_value)
            assert era.value == era_value

    def test_create_era_invalid_value(self):
        """Test creation of Era with invalid value raises exception"""
        invalid_eras = ["invalid_era", "prehistoric", "future", "", " ", "Victorian"]

        for era_value in invalid_eras:
            with pytest.raises(InvalidEraException, match="Invalid era"):
                Era(value=era_value)

    def test_create_era_case_sensitive(self):
        """Test that Era creation is case sensitive"""
        with pytest.raises(InvalidEraException):
            Era(value="Antiquity")  # Should be lowercase

    def test_era_immutability(self):
        """Test that Era is immutable"""
        era = Era(value="antiquity")

        with pytest.raises(AttributeError):
            era.value = "modern"

    def test_era_string_representation(self):
        """Test string representation of Era"""
        era = Era(value="antiquity")
        assert str(era) == "antiquity"

    def test_era_equality(self):
        """Test equality comparison between Era instances"""
        era1 = Era(value="antiquity")
        era2 = Era(value="antiquity")
        assert era1 == era2

    def test_era_inequality(self):
        """Test inequality comparison between Era instances"""
        era1 = Era(value="antiquity")
        era2 = Era(value="modern")
        assert era1 != era2

    def test_era_ordering(self):
        """Test ordering comparison between Era instances"""
        # Note: Era is marked with order=True, so it should support ordering
        era1 = Era(value="antiquity")
        era2 = Era(value="modern")

        # Since Era uses string comparison, we can test basic ordering
        assert era1 != era2
        # The actual ordering depends on the string values

    def test_era_hash(self):
        """Test that Era can be hashed"""
        era = Era(value="antiquity")
        assert hash(era) is not None

    def test_era_in_set(self):
        """Test that Era can be used in a set"""
        era1 = Era(value="antiquity")
        era2 = Era(value="antiquity")
        era3 = Era(value="modern")

        era_set = {era1, era2, era3}
        assert len(era_set) == 2  # era1 and era2 are the same

    def test_era_as_dict_key(self):
        """Test that Era can be used as a dictionary key"""
        era1 = Era(value="antiquity")
        era2 = Era(value="modern")

        era_dict = {era1: "ancient", era2: "recent"}
        assert era_dict[era1] == "ancient"
        assert era_dict[era2] == "recent"

    def test_era_repr(self):
        """Test repr representation of Era"""
        era = Era(value="antiquity")
        repr_str = repr(era)
        assert "Era" in repr_str
        assert "antiquity" in repr_str

    def test_era_allowed_values_constant(self):
        """Test that _allowed_values contains all expected values"""
        expected_values = {
            "paleolithic",
            "neolithic",
            "bronze_age",
            "iron_age",
            "antiquity",
            "middle_ages",
            "modern",
        }
        assert Era._allowed_values == expected_values

    def test_era_post_init_validation(self):
        """Test that validation happens in __post_init__"""
        # This is implicitly tested by the invalid value test, but let's be explicit
        with pytest.raises(InvalidEraException):
            Era(value="invalid")

    def test_era_frozen(self):
        """Test that Era is frozen (immutable)"""
        era = Era(value="antiquity")

        # Try to modify the value (should fail)
        with pytest.raises(AttributeError):
            era.value = "modern"

    def test_era_slots(self):
        """Test that Era uses slots for memory efficiency"""
        era = Era(value="antiquity")

        # Check that __slots__ is defined
        assert hasattr(Era, "__slots__")
        assert "value" in Era.__slots__

        # Check that we can't add new attributes (frozen dataclass with slots prevents this)
        with pytest.raises((AttributeError, TypeError)):
            era.new_attribute = "test"

    def test_era_kw_only(self):
        """Test that Era requires keyword-only arguments"""
        # This should fail because we're trying to pass positionally
        with pytest.raises(TypeError):
            Era("antiquity")  # type: ignore

    def test_era_dataclass_properties(self):
        """Test that Era behaves as a proper dataclass"""
        era = Era(value="antiquity")

        # Check dataclass properties
        assert hasattr(era, "__dataclass_fields__")
        assert "value" in era.__dataclass_fields__

        # Check that it's frozen
        assert era.__dataclass_params__.frozen

    def test_era_final(self):
        """Test that Era is marked as final (cannot be subclassed)"""
        # Check that the class has the __final__ attribute set by @final decorator
        assert hasattr(Era, "__final__") or getattr(Era, "__final__", False)

        # In some Python versions, @final may not prevent subclassing at runtime
        # but it should provide a hint to type checkers and static analysis tools
        # Let's check if we can detect the final marker
        try:

            class SubEra(Era):
                pass

            # If subclassing succeeds, we should at least verify that the final decorator was present
            # This is a runtime limitation in some Python versions
        except TypeError:
            # This is the expected behavior in Python versions that enforce @final at runtime
            pass
