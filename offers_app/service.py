def offer_path(instance, filename):
    """
    Generates a dynamic, offer-isolated file system path for uploaded files.
    """
    ext = filename.split('.')[-1]
    return f'uploads/offer_{instance.id}/offer.{ext}'
