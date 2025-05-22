class AirPlaneFilteringMixin:
    def get_queryset(self):
        queryset = self.queryset

        min_range = self.request.query_params.get("min_range")
        max_range = self.request.query_params.get("max_range")
        model = self.request.query_params.get("model")
        country = self.request.query_params.get("country")

        if min_range:
            queryset = queryset.filter(
                max_range_km__gte=int(min_range),
            )
        if max_range:
            queryset = queryset.filter(
                max_range_km__lte=int(max_range),
            )
        if model:
            queryset = queryset.filter(
                model__icontains=model,
            )
        if country:
            queryset = queryset.filter(
                country_of_origin__icontains=country,
            )

        return queryset
