from dataclasses import dataclass, asdict
from typing import Literal, Optional


@dataclass
class DiaryBlock:
    order: int
    type: Literal["paragraph", "heading", "quote", "todo", "divider"]
    content: Optional[str] = None
    level: Optional[int] = None
    textAlign: Optional[Literal["left", "center", "right"]] = None
    marks: Optional[list[Literal["bold", "italic", "strike"]]] = None
    is_in_quote: Optional[bool] = None
    parent_type: Optional[str] = None
    token_length: Optional[int] = None
    checked: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict) -> "DiaryBlock":
        return cls(**data)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_prosemirror(cls, pm_json: dict) -> list["DiaryBlock"]:
        return [
            cls._from_node(node, order)
            for order, node in enumerate(pm_json.get("content", []))
        ]

    @classmethod
    def _from_node(cls, node: dict, order: int) -> "DiaryBlock":
        node_type = node.get("type")
        attrs = node.get("attrs", {})
        content = node.get("content", [])

        text_parts = []
        marks_set = set()

        for c in content:
            if c.get("type") == "text":
                text_parts.append(c.get("text", ""))
                if "marks" in c:
                    for mark in c["marks"]:
                        marks_set.add(mark["type"])

        return cls(
            order=order,
            type=node_type,
            content="".join(text_parts) if text_parts else None,
            level=attrs.get("level"),
            textAlign=attrs.get("textAlign"),
            marks=list(marks_set) if marks_set else None,
        )
