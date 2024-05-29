import django.db.models as models
import karrio.server.providers.models as providers

@providers.has_auth_cache
class NinjaVanSettings(providers.Carrier):
   class Meta:
       db_table = "ninjaVan_settings"
       verbose_name = "NinjaVan Settings"
       verbose_name_plural = "NinjaVan Settings"

   api_key = models.CharField(max_length=100, blank=True, null=True)
   secret_key = models.CharField(max_length=100, blank=True, null=True)
   track_api_key = models.CharField(max_length=100, blank=True, null=True)
   track_secret_key = models.CharField(max_length=100, blank=True, null=True)
   account_number = models.CharField(max_length=50, blank=True, null=True)
   account_country_code = models.CharField(
       max_length=3, blank=True, null=True, choices=providers.COUNTRIES
   )

   @property
   def carrier_name(self) -> str:
       return "ninja_van"

   def get_auth_data(self):
       return {
           "api_key": self.api_key,
           "secret_key": self.secret_key,
           "track_api_key": self.track_api_key,
           "track_secret_key": self.track_secret_key,
           "account_number": self.account_number,
           "account_country_code": self.account_country_code,
       }

SETTINGS = NinjaVanSettings
