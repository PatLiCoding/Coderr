def user_profile_path(instance, filename):
    """
    Generates a dynamic, user-isolated file system path for uploaded
    profile files.

    Extracts the original file extension and renames the file to 'profile'
    inside a directory specific to the user's ID.
    """
    ext = filename.split('.')[-1]
    return f'uploads/user_{instance.user.id}/profile.{ext}'
