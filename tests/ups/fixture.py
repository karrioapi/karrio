from purplship.mappers.ups import UPSClient, UPSProxy

proxy = UPSProxy(UPSClient(
  server_url="https://wwwcie.ups.com/webservices",
  username="username",
  password="password",
  access_license_number="FG09H9G8H09GH8G0"
))