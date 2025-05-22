from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema
)


airport_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="name",
            description="Partial name of the airport (case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="city",
            description="Partial name of the closest big city (case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
    ]
)

pilot_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="first_name",
            description="Pilot's first name (partial match, case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="last_name",
            description="Pilot's last name (partial match, case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
    ]
)

route_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="source",
            description="Source location (partial match, case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="destination",
            description="Destination location (partial match, case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="min_distance",
            description="Minimum distance of the route in kilometers",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="max_distance",
            description="Maximum distance of the route in kilometers",
            required=False,
            type=OpenApiTypes.INT,
        ),
    ]
)
