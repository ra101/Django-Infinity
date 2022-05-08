from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


class FormattedPagination(LimitOffsetPagination):
    def get_next_offset(self):
        next_offset = self.offset + self.limit
        return next_offset if next_offset < self.count else None

    def get_previous_offset(self):
        previous_offset = max(self.offset - self.limit, 0)
        return previous_offset if self.offset > 0 else None

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    (
                        "offset",
                        OrderedDict(
                            [
                                ("next", self.get_next_offset()),
                                ("previous", self.get_previous_offset()),
                            ]
                        ),
                    ),
                    ("results", data),
                ]
            )
        )

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "example": 123,
                },
                "offset": {
                    "type": "object",
                    "properties": {
                        "next": {
                            "type": "integer",
                            "nullable": True,
                            "example": 100,
                        },
                        "previous": {
                            "type": "integer",
                            "nullable": True,
                            "example": 100,
                        },
                    },
                },
                "data": schema,
            },
        }
