from dataclasses import dataclass
from typing import ClassVar, Set, final


@final
@dataclass(frozen=True, slots=True, kw_only=True, order=True)
class Material:
    _allowed_values: ClassVar[Set[str]] = {
        "ceramic", "metal", "stone", "glass", "bone", "wood", "textile", "other"
    }
    value: str

    def __post_init__(self) -> None:
        if self.value not in self._allowed_values:
            raise ValueError(f"Invalid material: {self.value}")

    def __str__(self) -> str:
        return self.value