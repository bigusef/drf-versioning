from django.utils.translation import gettext as _
from rest_framework.compat import unicode_http_header
from rest_framework.exceptions import NotAcceptable
from rest_framework.versioning import BaseVersioning


class APIVersion:
    header: str
    major: int
    minor: int
    patch: int

    def __init__(self, version: str) -> None:
        self.header = version

        cast_value = version.split(".")
        if len(cast_value) != 3:
            raise ValueError(_("This version has wrong format, Please use right format EX:1.0.0"))

        self.major, self.minor, self.patch = tuple(int(num) for num in cast_value)

    def __str__(self) -> str:
        return f"V{self.header}"

    def __repr__(self) -> str:
        return f"<APIVersion {self.header}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(str(other))

        return True if self.header == other.header else False

    def __ne__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(str(other))

        return True if self.header != other.header else False

    def __gt__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(str(other))

        if self.major > other.major:
            return True
        elif self.major == other.major and self.minor > other.minor:
            return True
        return False

    def __ge__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(str(other))

        if self > other:
            return True
        elif self.major == other.major and self.minor >= other.minor:
            return True
        return False

    def __lt__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(str(other))

        if self.major < other.major:
            return True
        elif self.major == other.major and self.minor < other.minor:
            return True
        return False

    def __le__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(str(other))

        if self < other:
            return True
        elif self.major == other.major and self.minor <= other.minor:
            return True
        return False

    def is_valid(self, version: str) -> bool:
        """
        this method used to ensure this version is released after a passed version, and compare all version numbers
        :param version: string versions want to compare a current version with
        :return: a boolean flag represent result
        """
        compared = self.__class__(version)
        if self > compared:
            return True
        elif self >= compared and self.patch >= compared.patch:
            return True
        return False

    def is_child(self, version: str) -> bool:
        """
        this method used to ensure this version is part of passed version
        :param version: string version wants to compare a current version with
        :return: a boolean flag represents a result
        """
        compared = self.__class__(version)
        return self.major == compared.major


class APIHeaderVersioning(BaseVersioning):
    empty_version_message = _("API version credentials were not provided.")
    invalid_version_message = _("Invalid version in header, Please use valid api version")

    def is_allowed_version(self, version: APIVersion) -> bool:
        # make sure a request version greater than the default version
        if self.default_version and not version.is_valid(self.default_version):
            return False

        if not self.allowed_versions:
            return True
        allowed_status = [version.is_child(v) for v in self.allowed_versions]
        return any(allowed_status)

    def determine_version(self, request, *args, **kwargs):
        version = request.META.get("HTTP_API_VERSION", self.default_version)
        if not version:
            raise NotAcceptable(self.empty_version_message)

        unicode_version = unicode_http_header(version)
        try:
            version_obj = APIVersion(version=unicode_version)
            if not self.is_allowed_version(version_obj):
                raise NotAcceptable(self.invalid_version_message)
            return version_obj
        except ValueError as ex:
            raise NotAcceptable(ex)
