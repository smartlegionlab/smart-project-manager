# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
from typing import Dict, Optional
from dataclasses import dataclass

from smart_project_manager.core.utils import generate_id


@dataclass
class Label:
    id: str
    name: str
    color: str
    description: Optional[str] = None
    created_at: Optional[str] = None

    def __init__(self,
                 name: str,
                 color: str = "#3498db",
                 description: Optional[str] = None,
                 id: Optional[str] = None,
                 created_at: Optional[str] = None
                 ):
        self.id = id or generate_id()
        self.name = name
        self.color = color
        self.description = description
        self.created_at = created_at

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "description": self.description,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Label':
        return cls(
            id=data['id'],
            name=data['name'],
            color=data['color'],
            description=data.get('description'),
            created_at=data.get('created_at')
        )
