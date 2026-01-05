"""Karrio Asendia client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.asendia.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Create a parcel and retrieve the label."""
        response = lib.request(
            url=f"{self.settings.server_url}/api/parcels",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Cancel/delete a parcel by its ID."""
        parcel_id = request.serialize()

        response = lib.request(
            url=f"{self.settings.server_url}/api/parcels/{parcel_id}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Get tracking information for tracking numbers."""

        def _get_tracking(tracking_number: str):
            return tracking_number, lib.request(
                url=f"{self.settings.server_url}/api/customers/{self.settings.customer_id}/tracking/{tracking_number}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Authorization": f"Bearer {self.settings.access_token}",
                },
            )

        responses = lib.run_concurently(_get_tracking, request.serialize())

        return lib.Deserializable(
            responses,
            lambda res: [(num, lib.to_dict(track)) for num, track in res if any(track.strip())],
        )

    def create_manifest(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Create a manifest for parcels."""
        response = lib.request(
            url=f"{self.settings.server_url}/api/manifests",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_label(self, parcel_id: str, label_type: str = "PDF") -> str:
        """Fetch label for a parcel."""
        return lib.request(
            url=f"{self.settings.server_url}/api/parcels/{parcel_id}/label",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Accept": f"application/{label_type.lower()}",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=lambda r: r,
        )

    def get_return_label(self, parcel_id: str, label_type: str = "PDF") -> str:
        """Fetch return label for a parcel."""
        return lib.request(
            url=f"{self.settings.server_url}/api/parcels/{parcel_id}/return-label",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Accept": f"application/{label_type.lower()}",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=lambda r: r,
        )

    def get_manifest_document(self, manifest_id: str) -> str:
        """Fetch manifest document."""
        return lib.request(
            url=f"{self.settings.server_url}/api/manifests/{manifest_id}/document",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=lambda r: r,
        )
