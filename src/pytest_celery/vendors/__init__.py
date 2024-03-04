"""See :ref:`vendors`."""


def _is_vendor_installed(vendor_name: str) -> bool:
    """Check if a vendor is installed.

    Args:
        vendor_name (str): Vendor package name.

    Returns:
        bool: True if the vendor is installed, False otherwise.
    """

    try:
        container_module = f"pytest_celery.vendors.{vendor_name}.container"
        __import__(container_module)
        return True
    except ImportError:
        return False
