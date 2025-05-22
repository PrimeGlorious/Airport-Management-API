from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema
)


travel_airplane_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="min_range",
            description="Minimum range (km) the airplane can fly",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="max_range",
            description="Maximum range (km) the airplane can fly",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="model",
            description="Model name (partial match, case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="country",
            description="Country of origin (partial match, case-insensitive)",
            required=False,
            type=OpenApiTypes.STR,
        ),
    ]
)
