from django.urls import path
from django.views import View
from django.shortcuts import render

from purplship.core import utils
from purpleserver.core import dataunits
from purpleserver.manager.models import Tracking


class TrackingView(View):
    template_name = "client/tracking.html"

    def get(self, request, tracker_id: str):
        tracker = Tracking.objects.get(id=tracker_id)
        carrier_name = dataunits.REFERENCE_MODELS['carriers'].get(tracker.tracking_carrier.data.carrier_name)
        events = [
            {
                **event,
                "date": utils.DF.fdatetime(event.get('date'), current_format="%Y-%m-%d", output_format="%A, %B %Y")
            }
            for event in tracker.events
        ]

        context = dict(
            events=events,
            tracker=tracker,
            carrier_name=carrier_name
        )

        return render(request, self.template_name, context=context)


urlpatterns = [
    path('tracking/<str:tracker_id>', TrackingView.as_view(), name="tracking-page"),
]
