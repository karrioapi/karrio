import django.db.models as models
import karrio.server.providers.models as providers

@providers.has_auth_cache
class NinjaVanSettings(providers.Carrier):
   class Meta:
       db_table = "ninjavan_settings"
       verbose_name = "NinjaVan Settings"
       verbose_name_plural = "NinjaVan Settings"

   client_id = models.CharField(max_length=255, null=False, blank=False)
   client_secret = models.CharField(max_length=255, null=False, blank=False)
   grant_type = models.CharField(max_length=255, default="client_credentials")
   account_country_code = models.CharField(
        max_length=3, blank=True, null=True, choices=providers.COUNTRIES
    )

   @property
   def carrier_name(self) -> str:
       return "ninja_van"

   def get_auth_data(self):
       return {
              "client_id": self.client_id,
              "client_secret": self.client_secret,
              "grant_type": self.grant_type,
       }

SETTINGS = NinjaVanSettings
