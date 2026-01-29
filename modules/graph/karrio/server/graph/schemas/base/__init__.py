import typing
import strawberry
from strawberry.types import Info

import karrio.server.core.models as core
import karrio.server.graph.models as graph
import karrio.server.manager.models as manager
import karrio.server.providers.models as providers
import karrio.server.manager.serializers as manager_serializers
import karrio.server.graph.schemas.base.mutations as mutations
import karrio.server.graph.schemas.base.inputs as inputs
import karrio.server.graph.schemas.base.types as types
import karrio.server.graph.utils as utils

# extra_types = [*types.CarrierSettings.values()]
extra_types = []


@strawberry.type
class Query:
    user: types.UserType = strawberry.field(resolver=types.UserType.resolve)
    token: types.TokenType = strawberry.field(resolver=types.TokenType.resolve)
    api_keys: typing.List[types.APIKeyType] = strawberry.field(
        resolver=types.APIKeyType.resolve_list
    )
    workspace_config: typing.Optional[types.WorkspaceConfigType] = strawberry.field(
        resolver=types.WorkspaceConfigType.resolve
    )
    system_usage: types.SystemUsageType = strawberry.field(
        resolver=types.SystemUsageType.resolve
    )

    user_connections: utils.Connection[types.CarrierConnectionType] = strawberry.field(
        resolver=types.CarrierConnectionType.resolve_list
    )
    system_connections: utils.Connection[types.SystemConnectionType] = strawberry.field(
        resolver=types.SystemConnectionType.resolve_list
    )

    default_templates: types.DefaultTemplatesType = strawberry.field(
        resolver=types.resolve_default_templates
    )
    addresses: utils.Connection[types.AddressTemplateType] = strawberry.field(
        resolver=types.resolve_addresses
    )
    address: typing.Optional[types.AddressTemplateType] = strawberry.field(
        resolver=types.resolve_address
    )
    parcels: utils.Connection[types.ParcelTemplateType] = strawberry.field(
        resolver=types.resolve_parcels
    )
    parcel: typing.Optional[types.ParcelTemplateType] = strawberry.field(
        resolver=types.resolve_parcel
    )
    products: utils.Connection[types.ProductTemplateType] = strawberry.field(
        resolver=types.resolve_products
    )
    product: typing.Optional[types.ProductTemplateType] = strawberry.field(
        resolver=types.resolve_product
    )

    log: typing.Optional[types.LogType] = strawberry.field(
        resolver=types.LogType.resolve
    )
    logs: utils.Connection[types.LogType] = strawberry.field(
        resolver=types.LogType.resolve_list
    )

    tracing_record: typing.Optional[types.TracingRecordType] = strawberry.field(
        resolver=types.TracingRecordType.resolve
    )
    tracing_records: utils.Connection[types.TracingRecordType] = strawberry.field(
        resolver=types.TracingRecordType.resolve_list
    )

    shipment: typing.Optional[types.ShipmentType] = strawberry.field(
        resolver=types.ShipmentType.resolve
    )
    shipments: utils.Connection[types.ShipmentType] = strawberry.field(
        resolver=types.ShipmentType.resolve_list
    )

    tracker: typing.Optional[types.TrackerType] = strawberry.field(
        resolver=types.TrackerType.resolve
    )
    trackers: utils.Connection[types.TrackerType] = strawberry.field(
        resolver=types.TrackerType.resolve_list
    )

    rate_sheet: typing.Optional[types.RateSheetType] = strawberry.field(
        resolver=types.RateSheetType.resolve
    )
    rate_sheets: utils.Connection[types.RateSheetType] = strawberry.field(
        resolver=types.RateSheetType.resolve_list
    )

    manifest: typing.Optional[types.ManifestType] = strawberry.field(
        resolver=types.ManifestType.resolve
    )
    manifests: utils.Connection[types.ManifestType] = strawberry.field(
        resolver=types.ManifestType.resolve_list
    )

    pickup: typing.Optional[types.PickupType] = strawberry.field(
        resolver=types.PickupType.resolve
    )
    pickups: utils.Connection[types.PickupType] = strawberry.field(
        resolver=types.PickupType.resolve_list
    )

    carrier_connection: typing.Optional[types.CarrierConnectionType] = strawberry.field(
        resolver=types.CarrierConnectionType.resolve
    )
    carrier_connections: utils.Connection[types.CarrierConnectionType] = (
        strawberry.field(resolver=types.CarrierConnectionType.resolve_list)
    )

    metafield: typing.Optional[types.MetafieldType] = strawberry.field(
        resolver=types.MetafieldType.resolve
    )
    metafields: utils.Connection[types.MetafieldType] = strawberry.field(
        resolver=types.MetafieldType.resolve_list
    )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def update_user(
        self, info: Info, input: inputs.UpdateUserInput
    ) -> mutations.UserUpdateMutation:
        return mutations.UserUpdateMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def register_user(
        self, info: Info, input: inputs.RegisterUserMutationInput
    ) -> mutations.RegisterUserMutation:
        return mutations.RegisterUserMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_workspace_config(
        self, info: Info, input: inputs.WorkspaceConfigMutationInput
    ) -> mutations.WorkspaceConfigMutation:
        return mutations.WorkspaceConfigMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def mutate_token(
        self, info: Info, input: inputs.TokenMutationInput
    ) -> mutations.TokenMutation:
        return mutations.TokenMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def create_api_key(
        self, info: Info, input: inputs.CreateAPIKeyMutationInput
    ) -> mutations.CreateAPIKeyMutation:
        return mutations.CreateAPIKeyMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_api_key(
        self, info: Info, input: inputs.DeleteAPIKeyMutationInput
    ) -> mutations.DeleteAPIKeyMutation:
        return mutations.DeleteAPIKeyMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def request_email_change(
        self, info: Info, input: inputs.RequestEmailChangeMutationInput
    ) -> mutations.RequestEmailChangeMutation:
        return mutations.RequestEmailChangeMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def confirm_email_change(
        self, info: Info, input: inputs.ConfirmEmailChangeMutationInput
    ) -> mutations.ConfirmEmailChangeMutation:
        return mutations.ConfirmEmailChangeMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def confirm_email(
        self, info: Info, input: inputs.ConfirmEmailMutationInput
    ) -> mutations.ConfirmEmailMutation:
        return mutations.ConfirmEmailMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def change_password(
        self, info: Info, input: inputs.ChangePasswordMutationInput
    ) -> mutations.ChangePasswordMutation:
        return mutations.ChangePasswordMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def request_password_reset(
        self, info: Info, input: inputs.RequestPasswordResetMutationInput
    ) -> mutations.RequestPasswordResetMutation:
        return mutations.RequestPasswordResetMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def confirm_password_reset(
        self, info: Info, input: inputs.ConfirmPasswordResetMutationInput
    ) -> mutations.ConfirmPasswordResetMutation:
        return mutations.ConfirmPasswordResetMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def enable_multi_factor(
        self, info: Info, input: inputs.EnableMultiFactorMutationInput
    ) -> mutations.EnableMultiFactorMutation:
        return mutations.EnableMultiFactorMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def confirm_multi_factor(
        self, info: Info, input: inputs.ConfirmMultiFactorMutationInput
    ) -> mutations.ConfirmMultiFactorMutation:
        return mutations.ConfirmMultiFactorMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def disable_multi_factor(
        self, info: Info, input: inputs.DisableMultiFactorMutationInput
    ) -> mutations.DisableMultiFactorMutation:
        return mutations.DisableMultiFactorMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def create_address(
        self, info: Info, input: inputs.CreateAddressInput
    ) -> mutations.CreateAddressMutation:
        return mutations.CreateAddressMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_address(
        self, info: Info, input: inputs.UpdateAddressInput
    ) -> mutations.UpdateAddressMutation:
        return mutations.UpdateAddressMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def create_parcel(
        self, info: Info, input: inputs.CreateParcelInput
    ) -> mutations.CreateParcelMutation:
        return mutations.CreateParcelMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_parcel(
        self, info: Info, input: inputs.UpdateParcelInput
    ) -> mutations.UpdateParcelMutation:
        return mutations.UpdateParcelMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def create_product(
        self, info: Info, input: inputs.CreateProductInput
    ) -> mutations.CreateProductMutation:
        return mutations.CreateProductMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_product(
        self, info: Info, input: inputs.UpdateProductInput
    ) -> mutations.UpdateProductMutation:
        return mutations.UpdateProductMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_product(
        self, info: Info, input: inputs.DeleteMutationInput
    ) -> mutations.DeleteMutation:
        return mutations.DeleteMutation.mutate(
            info,
            model=manager.Commodity,
            validator=manager_serializers.can_mutate_commodity,
            **input.to_dict()
        )

    @strawberry.mutation
    def create_carrier_connection(
        self, info: Info, input: inputs.CreateCarrierConnectionMutationInput
    ) -> mutations.CreateCarrierConnectionMutation:
        return mutations.CreateCarrierConnectionMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_carrier_connection(
        self, info: Info, input: inputs.UpdateCarrierConnectionMutationInput
    ) -> mutations.UpdateCarrierConnectionMutation:
        return mutations.UpdateCarrierConnectionMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def mutate_system_connection(
        self, info: Info, input: inputs.SystemCarrierMutationInput
    ) -> mutations.SystemCarrierMutation:
        return mutations.SystemCarrierMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_carrier_connection(
        self, info: Info, input: inputs.DeleteMutationInput
    ) -> mutations.DeleteMutation:
        return mutations.DeleteMutation.mutate(
            info, model=providers.CarrierConnection, **input.to_dict()
        )

    @strawberry.mutation
    def partial_shipment_update(
        self, info: Info, input: inputs.PartialShipmentMutationInput
    ) -> mutations.PartialShipmentMutation:
        return mutations.PartialShipmentMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def mutate_metadata(
        self, info: Info, input: inputs.MetadataMutationInput
    ) -> mutations.MetadataMutation:
        return mutations.MetadataMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def change_shipment_status(
        self, info: Info, input: inputs.ChangeShipmentStatusMutationInput
    ) -> mutations.ChangeShipmentStatusMutation:
        return mutations.ChangeShipmentStatusMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_address(
        self, info: Info, input: inputs.DeleteMutationInput
    ) -> mutations.DeleteAddressMutation:
        return mutations.DeleteAddressMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_parcel(
        self, info: Info, input: inputs.DeleteMutationInput
    ) -> mutations.DeleteParcelMutation:
        return mutations.DeleteParcelMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def discard_commodity(
        self, info: Info, input: inputs.DeleteMutationInput
    ) -> mutations.DeleteMutation:
        return mutations.DeleteMutation.mutate(
            info,
            model=manager.Commodity,
            validator=manager_serializers.can_mutate_commodity,
            **input.to_dict()
        )

    @strawberry.mutation
    def discard_parcel(
        self, info: Info, input: inputs.DeleteMutationInput
    ) -> mutations.DeleteMutation:
        return mutations.DeleteMutation.mutate(
            info,
            model=manager.Parcel,
            validator=manager_serializers.can_mutate_parcel,
            **input.to_dict()
        )

    @strawberry.mutation
    def create_rate_sheet(
        self, info: Info, input: inputs.CreateRateSheetMutationInput
    ) -> mutations.CreateRateSheetMutation:
        return mutations.CreateRateSheetMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_rate_sheet(
        self, info: Info, input: inputs.UpdateRateSheetMutationInput
    ) -> mutations.UpdateRateSheetMutation:
        return mutations.UpdateRateSheetMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_rate_sheet_service(
        self, info: Info, input: inputs.DeleteRateSheetServiceMutationInput
    ) -> mutations.DeleteRateSheetServiceMutation:
        return mutations.DeleteRateSheetServiceMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_rate_sheet(
        self, info: Info, input: inputs.DeleteMutationInput
    ) -> mutations.DeleteMutation:
        return mutations.DeleteMutation.mutate(
            info, model=providers.RateSheet, **input.to_dict()
        )

    # ─────────────────────────────────────────────────────────────────
    # SHARED ZONE MUTATIONS (Rate Sheet Level)
    # ─────────────────────────────────────────────────────────────────

    @strawberry.mutation
    def add_shared_zone(
        self, info: Info, input: inputs.AddSharedZoneMutationInput
    ) -> mutations.AddSharedZoneMutation:
        return mutations.AddSharedZoneMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_shared_zone(
        self, info: Info, input: inputs.UpdateSharedZoneMutationInput
    ) -> mutations.UpdateSharedZoneMutation:
        return mutations.UpdateSharedZoneMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_shared_zone(
        self, info: Info, input: inputs.DeleteSharedZoneMutationInput
    ) -> mutations.DeleteSharedZoneMutation:
        return mutations.DeleteSharedZoneMutation.mutate(info, **input.to_dict())

    # ─────────────────────────────────────────────────────────────────
    # SHARED SURCHARGE MUTATIONS (Rate Sheet Level)
    # ─────────────────────────────────────────────────────────────────

    @strawberry.mutation
    def add_shared_surcharge(
        self, info: Info, input: inputs.AddSharedSurchargeMutationInput
    ) -> mutations.AddSharedSurchargeMutation:
        return mutations.AddSharedSurchargeMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_shared_surcharge(
        self, info: Info, input: inputs.UpdateSharedSurchargeMutationInput
    ) -> mutations.UpdateSharedSurchargeMutation:
        return mutations.UpdateSharedSurchargeMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_shared_surcharge(
        self, info: Info, input: inputs.DeleteSharedSurchargeMutationInput
    ) -> mutations.DeleteSharedSurchargeMutation:
        return mutations.DeleteSharedSurchargeMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def batch_update_surcharges(
        self, info: Info, input: inputs.BatchUpdateSurchargesMutationInput
    ) -> mutations.BatchUpdateSurchargesMutation:
        return mutations.BatchUpdateSurchargesMutation.mutate(info, **input.to_dict())

    # ─────────────────────────────────────────────────────────────────
    # SERVICE RATE MUTATIONS (Service-Zone Rate Mapping)
    # ─────────────────────────────────────────────────────────────────

    @strawberry.mutation
    def update_service_rate(
        self, info: Info, input: inputs.UpdateServiceRateMutationInput
    ) -> mutations.UpdateServiceRateMutation:
        return mutations.UpdateServiceRateMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def batch_update_service_rates(
        self, info: Info, input: inputs.BatchUpdateServiceRatesMutationInput
    ) -> mutations.BatchUpdateServiceRatesMutation:
        return mutations.BatchUpdateServiceRatesMutation.mutate(info, **input.to_dict())

    # ─────────────────────────────────────────────────────────────────
    # SERVICE ZONE/SURCHARGE ASSIGNMENT MUTATIONS
    # ─────────────────────────────────────────────────────────────────

    @strawberry.mutation
    def update_service_zone_ids(
        self, info: Info, input: inputs.UpdateServiceZoneIdsMutationInput
    ) -> mutations.UpdateServiceZoneIdsMutation:
        return mutations.UpdateServiceZoneIdsMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_service_surcharge_ids(
        self, info: Info, input: inputs.UpdateServiceSurchargeIdsMutationInput
    ) -> mutations.UpdateServiceSurchargeIdsMutation:
        return mutations.UpdateServiceSurchargeIdsMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def create_metafield(
        self, info: Info, input: inputs.CreateMetafieldInput
    ) -> mutations.CreateMetafieldMutation:
        return mutations.CreateMetafieldMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_metafield(
        self, info: Info, input: inputs.UpdateMetafieldInput
    ) -> mutations.UpdateMetafieldMutation:
        return mutations.UpdateMetafieldMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_metafield(
        self, info: Info, input: inputs.DeleteMutationInput
    ) -> mutations.DeleteMutation:
        return mutations.DeleteMutation.mutate(
            info, model=core.Metafield, **input.to_dict()
        )
