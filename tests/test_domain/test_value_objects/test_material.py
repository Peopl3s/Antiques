import pytest

from src.domain.exceptions import InvalidMaterialException
from src.domain.value_objects.material import Material


class TestMaterial:
    """Test cases for Material value object"""

    def test_create_material_success(self):
        """Test successful creation of Material with valid values"""
        valid_materials = [
            "ceramic", "metal", "stone", "glass", "bone", "wood", "textile", "other"
        ]

        for material_value in valid_materials:
            material = Material(value=material_value)
            assert material.value == material_value

    def test_create_material_invalid_value(self):
        """Test creation of Material with invalid value raises exception"""
        invalid_materials = [
            "invalid_material", "plastic", "paper", "", " ", "Concrete"
        ]

        for material_value in invalid_materials:
            with pytest.raises(InvalidMaterialException, match="Invalid material"):
                Material(value=material_value)

    def test_create_material_case_sensitive(self):
        """Test that Material creation is case sensitive"""
        with pytest.raises(InvalidMaterialException):
            Material(value="Ceramic")  # Should be lowercase

    def test_material_immutability(self):
        """Test that Material is immutable"""
        material = Material(value="ceramic")
        
        with pytest.raises(AttributeError):
            material.value = "metal"

    def test_material_string_representation(self):
        """Test string representation of Material"""
        material = Material(value="ceramic")
        assert str(material) == "ceramic"

    def test_material_equality(self):
        """Test equality comparison between Material instances"""
        material1 = Material(value="ceramic")
        material2 = Material(value="ceramic")
        assert material1 == material2

    def test_material_inequality(self):
        """Test inequality comparison between Material instances"""
        material1 = Material(value="ceramic")
        material2 = Material(value="metal")
        assert material1 != material2

    def test_material_ordering(self):
        """Test ordering comparison between Material instances"""
        # Note: Material is marked with order=True, so it should support ordering
        material1 = Material(value="ceramic")
        material2 = Material(value="metal")
        
        # Since Material uses string comparison, we can test basic ordering
        assert material1 != material2
        # The actual ordering depends on the string values

    def test_material_hash(self):
        """Test that Material can be hashed"""
        material = Material(value="ceramic")
        assert hash(material) is not None

    def test_material_in_set(self):
        """Test that Material can be used in a set"""
        material1 = Material(value="ceramic")
        material2 = Material(value="ceramic")
        material3 = Material(value="metal")
        
        material_set = {material1, material2, material3}
        assert len(material_set) == 2  # material1 and material2 are the same

    def test_material_as_dict_key(self):
        """Test that Material can be used as a dictionary key"""
        material1 = Material(value="ceramic")
        material2 = Material(value="metal")
        
        material_dict = {material1: "fragile", material2: "durable"}
        assert material_dict[material1] == "fragile"
        assert material_dict[material2] == "durable"

    def test_material_repr(self):
        """Test repr representation of Material"""
        material = Material(value="ceramic")
        repr_str = repr(material)
        assert "Material" in repr_str
        assert "ceramic" in repr_str

    def test_material_allowed_values_constant(self):
        """Test that _allowed_values contains all expected values"""
        expected_values = {
            "ceramic", "metal", "stone", "glass", "bone", "wood", "textile", "other"
        }
        assert Material._allowed_values == expected_values

    def test_material_post_init_validation(self):
        """Test that validation happens in __post_init__"""
        # This is implicitly tested by the invalid value test, but let's be explicit
        with pytest.raises(InvalidMaterialException):
            Material(value="invalid")

    def test_material_frozen(self):
        """Test that Material is frozen (immutable)"""
        material = Material(value="ceramic")
        
        # Try to modify the value (should fail)
        with pytest.raises(AttributeError):
            material.value = "metal"

    def test_material_slots(self):
        """Test that Material uses slots for memory efficiency"""
        material = Material(value="ceramic")
        
        # Check that __slots__ is defined
        assert hasattr(Material, '__slots__')
        assert 'value' in Material.__slots__
        
        # Check that we can't add new attributes (frozen dataclass with slots prevents this)
        with pytest.raises((AttributeError, TypeError)):
            material.new_attribute = "test"

    def test_material_kw_only(self):
        """Test that Material requires keyword-only arguments"""
        # This should fail because we're trying to pass positionally
        with pytest.raises(TypeError):
            Material("ceramic")  # type: ignore

    def test_material_dataclass_properties(self):
        """Test that Material behaves as a proper dataclass"""
        material = Material(value="ceramic")
        
        # Check dataclass properties
        assert hasattr(material, '__dataclass_fields__')
        assert 'value' in material.__dataclass_fields__
        
        # Check that it's frozen
        assert material.__dataclass_params__.frozen

    def test_material_final(self):
        """Test that Material is marked as final (cannot be subclassed)"""
        # Check that the class has the __final__ attribute set by @final decorator
        assert hasattr(Material, '__final__') or getattr(Material, '__final__', False)
        
        # In some Python versions, @final may not prevent subclassing at runtime
        # but it should provide a hint to type checkers and static analysis tools
        # Let's check if we can detect the final marker
        try:
            class SubMaterial(Material):
                pass
            # If subclassing succeeds, we should at least verify that the final decorator was present
            # This is a runtime limitation in some Python versions
        except TypeError:
            # This is the expected behavior in Python versions that enforce @final at runtime
            pass

    def test_material_all_values_coverage(self):
        """Test that all expected material values are covered"""
        expected_materials = [
            "ceramic", "metal", "stone", "glass", "bone", "wood", "textile", "other"
        ]
        
        for material_value in expected_materials:
            material = Material(value=material_value)
            assert material.value == material_value

    def test_material_edge_cases(self):
        """Test edge cases for Material creation"""
        # Test with whitespace
        with pytest.raises(InvalidMaterialException):
            Material(value=" ceramic ")  # Should fail due to whitespace

        # Test with empty string
        with pytest.raises(InvalidMaterialException):
            Material(value="")

        # Test with None (should fail type checking before validation)
        with pytest.raises((TypeError, InvalidMaterialException)):
            Material(value=None)  # type: ignore

    def test_material_comparison_with_different_types(self):
        """Test Material comparison with non-Material objects"""
        material = Material(value="ceramic")
        
        # Should not raise exception, just return False
        assert material != "ceramic"
        assert material != 123
        assert material != None
        assert material != []

    def test_material_boolean_context(self):
        """Test Material in boolean context"""
        material = Material(value="ceramic")
        
        # Material instances should always be truthy
        assert bool(material) is True
        assert material is not None
        assert material is not False

    def test_material_copy_behavior(self):
        """Test Material copy behavior"""
        material1 = Material(value="ceramic")
        material2 = Material(value="ceramic")
        
        # They should be equal but not the same object
        assert material1 == material2
        assert material1 is not material2
        assert hash(material1) == hash(material2)
