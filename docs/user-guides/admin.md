# Administration

When your shipping API is deployed and fully functional, you can handle administration related tasks
from the `Admin Console`.


!!! quote ""
    <figure>
      <img src="/tutos/admin-console-access.png" height="200" />
    </figure>

!!! info
    The admin console is only accessible to staff users of the system.
    Therefore, the link will only appear on staff users web app sessions.

## Email config

From the purplship server admin console, you can configure your email server.

!!! note "Email Config"

    - from the `Admin Console` page
    - click on the `change` button of the `CONSTANCE > Config` section
    - fill in your email server configuration and connection credential
    - and save


## Geocoding API

From the purplship server admin console, you can add your Google Geocoding API key,
to enable the `address validation` and `address autocompletion` features.

!!! note "Google Geocoding Config"

    - from the `Admin Console` page
    - click on the `change` button of the `CONSTANCE > Config` section
    - Set your `GOOGLE_CLOUD_API_KEY`
    - and save

## Price addons

As a carrier or broker, you can add your own markups (addons or additional charge) to shipping rates returned from
the purplship server carrier accounts through the API.

!!! note "Adding Rate Markup"

    - from the `Admin Console` page
    - click on the `add` button of the `CUSTOM PRICING > Broker Surcharges` section
    - Fil in the quote markup amount or percentage and set the conditions in which it should be added (applied)

