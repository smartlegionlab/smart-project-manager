# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from typing import Dict, Optional
from dataclasses import dataclass

from smart_project_manager.core.utils import generate_id


@dataclass
class Label:
    id: str
    name: str
    color: str
    text_color: str
    description: Optional[str] = None
    created_at: Optional[str] = None

    def __init__(self,
                 name: str,
                 color: str = "#3498db",
                 description: Optional[str] = None,
                 id: Optional[str] = None,
                 created_at: Optional[str] = None,
                 text_color: str = "#ffffff"
                 ):
        self.id = id or generate_id()
        self.name = name
        self.color = color
        self.text_color = text_color
        self.description = description
        self.created_at = created_at

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "text_color": self.text_color,
            "description": self.description,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Label':
        text_color = data.get('text_color', '')
        return cls(
            id=data['id'],
            name=data['name'],
            color=data['color'],
            text_color=text_color,
            description=data.get('description'),
            created_at=data.get('created_at')
        )
