# DRF Header Versioning
This repo is a proof of concept for integrate [Semantic Versioning](https://semver.org/) with [Django REST Framework](https://www.django-rest-framework.org)

I'm here using DRF capabilities to have API header called `HTTP_API_VERSION` in every request and validate the version.
and if the request doesn't contain this header, we use the drf `DEFAULT_VERSION` setting as a backup version.
another way to force a user parse version in every request is not determinate a `DEFAULT_VERSION` in the DRF settings.

The `DEFAULT_VERSION` here plays a second rule as a minial accepted version (this is a default DRF behavior),
as the passed version from any request must be greater than or equal to the default version. and in the same context
we have a using the drf `ALLOWED_VERSIONS` setting to get a list of only allowed version. and if the passed version
from request is not one of the allowed versions, the request will be rejected.

That's means if any request is not matched with versions we have the request will be returned to the client with status
code `406` as the request not acceptable duo to request a header version. also thanks to DRF we will have this version
in the request and will be accessible from the request instance will be passed to any view in the app. so in any
api view or serializer, you can take a decision based on a request version.

the version instance is of type `APIVersion` class a custom class will handle comparing any version with another version.
so this class is support some python comparing methods like (equal, not equal, grate than, grate than or equal,
smaller than and smaller than or equal). and this decision will be taken based on the semantic versioning logic for
consistences of major, minor, patch numbers. also, we take consideration the comparing version as is string.

## Contribution
If you think that anything can be improved in any way, please do suggest :
  - Open pull request with improvements
  - Discuss ideas on issues.

## License

This project is licensed under the terms of the MIT license.