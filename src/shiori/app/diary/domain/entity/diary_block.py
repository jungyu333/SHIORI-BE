from dataclasses import dataclass, asdict
from typing import Literal, Optional


@dataclass
class DiaryBlock:
    order: int
    type: Literal["paragraph", "heading", "quote", "todo", "divider"]
    content: Optional[str] = None
    level: Optional[int] = None
    textAlign: Optional[Literal["left", "center", "right"]] = None
    marks: Optional[list[Literal["bold", "italic", "strike", "underline"]]] = None
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
            for order, node in enumerate(pm_json.get("content", []) or [])
        ]

    @classmethod
    def _from_node(
        cls, node: dict, order: int, parent_type: Optional[str] = None
    ) -> "DiaryBlock":
        node_type = node.get("type")

        normalized_type = "quote" if node_type in ("blockquote", "quote") else node_type

        attrs = node.get("attrs") or {}
        text_align = attrs.get("textAlign") or attrs.get("text_align")
        level = attrs.get("level")

        def gather_text_and_marks(
            n: dict, buf_text: list[str], buf_marks: set[str]
        ) -> None:
            if not isinstance(n, dict):
                return

            if n.get("type") == "text":
                buf_text.append(n.get("text", "") or "")
                for m in n.get("marks") or []:  # ← 안전 반복
                    mt = m.get("type")
                    if mt:
                        buf_marks.add(mt)

            for child in n.get("content") or []:
                gather_text_and_marks(child, buf_text, buf_marks)

        text_parts: list[str] = []
        marks_set: set[str] = set()
        gather_text_and_marks(node, text_parts, marks_set)

        allowed_marks = {"bold", "italic", "strike", "underline", "code"}
        marks_list = [m for m in marks_set if m in allowed_marks]

        return cls(
            order=order,
            type=normalized_type,
            content=("".join(text_parts) or None),
            level=level,
            textAlign=text_align,
            marks=(marks_list or None),
            is_in_quote=(parent_type in ("blockquote", "quote")),
            parent_type=parent_type,
        )
