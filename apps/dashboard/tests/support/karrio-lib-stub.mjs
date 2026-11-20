// Stand-in for the two @karrio/lib constants the places routes read.
// Tests set them with configureAutocomplete(); live bindings reach the route.
export let ADDRESS_AUTO_COMPLETE_SERVICE = undefined;
export let ADDRESS_AUTO_COMPLETE_SERVICE_KEY = undefined;

export function configureAutocomplete(service, key) {
  ADDRESS_AUTO_COMPLETE_SERVICE = service;
  ADDRESS_AUTO_COMPLETE_SERVICE_KEY = key;
}
